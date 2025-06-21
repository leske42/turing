import tkinter as tk

CELL_SIZE = 40
VIEW_WIDTH = 21
TAPE_HEIGHT = 60

class Display:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Turing Machine")

        self.canvas = tk.Canvas(self.root, width=CELL_SIZE * VIEW_WIDTH, height=TAPE_HEIGHT)

        self.right_button = tk.Button(self.root, text="Step →", command=self.stepr)
        self.left_button = tk.Button(self.root, text="← Step", command=self.stepl)
        self.print_button = tk.Button(self.root, text="PRINT", command=self.print)

        self.canvas.grid(row=0, column=0, columnspan=VIEW_WIDTH)
        self.print_button.grid(row=1, column=VIEW_WIDTH // 2, sticky="ns")
        self.left_button.grid(row=1, column=VIEW_WIDTH // 2 - 1, sticky="w")
        self.right_button.grid(row=1, column=VIEW_WIDTH // 2 + 1, sticky="e")

        self.tape = {}
        self.tape[5] = '1'
        self.tape[-5] = '1'
        self.head = 0

        self.draw()

    def stepr(self):
        self.head += 1
        self.draw()

    def stepl(self):
        self.head -= 1
        self.draw()
    
    def print(self):
        self.tape[self.head] = 'X'
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        start = self.head - VIEW_WIDTH // 2
        end = self.head + VIEW_WIDTH // 2 + 1

        for i, pos in enumerate(range(start, end)):
            symbol = self.tape.get(pos, '_')
            x = i * CELL_SIZE
            self.canvas.create_rectangle(x, 0, x + CELL_SIZE, TAPE_HEIGHT, outline="black", fill="wheat")
            self.canvas.create_text(x + CELL_SIZE // 2, TAPE_HEIGHT // 2, text=symbol)

            if pos == self.head:
                self.canvas.create_rectangle(x, 0, x + CELL_SIZE, TAPE_HEIGHT, outline="green", width=3)

    def run(self):
        self.root.mainloop()

Display().run()