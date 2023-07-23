import random

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def generate_tile():
    return random.choice([2, 4])


def new_game():
    board = [[0] * 4 for _ in range(4)]
    board[random.randint(0, 3)][random.randint(0, 3)] = generate_tile()
    return board


def can_move(board):
    for row in board:
        if 0 in row:
            return True

    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] or board[j][i] == board[j +
                                                                      1][i]:
                return True
    return False


def compress_board(board):
    new_board = [[0] * 4 for _ in range(4)]
    for i in range(4):
        pos = 0
        for j in range(4):
            if board[i][j] != 0:
                new_board[i][pos] = board[i][j]
                pos += 1
    return new_board


def merge_board(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j + 1] = 0
    return board


def transpose_board(board):
    return [[board[j][i] for j in range(4)] for i in range(4)]


def move_board(board, direction):
    if direction == 'up':
        board = transpose_board(board)
        board = move_left(board)
        board = transpose_board(board)
    elif direction == 'down':
        board = transpose_board(board)
        board = move_right(board)
        board = transpose_board(board)
    elif direction == 'left':
        board = move_left(board)
    elif direction == 'right':
        board = move_right(board)
    return board


def move_up(board):
    for j in range(4):
        for i in range(1, 4):
            if board[i][j] != 0:
                x = i
                while x > 0 and board[x - 1][j] == 0:
                    board[x - 1][j] = board[x][j]
                    board[x][j] = 0
                    x -= 1
                if x > 0 and board[x - 1][j] == board[x][j]:
                    board[x - 1][j] *= 2
                    board[x][j] = 0
    return board


def move_down(board):
    for j in range(4):
        for i in range(2, -1, -1):
            if board[i][j] != 0:
                x = i
                while x < 3 and board[x + 1][j] == 0:
                    board[x + 1][j] = board[x][j]
                    board[x][j] = 0
                    x += 1
                if x < 3 and board[x + 1][j] == board[x][j]:
                    board[x + 1][j] *= 2
                    board[x][j] = 0
    return board


def move_left(board):
    for i in range(4):
        for j in range(1, 4):
            if board[i][j] != 0:
                y = j
                while y > 0 and board[i][y - 1] == 0:
                    board[i][y - 1] = board[i][y]
                    board[i][y] = 0
                    y -= 1
                if y > 0 and board[i][y - 1] == board[i][y]:
                    board[i][y - 1] *= 2
                    board[i][y] = 0
    return board


def move_right(board):
    for i in range(4):
        for j in range(2, -1, -1):
            if board[i][j] != 0:
                y = j
                while y < 3 and board[i][y + 1] == 0:
                    board[i][y + 1] = board[i][y]
                    board[i][y] = 0
                    y += 1
                if y < 3 and board[i][y + 1] == board[i][y]:
                    board[i][y + 1] *= 2
                    board[i][y] = 0
    return board


@app.route('/')
def index():
    board = new_game()
    return render_template('index.html', board=board)


@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    direction = data['direction']
    board = data['board']
    board = [board[i:i + 4] for i in range(0, len(board), 4)]

    board = move_board(board, direction)
    if can_move(board):
        empty_tiles = [(i, j) for i in range(4) for j in range(4)
                       if board[i][j] == 0]
        if empty_tiles:
            x, y = random.choice(empty_tiles)
            board[x][y] = generate_tile()

    return jsonify({'board': [cell for row in board for cell in row]})


if __name__ == '__main__':
    app.run(debug=True)
