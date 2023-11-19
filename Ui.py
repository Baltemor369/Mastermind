import tkinter as tk
from Game import Mastermind
from Const import *

class Ui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("800x600")
        self.title("Mastermind")
        self.resizable(False,False)

        self.game = Mastermind()
        self.game.generate_code()
        self.start_row = SQUARE_SIZE
        self.start_col = W_WIDTH / 2 - SQUARE_SIZE * 2
        self.current_delta_row = 0
        self.current_delta_col = 0
        
    def Game_tab(self):
        # main window 

        # create a canva to draw colored square for the game
        self.canva = tk.Canvas(self, width=W_WIDTH, height=W_HEIGHT, bg="#999999")
        self.canva.pack()
        
        # draw color choice buttons
        for i in range(len(COLORS)):
            x = W_WIDTH*3/4 + (SQUARE_SIZE * (i%4))
            y = SQUARE_SIZE + (SQUARE_SIZE * (i//4))
            square = self.create_square(self.canva, COLORS[i], x, y)
            self.canva.tag_bind(square, '<Button-1>', lambda evt, clr=COLORS[i]:self.click_select_color(clr))

        # draw a empty row of squares
        for i in range(self.game.guess_try):
            self.draw_empty_row(self.start_col, self.start_row * (i+1))

        # button to test the code ; check it's fulfill
        self.create_button(self.canva, "Valid", W_WIDTH*3/4, SQUARE_SIZE*4, w=70, bg_color="green")

    def create_square(self, canvas:tk.Canvas, color:str, x:int, y:int, clr_outline="black"):
        square = canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=color, outline=clr_outline)
        return square

    def create_button(self, canvas: tk.Canvas, text: str, x: int, y: int, w:int=100, h:int=50, bg_color:str="white", text_color:str="black", border_color:str="black"):
        # Créer le rectangle du bouton
        button_rect = canvas.create_rectangle(x, y, x + w, y + h, fill=bg_color, outline=border_color)

        # Calculer le centre du rectangle
        center_x = (x + x + w) / 2
        center_y = (y + y + h) / 2

        # Ajouter le texte centré
        button_text = canvas.create_text(center_x, center_y, text=text, fill=text_color)

        # Associer une fonction à l'événement clic sur le bouton
        return button_rect
    
    def draw_empty_row(self, x:int , y:int):
        for i in range(4):
            square = self.create_square(self.canva,"black",x + SQUARE_SIZE*i,y,"white")
            self.canva.tag_bind(square, '<Button-1>', lambda evt, index=i, _x=x + SQUARE_SIZE*i, _y=y: self.click_select_case(index,_x,_y))
    
    def click_select_color(self, color:str):
        # graphic changes
        self.create_square(self.canva, color, self.start_col + self.current_delta_col , self.start_row + self.current_delta_row , "white")
        self.current_delta_col = (self.current_delta_col + SQUARE_SIZE)%(SQUARE_SIZE*4)

        # game data changes
        self.game.add_color(color, self.game.index)
        self.game.index = (self.game.index + 1)%4
    
    def click_select_case(self, index:int, _x:int, _y:int):
        # UI changes
        print(_x, _y, '||', self.start_col, self.start_row)
        if _y == self.start_row:
            self.current_delta_col = _x - self.start_col

            # Game changes
            self.game.set_index(index)
    
    def testing_code(self):
        # test the code in self.game
        result = self.game.check_code()
        # display the return
        # change row
        # check how many try left
        if self.game.guess_try > 0:
            pass
        pass