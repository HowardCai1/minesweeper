
# Authors: Paul Heo, David Jiang, Howard Cai
# Course: Comp Sci 123
# Instructor: Susan Fox

# This is a simple structured Minesweeper game represented in text.


import random


numOfOpened = 0
nl = []


def generateGrid():
    """This function returns a 8x8 list of dictionaries, where each dictionary has two keys. The function then print
    out the list, which is the game board."""
    innerList = []
    outerList = []
    cell = {"display": "X", "value": 0}
    for horizontal in range(8):
        for vertical in range(8):
            n = cell.copy()
            innerList.append(n)
        outerList.append(innerList)
        innerList = []
    generateMine(outerList)
    generateNumbers(outerList)
    for row in range(8):
        for col in range(8):
            print(outerList[row][col]["display"], end=" ")
        print()
    for row in range(8):
        for col in range(8):
            print(outerList[row][col]["value"], end=" ")
        print()
    return outerList

def generateMine(lst):
    """This function takes in a list, randomly selects 10 dictionaries, and change the value of the value key of
    those dictionaries to 9, which represents the mines."""
    randomLst = []
    while True:
        if len(randomLst) == 10:
            break
        n = random.randint(0,63)
        if n not in randomLst:
            randomLst.append(n)
    print(randomLst)
    for i in randomLst:
        lst[i//8][i%8]["value"] = 9

def generateANumber(lst,r,c):
    """This function takes in a list, a row value and a column value. It then loops over the surrounding cells, counts
    how many mines(9) are around that specific cell, and return the count."""
    a = 0
    if lst[r][c]["value"] == 9:
        return 9
    for row in range(r-1,r+2):
        for col in range(c-1,c+2):
            if row >= 0 and row < 8 and col >= 0 and col < 8:
                if lst[row][col]["value"] == 9:
                    a = a + 1
    return a


def generateNumbers(lst):
    """This function takes in a list. It loops through the whole list and calls the function generateANumber. As a result,
    it changes the value of the value key to the number of mines around it."""
    for row in range(8):
        for col in range(8):
            lst[row][col]["value"] = generateANumber(lst, row, col)


def countOpen(lst):
    """This function takes in a list and is keeping track of how many cells are open. The value of numOfOpened determines
     if the user wins the game."""
    global numOfOpened
    numOfOpened = 0
    for row in range(8):
        for col in range(8):
            if lst[row][col]["display"] == lst[row][col]["value"]:
                numOfOpened += 1

def openZero(lst, r, c):
    """This function takes in a list, a row value and a column value. It is called when the user opens a cell whose value
    is 0. The function then open all the surround cells of the zero cell, and check if any zeros are opened. If it does,
    the function keeps repeating the same procedures until no more new zeros are opened."""
    l = []
    global nl
    global numOfOpened
    nl.append((r, c))
    for row in range(r-1, r+2):
        for col in range(c-1, c+2):
            if (row, col) not in nl:
                l.append((row, col))
    if lst[r][c]["value"] != 0:
        lst[r][c]["display"] = lst[r][c]["value"]
    else:
        for (x, y) in l:
            if 0 <= x < 8 and 0 <= y < 8:

                if lst[x][y]["value"] == 0:
                    openZero(lst, x, y)
                if lst[x][y]["value"] != 9:
                    lst[x][y]["display"] = lst[x][y]["value"]



def uncoverInput():
    """This function asks the users to input row and column coordinates that they want to open/flag/unflag. It then retruns
    the row and column values that the user inputs."""
    strInput = input("Type in row and column coordinates as row column (e.g 13 means the cell in row one, column three).")
    lst = ["1","2","3", "4", "5", "6","7", "8"]
    if len(strInput) == 2 and strInput[0] in lst and strInput[1] in lst:
        rowNum = int(strInput[0]) - 1
        colNum = int(strInput[1]) - 1
        return rowNum, colNum
    else:
        print("Invalid input")
        return uncoverInput()


def actionInput(lst,row,col):
    """This function takes in a list, a row value and a column value, and it asks the users if they want to open, flag,
    or unflag a specific cell. The list will change based on the three inputs."""
    strInput = input("Do you want to open, flag, or unflag this cell? (O, F or U)")
    if strInput.upper() == "O":
        lst[row][col]["display"] = lst[row][col]["value"]
        openZero(lst, row, col)
    elif strInput.upper() == "F":
        lst[row][col]["display"] = "F"
    elif lst[row][col]["display"] == "F" and strInput.upper() == "U":
        lst[row][col]["display"] = "X"
    else:
        print("Invalid input!")



def updateGrid(lst,r,c):
    """This function takes in a list, a row value and a column value. It calls the actionInput function, then
     return and print out the modified list."""
    actionInput(lst,r,c)
    for row in range(8):
        for col in range(8):
            print(lst[row][col]["display"], end=" ")
        print()
    return lst


def checkEnd(lst,row,col):
    """This function takes in a list, a row value and a column value. It checks if the game is over: Either the users open
     a mine(Lose), or they successfully open 54 cells without opening a mine(Win)."""
    global numOfOpened
    if lst[row][col]["value"] == 9 and lst[row][col]["display"]!= "F":
        end = True
        print("You opened a mine! Gameover!")
        return end
    elif numOfOpened == 54:
        end  = True
        print("Congratulations!")
        return end



def main():
    """This is the main function of the program. It first calls generateGrid to generate the game board, then it uses a
    while loop to keep asking for the user's input and updates the list accordingly. The while loop break when checkEnd
    is true."""
    lst = generateGrid()
    global numOfOpened
    while True:
        row, col = uncoverInput()
        lst = updateGrid(lst,row,col)
        countOpen(lst)
        print(numOfOpened)
        if checkEnd(lst,row,col):
            break




main()
