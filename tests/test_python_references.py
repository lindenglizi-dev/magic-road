from __future__ import annotations

import sys
import tempfile
import unittest
import csv
import json
from pathlib import Path

import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "tools"))

from candidate_chain_reference import (  # noqa: E402
    CandidateChainReference, cleanup_3x3, filter_short_runs, run_video, toward)
from convert_virat_ground import load_acceptance_receipt, parse_object_line, scene_from_clip  # noqa: E402
from import_virat_rois import import_rois, sample_rows  # noqa: E402
from single_task_protocol_model import SingleTaskProtocolModel, randomized_trial  # noqa: E402
from compare_candidate_reference_rtl import compare  # noqa: E402
from match_ccl_candidates_to_annotations import iou  # noqa: E402
from verify_blind_reserve import verify  # noqa: E402
from finalize_ccl_review import finalize  # noqa: E402
from select_candidate_windows import inclusive_iou  # noqa: E402
from evaluate_roi_padding import expanded_box  # noqa: E402
from candidate_review_io import load_reviewed  # noqa: E402
from candidate_resolution_sweep import parse_variant, source_extent_box  # noqa: E402
from candidate_temporal_sweep import parse_variant as parse_temporal_variant  # noqa: E402
from analyze_candidate_misses import expand_minimum  # noqa: E402
from render_component_miss_contexts import context_box  # noqa: E402
from audit_candidate_geometry_strata import geometry_stratum  # noqa: E402


class ViratConversionTests(unittest.TestCase):
    def test_usage_acceptance_receipt_is_explicit_and_hashed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs" / "user_acceptance_receipt.json").write_text(json.dumps({
                "accepted": True,
                "agreement_url": "https://viratdata.org/resources/VIRAT-Video-Data-Set-Protection-Agreement-1-4-11.pdf",
                "confirmation_date": "2026-09-27",
                "confirmation_source": "test_fixture",
            }), encoding="utf-8")
            receipt = load_acceptance_receipt(root)
            self.assertEqual(receipt["status"], "confirmed_by_user")
            self.assertEqual(len(receipt["receipt_sha256"]), 64)

    def test_blind_reserve_verifier_reads_hashes_only(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "video_original").mkdir()
            target = root / "video_original" / "sample.mp4"
            target.write_bytes(b"blind")
            request = {"files": [{"relative_path": "video_original/sample.mp4",
                                   "bytes": 5,
                                   "sha512": hashlib.sha512(b"blind").hexdigest()}]}
            result = verify(root, request)
            self.assertEqual(result["status"], "pass_hash_only_no_content_inspection")
            self.assertFalse(result["content_inspected"])

    def test_object_format_and_frozen_scene_identity(self):
        self.assertEqual(parse_object_line("7 10 0 100 200 20 30 1", 1),
                         (7, 10, 0, 100, 200, 20, 30, 1))
        self.assertEqual(scene_from_clip("VIRAT_S_000200_00_000100_000171"), "000200")
        with self.assertRaisesRegex(ValueError, "8 integer"):
            parse_object_line("1 2 3", 9)
        with self.assertRaisesRegex(ValueError, "invalid"):
            parse_object_line("1 2 -1 0 0 1 1 1", 2)

    def test_track_sampling_is_temporal_and_capped(self):
        rows = []
        for track in ("a", "b"):
            for frame in range(0, 200, 10):
                rows.append({"clip_id": "clip", "scene_id": "scene", "split": "train",
                             "object_id": track, "frame_index": str(frame), "label": "ped"})
        selected = sample_rows(rows, frame_stride=30, max_per_track=3, max_per_scene_label=5)
        self.assertEqual(len(selected), 5)
        by_track = {}
        for row in selected:
            by_track.setdefault(row["object_id"], []).append(int(row["frame_index"]))
        for frames in by_track.values():
            self.assertLessEqual(len(frames), 3)
            self.assertTrue(all(right - left >= 30 for left, right in zip(frames, frames[1:])))

    def test_import_refuses_to_overwrite_existing_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dataset = root / "dataset"
            dataset.mkdir()
            (dataset / "manifest.csv").write_text("existing", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "new or empty"):
                import_rois(root / "canonical", dataset, root / "output")


