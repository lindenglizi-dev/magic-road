"""Fixed, manifest-pinned 11 new + 11 replay samples per update."""
import hashlib
import json

from torch.utils.data import Dataset


class ReplayWindow(Dataset):
    """Keep the existing trainer's 22-sample epoch and resume cursors unchanged."""

    def __init__(self, dataset, sampling, epochs):
        if (not isinstance(sampling, dict)
                or set(sampling) != {'kind', 'orders'}
                or sampling['kind'] != 'balanced_replay_11_plus_11_v1'):
            raise ValueError('unsupported replay sampling contract')
        orders = sampling['orders']
        if not isinstance(orders, list) or len(orders) != epochs:
            raise ValueError('replay schedule must cover exactly the planned epochs')
        groups = [row.get('sampling_group') for row in dataset.rows]
        if len(groups) != len(dataset) or any(g not in ('new', 'replay') for g in groups):
            raise ValueError('every training row needs a new/replay group')
        for order in orders:
            if (not isinstance(order, list) or len(order) != 22
                    or any(type(i) is not int or not 0 <= i < len(dataset) for i in order)
                    or len(set(order)) != 22
                    or sum(groups[i] == 'new' for i in order) != 11):
                raise ValueError('each replay window must contain 11 distinct samples per domain')
        if set(i for order in orders for i in order) != set(range(len(dataset))):
            raise ValueError('the frozen schedule must expose every selected training sample')
        self.dataset = dataset
        self.orders = tuple(tuple(order) for order in orders)
        self.epoch = 0
        self.sampling_sha256 = hashlib.sha256(json.dumps(
            sampling, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

    def __len__(self):
        return 22

    def set_epoch(self, epoch, mosaic=None):
        if type(epoch) is not int or not 0 <= epoch < len(self.orders) or mosaic:
            raise ValueError('invalid replay epoch or Mosaic requested')
        self.epoch = epoch
        self.dataset.set_epoch(epoch, mosaic=False)

    def __getitem__(self, index):
        if not 0 <= index < len(self):
            raise IndexError(index)
        return self.dataset[self.orders[self.epoch][index]]
