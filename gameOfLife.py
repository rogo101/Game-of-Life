import numpy as np
import os
import time

class GameOfLife():
    board = None

    prevPrintedLength = None

    def __init__(self, boardDim):
        self.board = np.zeros(boardDim)

    def setInitialConfig(self, config):
        for i in config:
            self.board[i[0], i[1]] = 1

    def calculateNewBoard(self):
        # Extend axis ordered as follow: should extend row 0, row n - 1, column 0, column n - 1
        extendAxis = np.array([False, False, False, False])

        currDims = self.getBoardDims()
        rowsWithOne, columnsWithOne = self.board.any(axis = 1), self.board.any(axis = 0)
        if rowsWithOne[0]:
            extendAxis[0] = True
        if rowsWithOne[currDims[0] - 1]:
            extendAxis[1] = True
        if columnsWithOne[0]:
            extendAxis[2] = True
        if columnsWithOne[currDims[1] - 1]:
            extendAxis[3] = True

        if not extendAxis.any():
            return
        else:
            newRows = currDims[0] + np.count_nonzero(extendAxis[:2] == True)
            newCols = currDims[1] + np.count_nonzero(extendAxis[2:] == True)
            newBoard = np.zeros((newRows, newCols))
            rowOffset = 1 if extendAxis[0] else 0
            colOffset = 1 if extendAxis[2] else 0
            for i in range(self.board.shape[0]):
                for j in range(self.board.shape[1]):
                    newBoard[i + rowOffset, j + colOffset] = self.board[i, j]
            self.board = newBoard.copy()

    def getBoardDims(self):
        return self.board.shape

    def isAlive(self, i, j):
        return self.board[i, j] == 1

    def getNumAliveNeighbors(self, i, j):
        numAliveNeighbors = 0
        boardDims = self.getBoardDims()
        highestI, highestJ = boardDims[0] - 1, boardDims[1] - 1

        if i != 0:
            if self.isAlive(i- 1, j):
                numAliveNeighbors += 1
        if j != 0:
            if self.isAlive(i, j - 1):
                numAliveNeighbors += 1
        if i != highestI:
            if self.isAlive(i + 1, j):
                numAliveNeighbors += 1
        if j != highestJ:
            if self.isAlive(i, j + 1):
                numAliveNeighbors += 1
        if i != 0 and j != 0:
            if self.isAlive(i - 1, j - 1):
                numAliveNeighbors += 1
        if i != 0 and j != highestJ:
            if self.isAlive(i - 1, j + 1):
                numAliveNeighbors += 1
        if i != highestI and j != 0:
            if self.isAlive(i + 1, j - 1):
                numAliveNeighbors += 1
        if i != highestI and j != highestJ:
            if self.isAlive(i + 1, j + 1):
                numAliveNeighbors += 1

        return numAliveNeighbors

    def runGame(self, iterations = -1, title = "Game of Life"):
        numIterations = -1
        while True:
            numIterations += 1

            # Print current board and wait a bit
            self.printBoard(title)
            time.sleep(0.5)

            # Logic for iterations parameter if passed
            if iterations >= 0:
                if numIterations >= iterations:
                    break

            # Determine if current board needs to be extended and if so extend the board by 1
            self.calculateNewBoard()

            # Calculate next board state for each element in the current board
            newBoard = self.board.copy()
            for i in range(self.board.shape[0]):
                for j in range(self.board.shape[1]):
                    isAlive = self.isAlive(i, j)
                    numAliveNeighbors = self.getNumAliveNeighbors(i, j)
                    if isAlive:
                        if numAliveNeighbors < 2:
                            newBoard[i, j] = 0
                        elif numAliveNeighbors > 3:
                            newBoard[i, j] = 0
                    else:
                        if numAliveNeighbors == 3:
                            newBoard[i, j] = 1

            # Next board state is now the current board state
            self.board = newBoard

    # Fuck comments for this, just shit I had to do for it to print properly and forgot how it works
    def printBoard(self, title = None): 
        if self.prevPrintedLength:
            os.write(1, str.encode(f"\x1b[{self.prevPrintedLength}F"))
        self.prevPrintedLength = 0
        if title: 
            print(title)
            self.prevPrintedLength += 1
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i, j] == 0:
                    unicodeBlockCharacterCode='\u2588'
                    print(f"{unicodeBlockCharacterCode}", end = "")
                else:
                    greenANSIEscapeSeq='\033[92m'
                    ANSIEndSeq='\033[0m'
                    unicodeBlockCharacterCode='\u2588'
                    print(f"{greenANSIEscapeSeq}{unicodeBlockCharacterCode}{ANSIEndSeq}", end = "")
            print()
            self.prevPrintedLength += 1

if __name__ == "__main__":
    
    game = GameOfLife((50,100))

    blockConfig = np.array([(25, 25), (25, 26), (26, 25), (26, 26)])
    callahanInfiniteFiveByFiveConfig = np.array([(25, 25), (25, 26), (25, 27), (25, 29),
    (26, 25), (27, 28), (27, 29), (28, 26), (28, 27), (28, 29), (29, 25), (29, 27), (29, 29)])

    game.setInitialConfig(callahanInfiniteFiveByFiveConfig)
    game.runGame(title = "Game of Life")
