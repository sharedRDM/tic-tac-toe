# app.py
from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Initialize the game state
game_state = {
    "board": [["" for _ in range(3)] for _ in range(3)],
    "turn": "X",
    "winner": None,
    "difficulty": "hard"  # Default difficulty
}

def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]

    return None

def is_moves_left(board):
    for row in board:
        for cell in row:
            if cell == "":
                return True
    return False

def minimax(board, depth, is_max):
    winner = check_winner(board)
    if winner == "O":
        return 10 - depth
    if winner == "X":
        return depth - 10
    if not is_moves_left(board):
        return 0

    if is_max:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(best_score, score)
        return best_score

def find_best_move(board):
    best_score = -float('inf')
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def random_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
    return random.choice(empty_cells) if empty_cells else (-1, -1)

def medium_move(board):
    # Mix of random and best move
    return random_move(board) if random.random() < 0.5 else find_best_move(board)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    global game_state
    data = request.json
    game_state['difficulty'] = data.get('difficulty', 'hard')
    return jsonify({"difficulty": game_state['difficulty']})

@app.route('/move', methods=['POST'])
def move():
    global game_state
    data = request.json
    row, col = data['row'], data['col']

    if game_state['winner'] or game_state['board'][row][col]:
        return jsonify(game_state)

    # Player move
    game_state['board'][row][col] = game_state['turn']
    winner = check_winner(game_state['board'])

    if winner:
        game_state['winner'] = winner
        return jsonify(game_state)

    game_state['turn'] = "O"

    # Computer move
    if not game_state['winner']:
        if game_state['difficulty'] == "easy":
            ai_row, ai_col = random_move(game_state['board'])
        elif game_state['difficulty'] == "medium":
            ai_row, ai_col = medium_move(game_state['board'])
        else:
            ai_row, ai_col = find_best_move(game_state['board'])

        if ai_row is not None and ai_col is not None:
            game_state['board'][ai_row][ai_col] = "O"
            winner = check_winner(game_state['board'])
            if winner:
                game_state['winner'] = winner

    game_state['turn'] = "X"

    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset():
    global game_state
    game_state = {
        "board": [["" for _ in range(3)] for _ in range(3)],
        "turn": "X",
        "winner": None,
        "difficulty": game_state['difficulty']  # Preserve difficulty
    }
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)