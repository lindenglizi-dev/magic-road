"""Read bounded original MIO train members, never the full3.7GB tar."""
from pathlib import Path
import hashlib
import io
import tarfile
import urllib.request

from PIL import Image, ImageDraw
from .prepare_ground48 import ROOT, write_json

OUT = ROOT/'cnn/data/mio_ac_screen_20261010_v2'
URL = 'https://tcd.miovision.com/static/dataset/MIO-TCD-Localization.tar'
TOTAL = 3739303424
ETAG = '"11b2deb84e85d9cf7f7e76f404cc5d06-446"'
MAX_IMAGES = 48


def allowed(name):
    parts = Path(name).as_posix().split('/')
    return len(parts)==3 and parts[:2]==['MIO-TCD-Localization','train'] and parts[2].endswith('.jpg') and '..' not in parts


def fetch():
    if OUT.exists():
        raise FileExistsError('Preserve previous/partial source evidence')
    OUT.mkdir(parents=True)
    ranges, members, skipped_test_headers = [], [], []
    transferred = 0

    def read_range(offset, size):
        nonlocal transferred
        if size<=0 or offset<0 or offset+size>TOTAL or transferred+size>8*1024**2 or len(ranges)>=240:
            raise ValueError('Bounded range violation')
        end = offset+size-1
        req = urllib.request.Request(URL,headers={'Range':f'bytes={offset}-{end}','If-Range':ETAG,'User-Agent':'RoadYOLO-research/1'})
        with urllib.request.urlopen(req,timeout=20) as response:
            if response.status!=206 or response.headers.get('Content-Range')!=f'bytes {offset}-{end}/{TOTAL}' or response.headers.get('ETag')!=ETAG:
                raise ValueError('Source changed/range ignored; no full-download fallback')
            raw = response.read(size+1)
            if len(raw)!=size:
                raise ValueError('Incomplete range')
        transferred += size
        ranges.append(dict(offset=offset,bytes=size,sha256=hashlib.sha256(raw).hexdigest()))
        return raw

    offset = 0
    while len(members)<MAX_IMAGES:
        header = read_range(offset,512)
        if header==b'\0'*512:
            break
        info = tarfile.TarInfo.frombuf(header,'utf-8','strict')
        data_offset = offset+512
        if info.type in (tarfile.XHDTYPE,tarfile.XGLTYPE):
            # PAX path/mtime metadata only; do not read a subsequent image until its train path is checked.
            if info.size>4096:
                raise ValueError('Unexpected PAX metadata size')
            read_range(data_offset,info.size)
        elif info.isfile():
            if info.name.startswith('MIO-TCD-Localization/test/') and info.name.endswith('.jpg'):
                skipped_test_headers.append(info.name)
                offset=data_offset+((info.size+511)//512)*512
                continue
            if not allowed(info.name):
                raise ValueError(f'Stop at non-train/non-JPEG member: {info.name}')
            if not 0<info.size<256*1024:
                raise ValueError('Unexpected JPEG size')
            raw=read_range(data_offset,info.size)
            with Image.open(io.BytesIO(raw)) as im:
                im.verify()
            path=OUT/Path(info.name).name
            with path.open('xb') as stream:
                stream.write(raw)
            members.append(dict(name=info.name,path=str(path),size=info.size,offset=data_offset,sha256=hashlib.sha256(raw).hexdigest()))
            print('MIO source',len(members),path.name,flush=True)
        elif not info.isdir():
            raise ValueError('Unsupported tar entry')
        offset=data_offset+((info.size+511)//512)*512
    write_json(OUT/'receipt.json',dict(url=URL,etag=ETAG,archive_bytes=TOTAL,archive_fully_downloaded=False,
        archive_sha256=None,source_page='https://tcd.miovision.com/challenge/dataset.html',license='CC BY-NC-SA4.0 as stated on official page',
        downloaded_payload_bytes=transferred,ranges=ranges,members=members,skipped_test_headers=skipped_test_headers,
        boundary='Original train JPEGs only; tar header/PAX metadata. No source test pixels/labels. Source annotations not downloaded; AI labels will remain drafts.',
        training_started=False,dataset_frozen=False))
    sheet=Image.new('RGB',(1440,((len(members)+5)//6)*210),'white')
    draw=ImageDraw.Draw(sheet)
    for n,m in enumerate(members):
        with Image.open(m['path']) as im:
            im=im.convert('RGB');im.thumbnail((236,175))
            x=n%6*240;y=n//6*210
            sheet.paste(im,(x,y+25));draw.text((x+3,y+5),f'{n+1}: {Path(m["name"]).stem}',fill='black')
    sheet.save(OUT/'contact_sheet.jpg',quality=94)
    print('Saved',len(members),'train-only originals;',transferred,'bytes',flush=True)


if __name__=='__main__':
    assert allowed('MIO-TCD-Localization/train/0001.jpg')
    assert not allowed('MIO-TCD-Localization/test/0001.jpg')
    assert not allowed('MIO-TCD-Localization/train/../test/x.jpg')
    fetch()