class CandidateReferenceTests(unittest.TestCase):
    def test_resolution_sweep_variant_and_source_extent(self):
        self.assertEqual(parse_variant("4,20,25,8"), {
            "sample_stride": 4, "threshold": 20, "min_area": 25, "top_k": 8})
        candidate = {"xmin": 1, "ymin": 2, "xmax": 3, "ymax": 4}
        self.assertEqual(source_extent_box(candidate, 4), (4, 8, 15, 19))
        edge = {"xmin": 319, "ymin": 179, "xmax": 319, "ymax": 179}
        self.assertEqual(source_extent_box(edge, 4), (1276, 716, 1279, 719))
        with self.assertRaisesRegex(ValueError, "expected"):
            parse_variant("4,20")

    def test_temporal_sweep_variant_is_explicit(self):
        self.assertEqual(parse_temporal_variant("5,12,8,4,3"), {
            "sample_stride": 5, "threshold": 12, "min_area": 8,
            "top_k": 4, "temporal_frames": 3, "dilate_iterations": 0,
            "min_neighbors": 3, "min_run": 2})
        self.assertEqual(parse_temporal_variant("5,12,8,4,3,1")["dilate_iterations"], 1)
        weakened = parse_temporal_variant("5,12,4,8,1,0,1,1")
        self.assertEqual((weakened["min_neighbors"], weakened["min_run"]), (1, 1))
        with self.assertRaisesRegex(ValueError, "expected"):
            parse_temporal_variant("5,12,8,4")

    def test_minimum_candidate_box_repair_clamps_edges(self):
        self.assertEqual(expand_minimum((10, 10, 10, 10), 4, 6, 20, 20),
                         (9, 8, 12, 13))
        self.assertEqual(expand_minimum((0, 0, 0, 0), 4, 4, 20, 20),
                         (0, 0, 3, 3))
        self.assertEqual(context_box((0, 0, 10, 10), 1280, 720),
                         (0, 0, 319, 239))
        self.assertEqual(geometry_stratum((10, 10, 39, 29)),
                         "low_aspect_h_over_w_lt_1.25")
        self.assertEqual(geometry_stratum((10, 10, 29, 49)), "upright_medium_h_40_79")
        self.assertEqual(geometry_stratum((10, 700, 29, 719)), "frame_edge_truncated")

    def test_non_deployed_stride_is_explicit_python_diagnostic(self):
        chain = CandidateChainReference(sample_stride=4)
        self.assertEqual(chain.analysis_shape, (180, 320))
        base = np.zeros((180, 320), np.uint8)
        for frame_index in range(4):
            chain.process_analysis(base.copy(), frame_index)
        changed = base.copy()
        changed[10:14, 20:24] = 20
        candidate = chain.process_analysis(changed, 4)["candidates"][0]
        self.assertEqual(candidate["source_sample_box"], [80, 40, 92, 52])

    def test_review_loader_checks_split_and_frame_provenance(self):
        import hashlib
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate_root = root / "candidates"
            frame_root = root / "frames"
            candidate_root.mkdir()
            frame_root.mkdir()
            pixels = np.asarray([[1, 2], [3, 4]], dtype=np.uint8)
            Image.fromarray(pixels, mode="L").save(candidate_root / "c0.png")
            pixel_hash = hashlib.sha256(pixels.tobytes()).hexdigest()
            fields = ["candidate_id", "replay_frame", "source_frame", "xmin", "ymin",
                      "xmax", "ymax", "geometry_class", "label", "reviewer", "roi_path",
                      "roi_sha256"]
            base = {"candidate_id": "c0", "replay_frame": "0", "source_frame": "10",
                    "xmin": "0", "ymin": "0", "xmax": "1", "ymax": "1",
                    "geometry_class": "0", "label": "", "reviewer": "",
                    "roi_path": "c0.png", "roi_sha256": pixel_hash}
            with (candidate_root / "candidates.csv").open(
                    "w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fields)
                writer.writeheader()
                writer.writerow(base)
            reviewed = candidate_root / "reviewed.csv"
            with reviewed.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fields)
                writer.writeheader()
                writer.writerow({**base, "label": "ped", "reviewer": "fixture"})
            (candidate_root / "provenance.json").write_text(json.dumps({
                "split": "val", "scene_id": "fixture", "source_sha256": "abc"}),
                encoding="utf-8")
            (frame_root / "manifest.json").write_text(json.dumps({
                "source_sha256": "abc",
                "frame_map": [{"replay_frame": 0, "source_frame": 10}]}),
                encoding="utf-8")
            rows, receipt = load_reviewed(candidate_root, reviewed, "val", frame_root)
            self.assertEqual(rows[0]["label"], "ped")
            self.assertEqual(receipt["split"], "val")
            with self.assertRaisesRegex(ValueError, "does not match"):
                load_reviewed(candidate_root, reviewed, "train", frame_root)

            with (candidate_root / "candidates.csv").open(
                    "a", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fields)
                writer.writerow({**base, "candidate_id": "c1"})
            with self.assertRaisesRegex(ValueError, "complete candidate set"):
                load_reviewed(candidate_root, reviewed, "val", frame_root)

    def test_padding_clamps_inclusive_analysis_box(self):
        self.assertEqual(expanded_box({"xmin": "1", "ymin": "2", "xmax": "254",
                                       "ymax": "143"}, 4), (0, 0, 255, 143))

    def test_window_selector_uses_inclusive_iou(self):
        self.assertEqual(inclusive_iou((0, 0, 4, 4), (0, 0, 4, 4)), 1.0)
        self.assertEqual(inclusive_iou((0, 0, 4, 4), (5, 0, 9, 4)), 0.0)

    def test_ccl_review_fails_closed_without_manual_decision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            matches = root / "matches.csv"
            with matches.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, ["candidate_id", "best_annotation_label",
                                                  "best_annotation_iou", "label", "reviewer"])
                writer.writeheader()
                writer.writerow({"candidate_id": "c0", "best_annotation_label": "vehicle",
                                 "best_annotation_iou": "0.1", "label": "", "reviewer": ""})
            decisions = root / "decisions.json"
            decisions.write_text(json.dumps({"decisions": {}}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing explicit manual decision"):
                finalize(matches, decisions)

    def test_ccl_review_preserves_ignore_and_context(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            matches = root / "matches.csv"
            with matches.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, ["candidate_id", "best_annotation_label",
                                                  "best_annotation_iou"])
                writer.writeheader()
                writer.writerow({"candidate_id": "c0", "best_annotation_label": "",
                                 "best_annotation_iou": "0"})
            decisions = root / "decisions.json"
            decisions.write_text(json.dumps({
                "review_context": {"split": "val", "boundary": "fixture boundary"},
                "decisions": {"c0": {"label": "ignore", "reviewer": "fixture",
                                         "note": "ambiguous crop"}},
            }), encoding="utf-8")
            rows, report = finalize(matches, decisions)
            self.assertEqual(rows[0]["label"], "ignore")
            self.assertEqual(report["ignored_candidate_count"], 1)
            self.assertEqual(report["metric_candidate_count"], 0)
            self.assertEqual(report["boundary"], "fixture boundary")

    def test_inclusive_candidate_annotation_iou(self):
        self.assertEqual(iou((0, 0, 1, 1), (0, 0, 1, 1)), 1.0)
        self.assertEqual(iou((0, 0, 0, 0), (1, 1, 1, 1)), 0.0)
        self.assertAlmostEqual(iou((0, 0, 1, 1), (1, 1, 2, 2)), 1 / 7)

    def test_candidate_receipt_comparison(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            summary = root / "summary.json"
            objects = root / "objects.csv"
            summary.write_text(json.dumps({
                "processed_frames": 2,
                "frames": [
                    {"frame_index": 0, "candidates": []},
                    {"frame_index": 1, "candidates": [
                        {"xmin": 1, "ymin": 2, "xmax": 3, "ymax": 4, "area": 6}]},
                ]}), encoding="utf-8")
            with objects.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, [
                    "frame", "slot", "valid", "xmin", "ymin", "xmax", "ymax", "area"])
                writer.writeheader()
                writer.writerow({"frame": 0, "slot": 0, "valid": 0,
                                 "xmin": 0, "ymin": 0, "xmax": 0, "ymax": 0, "area": 0})
                writer.writerow({"frame": 1, "slot": 0, "valid": 1,
                                 "xmin": 1, "ymin": 2, "xmax": 3, "ymax": 4, "area": 6})
            result = compare(summary, objects)
            self.assertEqual(result["status"], "pass_exact_bbox_and_area")
            self.assertEqual(result["exact_match_count"], 1)
            self.assertEqual(result["mismatch_count"], 0)

    def test_candidate_comparison_can_select_manifest_subset(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            summary = root / "summary.json"
            objects = root / "objects.csv"
            manifest = root / "manifest.json"
            summary.write_text(json.dumps({
                "processed_frames": 3,
                "frames": [
                    {"frame_index": 10, "candidates": []},
                    {"frame_index": 11, "candidates": []},
                    {"frame_index": 12, "candidates": [
                        {"xmin": 1, "ymin": 2, "xmax": 3, "ymax": 4, "area": 6}]},
                ]}), encoding="utf-8")
            manifest.write_text(json.dumps({"frame_map": [
                {"source_frame": 11, "replay_frame": 0},
                {"source_frame": 12, "replay_frame": 1},
            ]}), encoding="utf-8")
            with objects.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, [
                    "frame", "slot", "valid", "xmin", "ymin", "xmax", "ymax", "area"])
                writer.writeheader()
                writer.writerow({"frame": 0, "slot": 0, "valid": 0,
                                 "xmin": 0, "ymin": 0, "xmax": 0, "ymax": 0, "area": 0})
                writer.writerow({"frame": 1, "slot": 0, "valid": 1,
                                 "xmin": 1, "ymin": 2, "xmax": 3, "ymax": 4, "area": 6})
            result = compare(summary, objects, manifest)
            self.assertEqual(result["processed_frames"], 2)
            self.assertEqual(result["exact_match_count"], 1)

    def test_integer_toward_and_cleanup(self):
        old = np.asarray([[0, 100, 100]], dtype=np.uint8)
        new = np.asarray([[1, 116, 84]], dtype=np.uint8)
        self.assertEqual(toward(old, new, 2).tolist(), [[1, 104, 96]])
        mask = np.zeros((5, 5), np.uint8)
        mask[1:4, 1:4] = 1
        self.assertEqual(int(cleanup_3x3(mask).sum()), 9)

    def test_minimum_run_filter_precedes_components(self):
        mask = np.zeros((4, 6), np.uint8)
        mask[1, 1] = 1
        mask[2, 3:5] = 1
        filtered = filter_short_runs(mask, 2)
        self.assertEqual(int(filtered.sum()), 2)
        self.assertEqual(int(filtered[1, 1]), 0)

    def test_run_fast_paths_match_all_short_rows_without_cross_row_merging(self):
        # Exhaust every width-8 row; an independent scalar oracle also covers
        # the generic path, nonbinary input, empty width and noncontiguous views.
        rows = np.array([[(bits >> x) & 1 for x in range(8)]
                         for bits in range(256)], dtype=np.int16)
        for mask in (rows, rows[:, ::-1], rows * -7, rows[:, :1], rows[:, :0]):
            original = mask.copy()
            for minimum in (1, 2, 3, 8, 9):
                expected = np.zeros(mask.shape, dtype=np.uint8)
                for y, row in enumerate(mask):
                    start = 0
                    for x in range(len(row) + 1):
                        if x < len(row) and row[x] != 0:
                            continue
                        if x - start >= minimum:
                            expected[y, start:x] = 1
                        start = x + 1
                actual = filter_short_runs(mask, minimum)
                np.testing.assert_array_equal(actual, expected)
                self.assertEqual(actual.dtype, np.uint8)
            np.testing.assert_array_equal(mask, original)
        with self.assertRaises(ValueError):
            filter_short_runs(rows, 0)
        for minimum in (1, 2, 3):
            with self.assertRaises(ValueError):
                filter_short_runs(np.ones(8, np.uint8), minimum)

    def test_learning_threshold_frame_and_bbox_contract(self):
        chain = CandidateChainReference(min_area=16)
        base = np.zeros((144, 256), np.uint8)
        for frame in range(4):
            result = chain.process_analysis(base.copy(), frame)
            self.assertTrue(result["learning"])
            self.assertEqual(result["candidates"], [])
        changed = base.copy()
        changed[10:14, 20:24] = 20  # equality exercises RTL >= threshold
        result = chain.process_analysis(changed, 4)
        self.assertFalse(result["learning"])
        self.assertEqual(result["foreground_pixels_after_min_run"], 16)
        self.assertEqual(len(result["candidates"]), 1)
        candidate = result["candidates"][0]
        self.assertEqual([candidate[key] for key in ("xmin", "ymin", "xmax", "ymax")],
                         [20, 10, 23, 13])
        self.assertEqual(candidate["source_sample_box"], [100, 50, 115, 65])
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            chain.process_analysis(changed, 4)

    def test_deployed_update_shift_four_and_foreground_freeze(self):
        chain = CandidateChainReference()
        base = np.zeros((144, 256), np.uint8)
        for frame in range(4):
            chain.process_analysis(base.copy(), frame)
        changed = np.full_like(base, 16)
        changed[5, 5] = 20
        chain.process_analysis(changed, 4)
        self.assertEqual(int(chain.background[0, 0]), 1)
        self.assertEqual(int(chain.background[5, 5]), 0)

    def test_run_receipt_tracks_input_parameters_and_dynamic_threshold(self):
        import cv2
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            video = root / "fixture.avi"
            writer = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*"MJPG"),
                                     25.0, (1280, 720))
            self.assertTrue(writer.isOpened())
            writer.write(np.zeros((720, 1280, 3), np.uint8))
            writer.release()
            result = run_video(video, root / "out", frame_count=1, threshold=17)
            self.assertEqual(result["parameters"]["threshold"], 17)
            self.assertIn(">= 17", result["contract"]["difference"])
            self.assertEqual(len(result["video_sha256"]), 64)
            self.assertEqual(len(result["script_sha256"]), 64)
            self.assertEqual(result["parameters"]["start_frame"], 0)


