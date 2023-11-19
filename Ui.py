import tkinter as tk
from Game import Mastermind
from Const import *

class Ui(tk.Tk):
    def __init__(self, tries:int = 10) -> None:
        super().__init__()
        self.geometry("800x600")
        self.title("Mastermind")
        self.resizable(False,False)
        self.canva = None
        self.tries = tries

    def menu(self):
        pass

    def init_data(self):
        self.game = Mastermind(self.tries)
        self.game.generate_code()
        self.start_row = SQUARE_SIZE
        self.start_col = W_WIDTH / 2 - SQUARE_SIZE * 2
        self.current_delta_row = 0
        self.current_delta_col = 0
        
    def Game_tab(self, e=None):
        print("start")
        
        self.init_data()

        
        if self.canva is None:
            print("New canva")
            # create a canva to draw colored square for the game
            self.canva = tk.Canvas(self, width=W_WIDTH, height=W_HEIGHT, bg="#999999")
            self.canva.pack()
        else:
            print("erase the canva")
            # delete all on the canva
            self.canva.delete("all")
        
        # draw color choice buttons
        for i in range(len(COLORS)):
            x = W_WIDTH*3/4 + (SQUARE_SIZE * (i%4))
            y = SQUARE_SIZE + (SQUARE_SIZE * (i//4))
            square = self.create_square(self.canva, COLORS[i], x, y,SQUARE_SIZE)
            self.canva.tag_bind(square, '<Button-1>', lambda evt, clr=COLORS[i]:self.click_select_color(clr))

        # draw a grid of empty squares
        for i in range(self.game.guess_try):
            self.draw_empty_row(self.start_col, self.start_row + i * SQUARE_SIZE)

        # button to test the code ; check it's fulfill
        button = self.create_button(self.canva, "Valid", W_WIDTH*3/4, SQUARE_SIZE*4, w=70, bg_color="green")
        self.canva.tag_bind(button[0], "<Button-1>", lambda evt: self.testing_code())
        self.canva.tag_bind(button[1], "<Button-1>", lambda evt: self.testing_code())

    def create_square(self, canvas:tk.Canvas, color:str, x:int, y:int, w:int, clr_outline="black"):
        """
        Creates a colored square on the specified canvas.

        @param canvas: The Tkinter Canvas on which the square will be drawn.
        @param color: The fill color of the square.
        @param x: The x-coordinate of the top-left corner of the square.
        @param y: The y-coordinate of the top-left corner of the square.
        @param clr_outline: The color of the square's outline (default is black).
        
        @return: The identifier of the created square on the canvas.
        """
        square = canvas.create_rectangle(x, y, x + w, y + w, fill=color, outline=clr_outline)
        return square

    def draw_empty_row(self, x:int , y:int):
        """
        Draws a horizontal row of black squares starting from the coordinates (x, y).

        @param x: Starting x-coordinate of the row.
        @param y: Starting y-coordinate of the row.
        """
        for i in range(4): 
            # For each iteration, create a black square using the create_square function
            square = self.create_square(self.canva, "black", x , y, SQUARE_SIZE, "white")
            x = x + SQUARE_SIZE

            # Bind a function to the click event on the square
            self.canva.tag_bind(square, '<Button-1>', lambda evt, index=i, _x=x, _y=y: self.click_select_index(index, _y))

    def create_button(self, canvas: tk.Canvas, text: str, x: int, y: int, w: int = 100, h: int = 50,
                    bg_color: str = "white", text_color: str = "black", border_color: str = "black"):
        """
        Creates a rectangular button on the specified canvas with customizable attributes.

        @param canvas: The Tkinter Canvas on which the button will be drawn.
        @param text: The text to be displayed on the button.
        @param x: The x-coordinate of the top-left corner of the button.
        @param y: The y-coordinate of the top-left corner of the button.
        @param w: The width of the button (default is 100).
        @param h: The height of the button (default is 50).
        @param bg_color: The background color of the button (default is "white").
        @param text_color: The color of the text on the button (default is "black").
        @param border_color: The color of the button's outline (default is "black").

        @return: The identifier of the created rectangle (button) on the canvas.
        """
        # Create the button rectangle
        button_rect = canvas.create_rectangle(x, y, x + w, y + h, fill=bg_color, outline=border_color)

        # Calculate the center of the rectangle
        center_x = (x + x + w) / 2
        center_y = (y + y + h) / 2

        # Add centered text
        button_text = canvas.create_text(center_x, center_y, text=text, fill=text_color)

        # Bind a function to the click event on the button
        return button_rect, button_text

    
    
    def click_select_color(self, color: str):
        """
        Handles the selection of a color in a game interface.

        @param color: The selected color.
        """
        # Calculate the coordinates for drawing the color square
        x = self.start_col + self.current_delta_col * SQUARE_SIZE
        y = self.start_row + self.current_delta_row * SQUARE_SIZE
        
        # Draw the color square on the canvas
        square = self.create_square(self.canva, color, x, y, SQUARE_SIZE, "white")

        # Bind a click event to the color square
        self.canva.tag_bind(square, '<Button-1>', lambda evt, i=self.game.index, _y=y: self.click_select_index(i, _y))
        
        # Update the value of current_delta_col
        self.current_delta_col =  (self.current_delta_col + 1) % 4

        # Add the selected color to the game guesser code
        self.game.add_color(color, self.game.index)

    
    def click_select_index(self, index:int, _y:int):
        if _y == self.start_row + self.current_delta_row * SQUARE_SIZE:
            self.current_delta_col = index
            self.game.index = index
    
    def testing_code(self, evt=None):
        if self.game.is_full():
            # verify the code
            result = self.game.check_code()
            # display the return
            # button with text
            button1 = self.create_button(self.canva, result[1], self.start_col - SQUARE_SIZE, self.start_row + SQUARE_SIZE * self.current_delta_row,SQUARE_SIZE, SQUARE_SIZE, bg_color="white")
            button2 = self.create_button(self.canva, result[0], self.start_col + 4*SQUARE_SIZE, self.start_row + SQUARE_SIZE * self.current_delta_row,SQUARE_SIZE, SQUARE_SIZE, bg_color="red")
            # change row
            self.current_delta_row += 1
            self.game.reset_light()
            # check how many try left
            if self.game.guess_try == 0:
                # draw the secret code
                for j in range(4):
                    self.create_square(self.canva, self.game.secret_code[j], self.start_col + SQUARE_SIZE * j, self.start_row + SQUARE_SIZE*(self.game.mem_guess_try+1), SQUARE_SIZE)
                # draw a message "Win" or "Loose"
                # end the game (reset after presing a key)
                self.bind("<KeyPress>",self.Game_tab)