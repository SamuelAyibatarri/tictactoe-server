import copy
import numpy as np

# eN where N could be any number refers to the canonical unit vectors
e1 = np.array([[1, 0, 0]])
e2 = np.array([[0, 1, 0]])
e3 = np.array([[0, 0, 1]])

# eNT represents the transpose of the canonical unit vectors
e1T = e1.T
e2T = e2.T
e3T = e3.T

oneMatrix = np.array([[1, 1, 1]])
oneMatrixT = oneMatrix.T


def rowSum(userMatrix, row=1):
    cuv = e1  # canonical unit vector
    if row == 2:
        cuv = e2
    if row == 3:
        cuv = e3
    if row < 1 or row > 3:
        raise ValueError("Invalid row val")
    result = cuv @ userMatrix @ oneMatrixT
    return result.item()


def colSum(userMatrix, col=1):
    cuv = e1T
    if col == 2:
        cuv = e2T
    if col == 3:
        cuv = e3T
    if col < 1 or col > 3:
        raise ValueError("Invalid col val")
    result = oneMatrix @ userMatrix @ cuv
    return result.item()


def lDiagonalSum(userMatrix):
    return np.trace(userMatrix)


def sDiagonalSum(userMatrix):
    A_Flipped = userMatrix[:, ::-1]
    return np.trace(A_Flipped)

# Evaluation Function
def evaluationFunc(userMatrix):
    A = np.array(userMatrix)
    if (lDiagonalSum(A) == 3) or (sDiagonalSum(A) == 3):
        return 1

    if (lDiagonalSum(A) == -3) or (sDiagonalSum(A) == -3):
        return -1

    for i in range(1, 4):
        xwin = (colSum(A, i) == 3) or (rowSum(A, i) == 3)
        owin = (colSum(A, i) == -3) or (rowSum(A, i) == -3)
        if xwin:
            return 1
        if owin:
            return -1
    return 0


def getValidMoves(userMatrix):
    validMoves = []
    for i in range(3):
        for j in range(3):
            if userMatrix[i][j] == 0:
                validMoves.append((i, j))
    return validMoves


def playMove(userMatrix, move, turn):
    userMatrix[move[0]][move[1]] = turn
    return userMatrix


def minimax(userMatrix, maximizing: bool, depth = 0):
    turn = 1 if maximizing else -1

    score = evaluationFunc(userMatrix)

    if score == 1: return 10 - depth
    if score == -1: return -10 + depth  
    
    moves = getValidMoves(userMatrix)

    if len(moves) == 0: return 0 
    
    baseScore = -float('inf') if maximizing else float('inf')

    for move in moves:
        boardCopy = copy.deepcopy(userMatrix)
        playMove(boardCopy, move, turn)
            
        currentScore = minimax(boardCopy, not maximizing, depth + 1)
        bestScore = max(baseScore, currentScore) if maximizing else min(baseScore, currentScore)
        baseScore = bestScore
    return bestScore


def getBestMove(userMatrix, maximizing: bool):
    print("Thinking...")
    moveEvaluation = {}
    moves = getValidMoves(userMatrix)
    turn = 1 if maximizing else -1
    bestScore = -float('inf') if maximizing else float('inf')
    bestMove = None
    
    for move in moves:
        boardCopy = copy.deepcopy(userMatrix)
        playMove(boardCopy, move, turn)
        
        score = minimax(boardCopy, not maximizing)
        
        moveEvaluation[move] = score
        
        if (score > bestScore and maximizing) or (score < bestScore and not maximizing):
            bestScore = score
            bestMove = move
            
    return moveEvaluation, bestMove
