def print_jflap_head():
    print('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    print('<structure>\n  <type>fa</type>\n  <automaton>')


def print_jflap_state(state_id, x, y, is_initial, is_final):
    print(f'    <state id="{state_id}" name="q{state_id}">')
    print(f'      <x>{x}</x>')
    print(f'      <y>{y}</y>')

    if is_initial:
        print('      <initial/>')
    if is_final:
        print('      <final/>')

    print('    </state>')


def print_jflap_transition(from_id, to_id, symbol):
    print('    <transition>')
    print(f'      <from>{from_id}</from>')
    print(f'      <to>{to_id}</to>')
    if symbol:
        print(f'      <read>{symbol}</read>')
    print('    </transition>')


def print_jflap_tail():
    print('  </automaton>\n</structure>')


DIST_SCALE_HOR = 200
DIST_SCALE_VERT = 600


def main():

    print("Enter text:")
    userinput = []

    while True:
        line = input().strip()
        if line == "":
            break

        userinput.append(line)

    print()
    print_jflap_head()

    curr_id = 1
    curr_height = 0
    transitions_of_state = {}
    info_of_state = {}
    transitions = []

    for line in userinput:
        line_len = len(line)

        if line_len == 0:
            continue

        prev_state = 0

        for i in range(line_len):
            symbol = line[i]

            if not symbol.islower():
                print(f"Symbol '{symbol}' is invalid. Only lowercase a-z allowed.")
                return

            if (prev_state, symbol) in transitions_of_state:
                next_state = transitions_of_state[(prev_state, symbol)]
            else:
                if curr_id not in info_of_state:
                    info_of_state[curr_id] = {'x': i * DIST_SCALE_HOR, 'y': curr_height, 'is_final': False, 'is_initial': False}

                transitions_of_state[(prev_state, symbol)] = curr_id
                transitions.append((prev_state, curr_id, symbol))

                next_state = curr_id
                curr_id += 1

            prev_state = next_state

        if prev_state in info_of_state:
            info_of_state[prev_state]['is_final'] = True

        curr_id += DIST_SCALE_VERT

    if 0 not in info_of_state:
        info_of_state[0] = {'x': -2 * DIST_SCALE_HOR, 'y': (curr_height - DIST_SCALE_VERT) // 2 + 3120, 'is_initial': True, 'is_final': True}
    else:
        info_of_state[0]['is_initial'] = True

    for state_id, info in info_of_state.items():
        print_jflap_state(state_id, info['x'], info['y'], info['is_initial'], info['is_final'])

    for from_id, to_id, symbol in transitions:
        print_jflap_transition(from_id, to_id, symbol)

    print_jflap_tail()


if __name__ == "__main__":
    main()
