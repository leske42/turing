import re
import sys
import string

__all__ = ["parse_config"]

class ParseError(Exception):
    pass

def valid_symbol(token):
    return ((len(token) == 1 and token in string.printable))

def valid_state(token):
    state_pattern = re.compile(r'^[a-z0-9_]+$')
    return (state_pattern.match(token))

def validate(tokens, line):

    if (len(tokens) == 10
        and tokens[0] == "IF"
        and tokens[2] == "FROM"
        and tokens[4] == "TO"
        and tokens[6] == "WRITE"
        and tokens[8] == "MOVE"
        and tokens[9] in ("LEFT", "RIGHT", "HALT")
    ):
        if not (valid_symbol(tokens[1]) and valid_symbol(tokens[7])):
            raise ParseError(f"Invalid symbol in transition: {line}")
        if not (valid_state(tokens[3]) and valid_state(tokens[5])):
            raise ParseError(f"Invalid state in transition: {line}")  
        return

    raise ParseError(f"Invalid keyword in transition: {line}")

def check_sets(read_symbol, from_state, to_state, write_symbol, symbols, states):

    if from_state not in states:
        raise ParseError(f"Unknown state in transition: {from_state}")
    if to_state not in states:
        raise ParseError(f"Unknown state in transition: {to_state}")
    if read_symbol not in symbols:
        raise ParseError(f"Unknown symbol in transition: {read_symbol}")
    if write_symbol not in symbols:
        raise ParseError(f"Unknown symbol in transition: {write_symbol}")

def fill_dict(lines, states, symbols):

    transitions = {}

    for line in lines:
        tokens = line.split()      
        validate(tokens, line)

        _, read_symbol, _, from_state, _, to_state, _, write_symbol, _, mov = tokens
        check_sets(read_symbol, from_state, to_state, write_symbol, symbols, states)

        if from_state not in transitions:
            transitions[from_state] = {}
        if read_symbol in transitions[from_state]:
            raise ParseError(f"Duplicate transition for ({from_state}, {read_symbol})")
        transitions[from_state][read_symbol] = (to_state, write_symbol, mov)

    return transitions

def create_symbols(line):
    symbols = line.split()[2:]
    for symbol in symbols:
        if not valid_symbol(symbol):
            raise ParseError(f"Invalid symbol in VALID SYMBOLS: {symbol}")
    return set(symbols)

def create_states(line):
    states = line.split()[2:]
    for state in states:
        if not valid_state(state):
            raise ParseError(f"Invalid state in VALID STATES: {state}")
    return set(states)


def parse_config(filename):

    name = None

    with open(filename, 'r') as f:
        lines = f.readlines()
    def clean(line):
        return re.sub(r'#.*', '', line).strip()
    lines = [clean(line) for line in lines]
    lines = [line for line in lines if line]

    if len(lines) < 5:
        raise ParseError("Config must contain NAME, VALID SYMBOLS, TAPE, VALID STATES and START STATE")

    symbols = create_symbols(lines[1])
    states = create_states(lines[3])

    return {
        "name": lines[0],
        "tape" : lines[2].split()[1:],
        "symbols": symbols,
        "states": states,
        "init": re.sub(r'^\s*START STATE:\s*', '', lines[4]).strip(),
        "transitions": fill_dict(lines[5:], states, symbols)
    }
#TODO: validate NAME, validate first 2 word of symbols and states, lines[4] etc.

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse.py <configfile>")
        sys.exit(1)
    config = parse_config(sys.argv[1])
    print(config)