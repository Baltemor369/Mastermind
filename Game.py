import random as rd
from Const import *

class Mastermind:

    def __init__(self, guess_try:int=10) -> None:
        self.secret_code:list[str] = []     # code à deviner
        self.guest_code:list[str] = [0,0,0,0]      # code essayer
        self.guess_try:int = guess_try      # nombre d'essaies restant
        self.mem_guess_try = guess_try      # utile pour le reset
        self.index = 0                      # index d'affection color
        self.right_place:int = 0            # color juste
        self.wrong_place:int = 0            # color mal placé
    
    def check_code(self):
        secret_code = self.secret_code.copy()
        try_code = self.guest_code.copy()

        self.right_place = 0
        self.wrong_place = 0

        for i,elt in enumerate(try_code):
            if elt == secret_code[i]:
                self.right_place += 1
                secret_code[i] = "E"
            elif elt in secret_code:
                self.wrong_place += 1
                secret_code[secret_code.index(elt)] = "E"
        
        self.guess_try -= 1
        
        return (self.right_place,self.wrong_place)
    
    def generate_code(self):
        for i in range(4):
            self.secret_code.append(rd.choice(COLORS))
        
    def reset(self):
        self.guess_try += self.mem_guess_try
        self.secret_code = ""
        self.guest_code = ""
        self.right_place = 0
        self.wrong_place = 0
    
    def set_index(self, index:int):
        self.index = index

    def add_color(self, color:str, index:int):
        self.guest_code[index] = color
        self.index = (index + 1) % 4