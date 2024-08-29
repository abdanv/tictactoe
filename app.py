from flask import Flask, render_template, request, redirect, url_for
import tictactoe as ttt
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "play_as_X" in request.form:
            user = ttt.X
            board = ttt.initial_state()
            ai_turn = False
        elif "play_as_O" in request.form:
            user = ttt.O
            board = ttt.initial_state()
            ai_turn = True  # AI starts as X
            move = (random.randint(0, 2), random.randint(0, 2))
            board = ttt.result(board, move)
            ai_turn = False
        elif "reset" in request.form:
            return redirect(url_for("index"))
        else:
            user = request.form.get("user")
            board = eval(request.form["board"])
            ai_turn = request.form.get("ai_turn") == "True"
            
            if not ai_turn:
                if "move" in request.form:
                    move = tuple(map(int, request.form["move"].split(',')))
                    if board[move[0]][move[1]] == ttt.EMPTY:
                        board = ttt.result(board, move)
                        if not ttt.terminal(board):
                            ai_turn = True
                            move = ttt.minimax(board)
                            board = ttt.result(board, move)
                            ai_turn = False
    else:
        user = None
        board = ttt.initial_state()
        ai_turn = False

    game_over = ttt.terminal(board)
    winner = ttt.winner(board)
    player = ttt.player(board)

    # Pass necessary constants to the template
    return render_template("index.html", user=user, board=board, game_over=game_over, winner=winner, player=player, ai_turn=ai_turn, X=ttt.X, O=ttt.O, EMPTY=ttt.EMPTY)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