class SingleTaskProtocolTests(unittest.TestCase):
    @staticmethod
    def accepted_task(model: SingleTaskProtocolModel, frame_id: int = 1):
        mutable_payload = {"objects": [1, 2]}
        model.tick(sof=(frame_id, {"capture_started": True}))
        model.tick(eof=(frame_id, mutable_payload))
        mutable_payload["objects"].append(99)
        task = model.outstanding
        for _ in range(model.request_sync_cycles):
            model.tick()
        assert model.destination_task is not None
        return task

    def test_copy_read_done_ack_and_duplicate_timing(self):
        model = SingleTaskProtocolModel()
        task = self.accepted_task(model, 3)
        self.assertEqual(model.destination_task.payload, {"objects": [1, 2]})
        self.assertEqual(model.banks[task.bank_id].state, "PUBLISHED")
        model.inject_duplicate_request(task)
        model.tick()
        self.assertEqual(model.counters["duplicate_request"], 1)
        model.destination_ram_read_done(task.transaction_id)
        self.assertIsNotNone(model.outstanding)
        # Capture into the other bank while the old task is still published.
        model.tick(sof=(4, {"capture_started": True}))
        self.assertIsNotNone(model.outstanding)
        # Read-done ack and new EOF publication occur on the same tick.  CDC
        # arrival priority releases the old bank before the new task publishes.
        model.tick(eof=(4, {"objects": []}))
        self.assertIsNotNone(model.outstanding)
        self.assertEqual(model.outstanding.frame_id, 4)
        same_cycle = [entry["event"] for entry in model.log if entry["time"] == model.time]
        self.assertEqual(same_cycle[-2:], ["source_ack_release", "source_publish"])
        self.assertEqual(model.destination_task.transaction_id, task.transaction_id)
        second = model.outstanding
        for _ in range(model.request_sync_cycles):
            model.tick()
        self.assertEqual(model.visible_request.transaction_id, second.transaction_id)
        self.assertEqual(model.destination_task.transaction_id, task.transaction_id)
        model.destination_done(task.transaction_id, {"boxes": [3]})
        self.assertEqual(model.destination_task.transaction_id, second.transaction_id)
        self.assertEqual(model.active_display, None)
        model.tick()
        model.tick(vsync=9)
        self.assertEqual(model.active_display["source_frame_id"], 3)
        self.assertEqual(model.active_display["effective_display_frame_id"], 9)
        self.assertEqual(model.active_display["frame_id_modulo_delta"], 6)
        frozen_display = dict(model.active_display)
        model.tick()
        self.assertEqual(model.active_display, frozen_display)
        model.inject_duplicate_ack(task)
        model.tick()
        self.assertEqual(model.counters["duplicate_or_stale_ack"], 1)

    def test_busy_drop_reset_and_frame_wrap(self):
        model = SingleTaskProtocolModel(frame_bits=2)
        task = self.accepted_task(model, 3)
        model.tick(sof=(0, {}))
        model.tick(eof=0)
        self.assertEqual(model.counters["publish_busy_frame_drop"], 1)
        model.tick(reset=True, sof=(1, {}), eof=1, vsync=1)
        self.assertTrue(all(bank.state == "FREE" for bank in model.banks))
        self.assertIsNone(model.outstanding)
        self.assertFalse(model.events)
        # After reset, wrapped frame zero is a normal new identity.
        model.tick(sof=(0, {"wrapped": True}))
        model.tick(eof=0)
        self.assertEqual(model.outstanding.frame_id, 0)
        self.assertNotEqual(task.frame_id, model.outstanding.frame_id)

    def test_old_ack_cannot_release_wrapped_ids_with_new_bank_generation(self):
        model = SingleTaskProtocolModel(frame_bits=1, transaction_bits=1,
                                        bank_generation_bits=3)

        def finish(frame_id: int):
            task = self.accepted_task(model, frame_id)
            model.destination_ram_read_done(task.transaction_id)
            model.destination_done(task.transaction_id, {})
            for _ in range(model.ack_sync_cycles):
                model.tick()
            return task

        first = finish(0)
        second = finish(1)
        self.assertEqual((first.bank_id, second.bank_id), (0, 1))
        model.tick(sof=(0, {}))
        model.tick(eof=0)
        wrapped = model.outstanding
        self.assertEqual((wrapped.transaction_id, wrapped.frame_id, wrapped.bank_id),
                         (first.transaction_id, first.frame_id, first.bank_id))
        self.assertNotEqual(wrapped.bank_generation, first.bank_generation)
        model.inject_duplicate_ack(first)
        model.tick()
        self.assertTrue(model.same_task(model.outstanding, wrapped))
        self.assertEqual(model.banks[wrapped.bank_id].state, "PUBLISHED")
        self.assertEqual(model.counters["duplicate_or_stale_ack"], 1)

    def test_randomized_invariants(self):
        for seed in (1, 7, 23):
            result = randomized_trial(seed, 500)
            self.assertGreater(result["event_count"], 0)
            self.assertGreater(result["counters"].get("published_task", 0), 0)


if __name__ == "__main__":
    unittest.main()
