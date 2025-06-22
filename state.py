from parse import parse_config
import sys

class Machine:
    def __init__(self, tmap, state, tape):
        self.map = tmap
        self.state = state
        self.tape = tape
        self.pos = 0 # TODO: make this configurable
    
    def run(self):
        print(self.map)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 state.py <configfile>")
        sys.exit(1)
    config = parse_config(sys.argv[1])
    Machine(config["transitions"], config["init"], config["tape"]).run()

