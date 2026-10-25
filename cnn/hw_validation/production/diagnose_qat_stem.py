"""Train-only counterfactual: isolate the changed Stem, without selecting a model."""
import json
from pathlib import Path

import numpy as np
import torch

from cnn.hw_validation.production.diagnose_trained_integer import error
from cnn.hw_validation.production.train_qat import BASE, OUT, prepare
from cnn.hw_validation.production.trained_integer import IntegerModel, load_package
from cnn.hw_validation.production.run_trained_integer import PROJECT, centered, save
from cnn.train import sha256


def main():
    torch.set_num_threads(2)
    dataset, _, _, identity, _ = prepare()
    old, old_manifest = load_package(BASE / 'package')
    new, new_manifest = load_package(OUT / 'package')
    completion = json.loads((OUT / 'independent_completion_review.json').read_text(encoding='utf-8'))
    # Both fixed-scale packages have already undergone full checkpoint/export verification.
    if new_manifest['provenance']['identity'] != identity or not completion:
        raise ValueError('candidate identity/review missing')
    name = 'stem.conv'
    models = {'QAT_G10': new}
    for variant, fields in (('restore_stem_weights', ('weights',)),
                            ('restore_stem_weights_and_bias', ('weights', 'bias'))):
        parameters = dict(new.parameters)
        parameters[name] = dict(parameters[name])
        for field in fields:
            parameters[name][field] = old.parameters[name][field]
        models[variant] = IntegerModel(new.graph, parameters, new.scales)
    cases = []
    for index in range(4):
        image, _, key = dataset[index]
        inputs = centered(image)
        reference, _, _ = old.forward(inputs)
        row = {'training_key': key, 'comparisons_to_initial_PTQ': {}}
        for variant, model in models.items():
            heads, _, _ = model.forward(inputs)
            row['comparisons_to_initial_PTQ'][variant] = [
                error(left.astype(np.float64), right.astype(np.float64))
                for left, right in zip(reference, heads, strict=True)]
        cases.append(row)
        print(f'train-only Stem counterfactual {index + 1}/4', flush=True)
    summary = {variant: [float(np.mean([
        row['comparisons_to_initial_PTQ'][variant][head]['normalized_rmse'] for row in cases]))
        for head in range(3)] for variant in models}
    save(OUT / 'stem_counterfactual.json', dict(
        scope='first four training inputs; output drift relative to initial PTQ, not accuracy',
        cases=cases, mean_head_normalized_rmse=summary,
        old_payload_sha256=old_manifest['payload_sha256'], new_payload_sha256=new_manifest['payload_sha256'],
        identity=identity, source_sha256={str(Path(__file__).relative_to(PROJECT)).replace('\\', '/'):
                                         sha256(Path(__file__))},
        optimizer_updates=0, model_exported=False, validation_used=False,
        model_selection=False, formal_acceptance=False,
        limitation='Restoring a bundle establishes its effect on output drift only; does not establish AP recovery or authorize training.'))
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
