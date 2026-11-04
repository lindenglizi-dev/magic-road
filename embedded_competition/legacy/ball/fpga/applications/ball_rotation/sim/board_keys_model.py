"""板载键行为约定：前两键互斥短/长动作，档位按事件循环。"""

EXPOSURES = (1991, 480, 240, 120)
GAINS = (144, 176, 80, 112)


def action(key, held_clocks, threshold):
    if key < 2:
        return ("camera", key) if held_clocks >= threshold else ("application", key)
    return "application", key


if __name__ == "__main__":
    for key in range(2):
        assert action(key, 31, 32) == ("application", key)
        assert action(key, 32, 32) == ("camera", key)
        assert action(key, 320, 32) == ("camera", key)
    assert [EXPOSURES[index % 4] for index in range(5)] == [1991, 480, 240, 120, 1991]
    assert [GAINS[index % 4] for index in range(5)] == [144, 176, 80, 112, 144]
    print("PASS board-key intent: mutually exclusive short/long actions and profile wrap")
