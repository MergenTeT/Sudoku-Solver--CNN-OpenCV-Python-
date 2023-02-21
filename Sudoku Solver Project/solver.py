# DataFlair Sudoku solver


def find_empty(board):#boş olan bloğun nerede olduğunu kontrol eder
    """checkes where is an empty or unsolved block"""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None

def valid(board, num, pos):#satır sutun hucre sorguları gercekleşiyor
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True

#Sudoku cözülüyor
def solve(board):
    find = find_empty(board)#boş olan blok tespit bilgileri alınıyor
    if not find:
        return True
    else:
        row, col = find#koordinatlar değişkenlere atanıyor

    for i in range(1,10):#1 den 9 a olan rakamları atanmak için valid metoduyla birlikte işlemler gerçekleşiyor
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):#Recursive fonction
                return True
            board[row][col] = 0
    return False


def get_board(bo):
    """Takes a 9x9 matrix unsolved sudoku board and returns a fully solved board."""
    if solve(bo):
        return bo
    else:
        raise ValueError


