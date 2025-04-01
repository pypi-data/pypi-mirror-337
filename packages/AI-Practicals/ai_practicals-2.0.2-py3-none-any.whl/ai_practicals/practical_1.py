import numpy as np

def Practical_1():
    # Creating matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])

    # Matrix addition
    C = A + B

    # Matrix multiplication
    D = np.dot(A, B)

    # Determinant
    det_A = np.linalg.det(A)

    # Eigenvalues and Eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(A)

    print("Matrix A:\n", A)
    print("Matrix B:\n", B)
    print("Matrix Addition:\n", C)
    print("Matrix Multiplication:\n", D)
    print("Determinant of A:", det_A)
    print("Eigenvalues of A:", eigenvalues)
    print("Eigenvectors of A:\n", eigenvectors)

# You can call the function like this:
# Practical_1()