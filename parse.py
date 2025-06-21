import re
import sys

class ParseError(Exception):
    pass

def fill_dict(lines, states, symbols):

    transitions = {}

    for line in lines:
        tokens = line.split()
        if len(tokens) != 10 or tokens[0] != "IF" or tokens[2] != "FROM" or tokens[4] != "TO" or tokens[6] != "WRITE" or tokens[8] != "MOVE" or tokens[9] not in ("LEFT", "RIGHT", "HALT"):
            raise ParseError(f"Invalid transition line: {line}")
        _, read_symbol, _, from_state, _, to_state, _, write_symbol, _, mov = tokens

        if from_state not in states:
            raise ParseError(f"Unknown state in transition: {from_state}")
        if to_state not in states:
            raise ParseError(f"Unknown state in transition: {to_state}")
        if read_symbol not in symbols:
            raise ParseError(f"Unknown symbol in transition: {read_symbol}")
        if write_symbol not in symbols:
            raise ParseError(f"Unknown symbol in transition: {write_symbol}")

        if from_state not in transitions:
            transitions[from_state] = {}
        if read_symbol in transitions[from_state]:
            raise ParseError(f"Duplicate transition for ({from_state}, {read_symbol})")
        transitions[from_state][read_symbol] = (to_state, write_symbol, mov)

    return transitions

def parse_config(filename):

    name = None
    symbols = set()
    states = set()

    with open(filename, 'r') as f:
        lines = f.readlines()

    def clean(line):
        return re.sub(r'#.*', '', line).strip()

    lines = [clean(line) for line in lines]
    lines = [line for line in lines if line]

    if len(lines) < 3:
        raise ParseError("Config must contain at least NAME, VALID SYMBOLS and VALID STATES")

    name = lines[0]
    symbols = lines[1].split()
    symbols = set(symbols[2:])
    states = lines[2].split()
    states = set(states[2:])

    return {
        "name": name,
        "symbols": symbols,
        "states": states,
        "transitions": fill_dict(lines[3:], states, symbols)
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse.py <configfile>")
        sys.exit(1)
    config = parse_config(sys.argv[1])
    print(config)