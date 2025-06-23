from parse import parse_config
from state import Machine
from display import Display
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <configfile>")
        sys.exit(1)
    config = parse_config(sys.argv[1])
    machine = Machine(config["transitions"], config["init"], config["tape"])

    def step():
        machine.step()
        display.draw(machine.tape, machine.pos)
    
    print("Program chosen is " + config["name"])
    user_input = input("Display? (y/n) ")
    
    if user_input == "y" or user_input == "yes":
        display = Display(config["name"])
        display.setup_step_button(step)
        display.draw(machine.tape, machine.pos)
        display.run()
    else:
        while machine.step():
            pass
        machine.print()
    