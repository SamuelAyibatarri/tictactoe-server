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
    if row < 1 and row > 3:
        return "Invalid row val"
    A = np.array(userMatrix)
    result = cuv @ A @ oneMatrixT
    return result


def colSum(userMatrix, col=1):
    cuv = e1T
    if col == 2:
        cuv = e2T
    if col == 3:
        cuv = e3T
    if col < 1 and col > 3:
        return "Invalid col val"
    A = np.array(userMatrix)
    result = oneMatrix @ A @ cuv
    return result


def lDiagonalSum(userMatrix):
    A = np.array(userMatrix)
    return np.trace(A)


def sDiagonalSum(userMatrix):
    A = np.array(userMatrix)
    A_Flipped = A[:, ::-1]
    print(A_Flipped)
    return np.trace(A_Flipped)


test = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
output = rowSum(test, 12)
output2 = colSum(test, 1)
output3 = lDiagonalSum(test)
output4 = sDiagonalSum(test)
print("Row sum output", output)
print("Col sum output", output2)
print("Trace sum output", output3)
print("Secondary trace", output4)
