import tkinter as tk
from Game import Mastermind
from Const import *

class Ui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("800x600")
        self.title("Mastermind")

        self.game = Mastermind()

    def Game_tab(self):
        self.canva = tk.Canvas(self, width=W_WIDTH, height=W_HEIGHT)
        self.canva.pack()
        
        square = self.create_square(self.canva, "blue", W_WIDTH/2 + SQUARE_SIZE * (1/2), W_HEIGHT - SQUARE_SIZE - 10)

    def create_square(self, canvas:tk.Canvas, color:str, x:int, y:int):
        square = canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=color, outline="black")
        canvas.tag_bind(square, '<Button-1>', )
        return square
    
    def click_select_color(self):
        self.game.add_color()