"""Small event contract before RTL; visible/read-last are controlled external facts."""
FREE, CAPTURING, WAIT_VISIBLE, READY, READING, QUARANTINE = range(6)


def step(states, identities, event):
    states, identities = list(states), list(identities)
    active = next((i for i, state in enumerate(states) if state == CAPTURING), None)
    prior = list(states)
    outcome = None
    allocated = None
    if event.get('sof'):
        if active is not None:
            outcome = 'skipped'
        else:
            allocated = next((i for i, state in enumerate(prior) if state == FREE), None)
            outcome = 'accepted' if allocated is not None else 'skipped'
    if active is not None and event.get('frame_error'):
        states[active] = QUARANTINE
    elif active is not None and event.get('end') and not event.get('sof'):
        states[active] = WAIT_VISIBLE if event['bytes'] == 442368 else QUARANTINE
    if 'visible' in event:
        slot, identity = event['visible']
        if states[slot] == WAIT_VISIBLE and identity == identities[slot]:
            states[slot] = READY
    if 'claim' in event:
        slot, identity = event['claim']
        if prior[slot] == READY and identity == identities[slot]:
            states[slot] = READING
    if 'last_read' in event:
        slot, identity = event['last_read']
        if prior[slot] == READING and identity == identities[slot]:
            states[slot] = FREE
    if event.get('sof') and active is not None:
        states[active] = QUARANTINE
    if allocated is not None:
        states[allocated] = CAPTURING
        identities[allocated] = event['identity']
    return states, identities, outcome


def main():
    states, identities = [FREE, FREE], [None, None]
    states, identities, outcome = step(states, identities, {'sof': True, 'identity': (1, 7)})
    assert states == [CAPTURING, FREE] and outcome == 'accepted'
    states, identities, _ = step(states, identities, {'visible': (0, (1, 7))})
    assert states[0] == CAPTURING
    states, identities, _ = step(states, identities, {'end': True, 'bytes': 442368})
    assert states[0] == WAIT_VISIBLE
    states, identities, _ = step(states, identities, {'visible': (0, (1, 6))})
    assert states[0] == WAIT_VISIBLE
    states, identities, _ = step(states, identities, {'visible': (0, (1, 7))})
    states, identities, _ = step(states, identities, {'claim': (0, (1, 7))})
    assert states[0] == READING
    states, identities, _ = step(states, identities, {'sof': True, 'identity': (1, 8)})
    states, identities, _ = step(states, identities, {'end': True, 'bytes': 442368, 'visible': (1, (1, 8))})
    assert states == [READING, READY]
    states, identities, outcome = step(states, identities, {'sof': True, 'identity': (1, 9)})
    assert outcome == 'skipped' and states == [READING, READY]
    states, identities, _ = step(states, identities, {'last_read': (0, (0, 7))})
    assert states[0] == READING
    states, identities, _ = step(states, identities, {'last_read': (0, (1, 7))})
    assert states[0] == FREE
    states, identities, _ = step(states, identities, {'sof': True, 'identity': (1, 10)})
    states, identities, _ = step(states, identities, {'end': True, 'bytes': 442367})
    assert states == [QUARANTINE, READY]
    states, identities, outcome = step([CAPTURING, READING], [(2, 1), (2, 0)],
                                      {'sof': True, 'identity': (2, 2), 'last_read': (1, (2, 0))})
    assert states == [QUARANTINE, FREE] and outcome == 'skipped'
    print('SLOT_EVENT_REFERENCE_PASS', flush=True)


if __name__ == '__main__':
    main()
