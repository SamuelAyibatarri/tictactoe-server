from flask import Flask, json, jsonify, request
from flask_socketio import SocketIO, join_room, emit, disconnect
from flask_cors import CORS
from minimax import getBestMove

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

# --- GAME STATE STORAGE ---
# Format:
# {
#   "room_1": {
#       "board": ["", "", ...],
#       "turn": "X",
#       "players": ["socket_id_1", "socket_id_2"]
#   }
# }
games = {}

@socketio.on('join_game')
def handle_join(data):
    room = data['room']
    sid = request.sid
    
    if room not in games:
        games[room] = {
            "board": [""] * 9,
            "turn": "X",
            "players": []
        }
    
    game = games[room]
    
    if len(game["players"]) >= 2:
        emit('error', {'msg': 'Room is full!'}, to=sid)
        return

    join_room(room)
    game["players"].append(sid)
    
    symbol = "X" if len(game["players"]) == 1 else "O"
    emit('player_joined', {'symbol': symbol}, to=sid)
    
    if len(game["players"]) == 2:
        emit('game_start', {'startTurn': True}, room=room)
        print(f"Game started in room {room}")


@socketio.on('make_move')
def handle_move(data):
    room = data['room']
    index = data['index']
    sid = request.sid
    
    if room not in games: return
    game = games[room]
    
    if sid not in game["players"]: return 
    player_symbol = "X" if game["players"][0] == sid else "O"
    
    if game["turn"] != player_symbol:
        return 
    
    if game["board"][index] != "":
        return 
    
    game["board"][index] = player_symbol
    
    game["turn"] = "O" if player_symbol == "X" else "X"
    
    winner = check_winner(game["board"])
    
    emit('update_board', {
        'board': game["board"],
        'nextTurn': game["turn"]
    }, room=room)
    
    if winner:
        emit('game_over', {'winner': winner}, room=room)


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    for room_id, game in list(games.items()):
        if sid in game["players"]:
            game["players"].remove(sid)
            emit('error', {'msg': 'Opponent disconnected. Refresh to play again.'}, room=room_id)
            
            if len(game["players"]) == 0:
                del games[room_id]
            break

def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Cols
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for pattern in wins:
        a, b, c = pattern
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    
    if "" not in board:
        return "draw"
        
    return None

@app.route('/play', methods=['POST'])
def play_move():
    try:
        board_str = request.form.get('board')
        maximizing_str = request.form.get('maximizing')

        if not board_str or not maximizing_str:
            return jsonify({"error": "Missing 'board' or 'maximizing' field"}), 400

        try:
            board = json.loads(board_str) 
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid board format. Expected JSON string."}), 400
        
        is_maximizing = maximizing_str.lower() == 'true'

        _, best_move = getBestMove(board, is_maximizing)

        if best_move is None:
             return jsonify({"game_over": True, "message": "No moves left"})

        return jsonify({
            "move": best_move,  
            "maximizing": is_maximizing
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
