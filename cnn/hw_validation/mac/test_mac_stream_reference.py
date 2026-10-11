import unittest

from mac_reference import Beat
from mac_stream_reference import (
    OP_ACTIVATION,
    OP_BIAS,
    OP_CONTROL,
    OP_WEIGHT,
    commands_for_beat,
    dynamic_resource_probe_beat,
)


class MacStreamReferenceTest(unittest.TestCase):
    def test_fixed_transaction_layout_reconstructs_all_payload_bits(self) -> None:
        beat = dynamic_resource_probe_beat()
        commands = commands_for_beat(beat)
        self.assertEqual(len(commands), 12)
        self.assertEqual([command.opcode for command in commands], [OP_ACTIVATION] * 2 + [OP_WEIGHT] * 6 + [OP_BIAS] * 3 + [OP_CONTROL])
        activation = sum(command.data << (32 * command.index) for command in commands if command.opcode == OP_ACTIVATION)
        weights = sum(command.data << (32 * command.index) for command in commands if command.opcode == OP_WEIGHT)
        biases = sum(command.data << (32 * command.index) for command in commands if command.opcode == OP_BIAS)
        self.assertEqual(activation, sum((value & 0xFF) << (8 * index) for index, value in enumerate(beat.activations)))
        flattened_weights = tuple(value for row in beat.weights for value in row)
        self.assertEqual(weights, sum((value & 0xFF) << (8 * index) for index, value in enumerate(flattened_weights)))
        self.assertEqual(biases, sum((value & 0xFFFFFFFF) << (32 * index) for index, value in enumerate(beat.biases)))
        self.assertEqual(commands[-1].data, 0x3FF)

    def test_every_multiplier_operand_is_runtime_variable(self) -> None:
        beat = dynamic_resource_probe_beat()
        self.assertEqual(len(set(beat.activations)), 8)
        flattened_weights = tuple(value for row in beat.weights for value in row)
        self.assertEqual(len(flattened_weights), 24)
        self.assertEqual(len(set(flattened_weights)), 24)
        self.assertNotIn(0, flattened_weights)

    def test_control_word_carries_only_mask_first_and_last(self) -> None:
        beat = Beat(False, True, 0x81, (0,) * 8, ((0,) * 8,) * 3, (0, 0, 0))
        control = commands_for_beat(beat)[-1]
        self.assertEqual((control.opcode, control.index, control.data), (OP_CONTROL, 0, 0x281))


if __name__ == "__main__":
    unittest.main()
