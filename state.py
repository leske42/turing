from parse import parse_config
import sys

class Machine:
    def __init__(self, tmap, state, tape):
        self.map = tmap
        self.state = state
        self.tape = tape
        self.pos = 0 # TODO: make this configurable
    
    def step(self):
        if self.pos < 0:
            self.tape.insert(0, '_')
            self.pos = 0
        elif self.pos >= len(self.tape):
            self.tape.append('_')
        if self.state not in self.map or self.tape[self.pos] not in self.map[self.state]:
            #print("position: " + self.state + " character: " + self.tape[self.pos])
            return False
        to_state, write_symbol, mov = self.map[self.state][self.tape[self.pos]]
        self.state = to_state
        self.tape[self.pos] = write_symbol
        self.pos += -1 if mov == "LEFT" else (1 if mov == "RIGHT" else 0)
        return True

    def print(self):
        print("OUTPUT: " + ' '.join(self.tape))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 state.py <configfile>")
        sys.exit(1)
    config = parse_config(sys.argv[1])
    Machine(config["transitions"], config["init"], config["tape"]).run()
