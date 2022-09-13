#By Tiia Leinonen, in June 2018
#run: ipython battleship.py

import random

board = []

def ask_setups():
    while True:
        try:
            rows = int(input("How many rows: "))
            cols = int(input("How many columns: "))      
            if rows < 1 or cols < 1:
                print("That's not a sea, it's a puddle!")
            elif rows >= 1 and cols >= 1:  
                ships = int(input("How many ships do you want to sink: "))
                if ships >= (rows * cols):
                    print("The sea is full of ships already!")
                elif ships <= 0:
                    print("The sea is as empty as a pirate's heart.")
                else:
                    turns = int(input("How many cannonballs do you have: "))
                    break
        except ValueError:
            print("Give integers dude.")
    return(rows, cols, ships, turns)
 
    
def create_board(rows, cols):
    for x in range(rows):
        board.append(["O"] * cols)
        

def print_board(board):
    print(" # |", end=' ')                      
    for j,col in enumerate(board[0]):    
        print(str(j),end=' ')
    print()                                        #top row looks like # | 0 1 2 3 4 ...
    print("----" + len(board[0])*"--",end=' ')     # row of "--------" to separate top row from the board
    print()
    for i,row in enumerate(board):
        #print(row)  testi
        print(" " + str(i) + " | " + " ".join(row))  # adds "rownum | " before the row
        
def random_ships(rows, cols, ship_amount):
    """ Creates a list of all the possible coordinates in the board and returns random coordinates for ships to be in."""
    shipcoordinates = []
    for y in range(rows):
        for x in range(cols):               
            shipcoordinates.append((y, x)) #these x&y must be this way around!!!!
    #print(shipcoordinates)          #list of every ingle possible coordinatepair in the board
    
    coordinatepairs = random.sample(shipcoordinates, ship_amount)
    print(coordinatepairs)    
    return coordinatepairs       #looks like [(a,b), (c,d)]


if __name__ == "__main__":
    while True:
    
        rows, cols, ships, turns = ask_setups()
        create_board(rows,cols)
        coordinatepairs = random_ships(rows, cols, ships)
        #print(coordinatepairs) test
        
        for turn in range(turns):
        
            
            print(" ")
            print_board(board)
            print(" ")
            print("Turn " + str(turn + 1))   #would look weird to start from 0 here
            
            guess_row = int(input("Guess Row: "))
            guess_col = int(input("Guess Col: "))

            #first set of square brackets has the place in a list, second brackets include the coordinates 
            for i in range(0,len(coordinatepairs)):
                if (guess_row == coordinatepairs[i][0] and guess_col == coordinatepairs[i][1]):
                    print("Arrrgh! You sank my battleship!")
                    board[guess_row][guess_col] = "V"
                    coordinatepairs.pop(i)   # (x,y) of index i removed from coordinatepairs
                    #print(coordinatepairs) test
                    break    
                else:
                    continue
                
            else:   
                if guess_row not in range(rows) or guess_col not in range(cols):
                    print("Oops, that's not even in the ocean.")
                     
                elif board[guess_row][guess_col] == "X" or board[guess_row][guess_col] == "V":
                    print("You guessed that one already.")
                        
                else:
                    print("You missed my battleship!")
                    board[guess_row][guess_col] = "X"
            
            if coordinatepairs == []:
                break

        if turn == (turns-1):
            print("You ran out of cannonballs!")
            break
        if coordinatepairs == []:
            print("YYou sank everything!")
            break
               