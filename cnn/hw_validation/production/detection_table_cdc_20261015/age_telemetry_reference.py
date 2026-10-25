"""SRIF1 invalid age is UNKNOWN, never a falsely fresh zero milliseconds."""
UINT64_MAX = (1 << 64) - 1


def age_upper(active, time_valid, epoch, time_epoch, capture, completion, now):
    if not active or not time_valid or epoch != time_epoch or not capture <= completion <= now:
        return UINT64_MAX
    return min(now - capture + 4, UINT64_MAX)


def main():
    assert age_upper(True, True, 1, 1, 100, 110, 596) == 500
    assert age_upper(True, True, 1, 1, 100, 110, 597) == 501
    assert age_upper(False, True, 1, 1, 100, 110, 120) == UINT64_MAX
    assert age_upper(True, False, 1, 1, 100, 110, 120) == UINT64_MAX
    assert age_upper(True, True, 1, 2, 100, 110, 120) == UINT64_MAX
    assert age_upper(True, True, 1, 1, 121, 121, 120) == UINT64_MAX
    assert age_upper(True, True, 1, 1, 111, 110, 120) == UINT64_MAX
    assert age_upper(True, True, 1, 1, 100, 121, 120) == UINT64_MAX
    assert age_upper(True, True, 1, 1, 0, 1, UINT64_MAX) == UINT64_MAX
    assert age_upper(True, True, 1, 1, UINT64_MAX - 2, UINT64_MAX - 1, UINT64_MAX) == 6
    print('AGE_TELEMETRY_PASS invalid=UINT64_MAX, valid_age=delta+4, overflow=saturate')


if __name__ == '__main__':
    main()
