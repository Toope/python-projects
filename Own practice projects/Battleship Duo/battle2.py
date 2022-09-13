#By Tiia Leinonen
#run: ipython battle2.py

import random
import time

class Error(Exception):
   """Base class for my own exceptions."""
   pass
   
class DoubleError(Error):
    """Raised when user tries to set many ships into one spot or guess the same spot multiple times."""
    pass

#state variables used in game statistics, easy to retrive from here
state = {
    "timestamp": None,
    "gameover": False,
    "turn": 1,
    "rows": None,
    "cols": None,
    "ships": None
}

#boards are global variables
board = []
board2 = [] 


def ask_setups():
    """ Asks the settings for the game, board size and the amount of the ships. """
    while True:
        try:
            rows = int(input("How many rows: "))
            cols = int(input("How many columns: "))      
            if rows < 2 or cols < 2:
                print("That's not a sea, it's a puddle!")
            elif rows >= 2 and cols >= 2: 
                while True:                   #inner while true loop so that if you mess up your ship amount you don't have to set the board again
                    try:
                        ships = int(input("How many ships do you have: "))
                        if ships >= (rows * cols):
                            print("The sea is full of ships already!")
                        elif ships <= 0:
                            print("It's so lonely out here...")
                        else:
                            print("")
                            break
                    except ValueError:
                        print("Give integers dude.")
                break
        except ValueError:
            print("Give integers dude.")
    #save the values in state
    state["rows"] = rows
    state["cols"] = cols
    state["ships"] = ships
 
    
def create_board(board):
    """ Creates the board. """
    for x in range(state["rows"]):
        board.append(["O"] * state["cols"])
        

def print_board(board):
    """ Prints the board and row- and column-numbers on top and on the left side of the board. """
    print(" # |", end=' ')                      
    for j,col in enumerate(board[0]):    
        print(str(j),end=' ')
    print()                                        #top row looks like # | 0 1 2 3 4 ...
    print("---+" + len(board[0])*"--",end=' ')     # row of "--------" to separate top row from the board
    print()
    for i,row in enumerate(board):
        print(" " + str(i) + " | " + " ".join(row))  # adds "rownum | " before the row
        

def set_ships():
    """ Set coordinates for your ships by yourself."""
    shipcoordinates = []
    for ship in range(state["ships"]):
        while True:                                    #gives mercy if you try to set coordinates outside the board
            try:                                     
                print("Ship #" + str(ship) + ":")
                y = int(input("Give row: "))
                x = int(input("Give col: "))      
                if x < 0 or y < 0 or x >(state["cols"]-1) or y > (state["cols"]-1):
                    print("Not in the board, try again!")
                elif y >= 0 and y < state["cols"] and x >= 0 and x < state["rows"]:  
                    for coord in shipcoordinates:
                        if coord ==(y,x):
                            raise DoubleError   #my own error for handling multiple ships in one spot
                        else:
                            pass
                    shipcoordinates.append((y,x))
                    break
            except ValueError:
                print("Give integers dude.")  
            except DoubleError:
                print("You can't put many ships in one spot.")
                  
    return shipcoordinates         #looks like [(a,b), (c,d)]
    
def turns(): 
    """Basic game loop. Guessing the coordinates in turns."""
    while state["gameover"] != True:   
        if state["turn"] % 2 == 1:  #player 1's turn
            print("\nPlayer 1, time to sink player 2's boats! ")
            list_in_use = coordinatepairs2
            board_in_use = board2
        elif state["turn"] % 2 == 0: #player 2's turn
            print("\nPlayer 2, time to sink player 1's boats!")       
            list_in_use = coordinatepairs
            board_in_use = board
            
        print_board(board_in_use)
        
        while True:
            try:
                guess_row = int(input("Guess Row: "))
                guess_col = int(input("Guess Col: "))
                #for-else structure here: if coordinates found, else does not execute and vice versa
                for i in range(0,len(list_in_use)):
                    if (guess_row == list_in_use[i][0] and guess_col == list_in_use[i][1]):
                        print("Arrrgh! You sank the battleship!")
                        board_in_use[guess_row][guess_col] = "X"
                        list_in_use.pop(i)   # pair(x,y) of index i removed from coordinatepairs
                        break    
                    else:
                        continue
                else:       
                    if guess_row not in range(state["rows"]) or guess_col not in range(state["cols"]): 
                        raise LookupError            
                    elif board_in_use[guess_row][guess_col] == "M" or board_in_use[guess_row][guess_col] == "X":
                        raise DoubleError
                    else:
                        print("You missed the battleship!")
                        board_in_use[guess_row][guess_col] = "M"
                break
            except ValueError:
                print("Give integers, dude.")
            except LookupError:
                print("Oops, that's not even in the ocean.") 
            except DoubleError:
                print("You guessed that one already.")
                                    
        if list_in_use == []:
            break
           
        state["turn"] += 1 
  

def save_stats(stats):
    """Saving the game statistics in a file."""
    try:
        with open(stats, "a") as target:
            target.write("{},{},{},{},{}\n".format(state["timestamp"], state["turn"], state["rows"], state["cols"], state["ships"]))          
    except IOError:
        pass
        
        
def read_stats(stats):
    """Reading the game statistics from the file."""
    try:
        with open(stats) as source:
            for line in source.readlines():
                info = line.strip("\n").split(",")
                print("{}\nGame lasted: {} turns.\nField size: {} x {}.\nShips: {}.\n".format(info[0], info[1], info[2], info[3], info[4]))               
    except IOError:
        print("No stats yet. Play a game first.")
                

if __name__ == "__main__":
    
    while True:
        print(" ")
        print("Welcome to battleship!")
        print("G = new game\nS = statistics\nQ = quit\n")
        choice = input("Your choice: ").upper()
        if choice == "G":
            while True:
                state["timestamp"] = time.strftime("%d.%m.%Y - %H.%M", time.localtime())
                print("Choose your settings.")
                ask_setups()             #ask the size of the board, ship number etc. for both boards
                #player 1
                create_board(board)
                print("Player one, set your ships:")
                coordinatepairs = set_ships()           
                #player2       
                create_board(board2)
                print(" ")
                print("Player two, set your ships:")
                coordinatepairs2 = set_ships() 
                turns()                
                if coordinatepairs == [] or coordinatepairs2 == []:
                    print("You sank everything!")
                    print("GAME OVER!")
                    state["gameover"] == 1
                    save_stats("stats.txt")
                    break
        elif choice == "S":
            read_stats("stats.txt")
        elif choice == "Q":
            break
        else:
            print("Invalid input.")
             
        