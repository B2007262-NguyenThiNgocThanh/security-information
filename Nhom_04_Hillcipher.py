UNICODE_NUM = 256

def calc_det(matrix):
    # Check if the matrix is square
    if len(matrix) != len(matrix[0]):
        return "The matrix is not square."

    # Base case: if the matrix is 1x1, return the single element
    if len(matrix) == 1:
        return matrix[0][0]

    # Recursive case: calculate the determinant using cofactor expansion
    determinant = 0
    for i in range(len(matrix)):
        # Calculate the cofactor of the current element
        cofactor = (-1) ** i * matrix[0][i]

        # Create the submatrix by removing the first row and current column
        submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]

        # Recursively calculate the determinant of the submatrix
        submatrix_determinant = calc_det(submatrix)

        # Add the product of the cofactor and submatrix determinant to the total determinant
        determinant += cofactor * submatrix_determinant

    return determinant


def multiply_matrix(matrix, number):
    result = []
    for row in matrix:
        new_row = [element * number for element in row]
        result.append(new_row)
    return result


def add_number(matrix, number):
    result = []
    for row in matrix:
        new_row = [element + number for element in row]
        result.append(new_row)
    return result


def modulus_matrix(matrix, number):
    result = []
    for row in matrix:
        new_row = [element % number for element in row]
        result.append(new_row)
    return result

def round_matrix(matrix):
    result = []
    for row in matrix:
        new_row = [round(element) for element in row]
        result.append(new_row)
    return result



def inverse_matrix_func(matrix):
    # Check if the matrix is square
    if len(matrix) != len(matrix[0]):
        return "The matrix is not square."

    # Create an augmented matrix [matrix | identity matrix]
    n = len(matrix)
    augmented_matrix = [row + [1 if i == j else 0 for i in range(n)] for j, row in enumerate(matrix)]

    # Apply Gauss-Jordan elimination
    for i in range(n):
        # Find the pivot row
        pivot_row = max(range(i, n), key=lambda j: abs(augmented_matrix[j][i]))

        # Swap rows
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]

        # Scale the pivot row
        pivot = augmented_matrix[i][i]
        augmented_matrix[i] = [element / pivot for element in augmented_matrix[i]]

        # Eliminate other rows
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                augmented_matrix[j] = [element - factor * augmented_matrix[i][k] for k, element in enumerate(augmented_matrix[j])]

    # Extract the inverse matrix
    inverse = [row[n:] for row in augmented_matrix]

    return inverse




def dot_matrix(matrix1, matrix2):
    # Check if the dimensions are compatible for matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        return "The matrices are not compatible for dot product."

    # Get the dimensions of the matrices
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])

    # Create a new matrix to store the result
    result = [[0 for _ in range(cols2)] for _ in range(rows1)]

    # Perform dot product
    for i in range(rows1):
        for j in range(cols2):
            for k in range(cols1):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result


def adjugate(matrix):
    det = calc_det(matrix)

    if det == 0:
        raise ValueError("The matrix is singular and does not have an inverse.")
    
    inverse_matrix = inverse_matrix_func(matrix)

    adjugate_matrix = multiply_matrix(inverse_matrix, det)

    return adjugate_matrix

#transpose string key to int, ord(): function return int => unicode
#transpose string message to int
def getMatrix(message, SIZE_MATRIX):
    result = []
    for size_matrix in range(SIZE_MATRIX):
        result.append([])

    lenMessage = len(message)
    i = 0
    while (i < lenMessage):
        for row in range(SIZE_MATRIX):
            if (i < lenMessage):
                result[row].append(ord(message[i]))
            else:
                result[row].append(32)
            i+=1
    return result

def getMessage(matrix, SIZE_MATRIX):
    if (matrix is None):
        return
    if (matrix[0] is None):
        return
    result = ""
    lenCol = len(matrix[0])
    for c in range(lenCol):
        for r in range(SIZE_MATRIX):
            result += chr(matrix[r][c])
    return result
    

#encypher the message
def encodeHillCipher(matrixM, matrixK):
    newMatrix = dot_matrix(matrixK, matrixM)
    newMatrix = modulus_matrix(newMatrix, UNICODE_NUM)
    return newMatrix

def decodeHillCipher(encryptMatrix, matrixK):
    detMatrix = int(calc_det(matrixK))

    adjugate_matrix = adjugate(matrixK)
    adjugate_matrix_module = modulus_matrix(add_number(adjugate_matrix, UNICODE_NUM),UNICODE_NUM)
    invMatrixModule = modulus_matrix (multiply_matrix(adjugate_matrix_module, pow(detMatrix,-1, UNICODE_NUM)),UNICODE_NUM)

    decodeMatrix = modulus_matrix(dot_matrix(invMatrixModule, encryptMatrix),UNICODE_NUM)
    return round_matrix(decodeMatrix)
    

def main():
    # luu y (SIZE_MATRIX "so hang") trong getMatrix:
    # phai thoa dieu kien neu "ma tran can ma hoa" "co so hang" la 3 thi do dai cua key phai la "3*3"
    # neu co "so hang" la 4 thi do dai cua string phai la (4*4)
    # neu co "so hang" la n thi do dai cua string phai la (n*n)
    # va "ma tran cua 'variable key dong 178'" phai "capable of inversion"
    # capable of inversion is det(A) = 0
    key = "ABCDEFGHI"


    message = input("Enter the message: ")
    # key = input("Enter the Key": )
    # print("Message: ", "".join(message))
    # print("Key: ", "".join(key))

    # so 3 la so hang cua ma tran
    matrixKCustom = getMatrix(key, 3)
    # matrixK taken from wiki
    matrixK = [[6,24,1],[13,16,10],[20,17,15]]
    matrixM = getMatrix(message, 3)

    encryptMatrix = encodeHillCipher(matrixM, matrixK)
    decodeMatrix = decodeHillCipher(encryptMatrix, matrixK)

    # print("\norigin matrix")
    print(matrixM)
    print("\nencode matrix")
    print(encryptMatrix)
    print("\ndecode matrix")
    print(decodeMatrix)
    print ("\nMessage encode:")
    print(getMessage(encryptMatrix, 3))
    print("\nMessage decode:")
    print(getMessage(decodeMatrix, 3))
    

if __name__=="__main__":
    main()