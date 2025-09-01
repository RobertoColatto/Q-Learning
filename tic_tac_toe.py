import numpy as np
import random
from tkinter import*

board = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]

#Q-Learning
Q = {}

def flatten_list(matrix: list[list[str]]):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list

learning_rate = 0.1
discount_factor = 0.9
exploration_rate = 0.1

def board_to_string(board_matrix):
    arr = np.array(board_matrix)
    return ''.join(arr.flatten())
          
def choose_action(board, exploration_rate):
    state = board_to_string(board)
    empty_cells = np.argwhere(board == ' ')
    
    if random.uniform(0,1) < exploration_rate or state not in Q:
        action = tuple(random.choice(empty_cells))
    else:
        q_values = Q[state]
        empty_q_values = [q_values[cell[0],cell[1]] for cell in empty_cells]
        max_q_value = max(empty_q_values)
        max_q_indices = [i for i in range(len(empty_cells)) if empty_q_values[i] == max_q_value]
        max_q_index = random.choice(max_q_indices)
        action = tuple(empty_cells[max_q_index])
    return action

def update_q_table(state, action, next_state, reward):
    q_values = Q.get(state, np.zeros((3,3)))

    next_q_values = Q.get(next_state, np.zeros((3,3)))
    max_next_q_value = np.max(next_q_values)

    q_values[action[0], action[1]] += learning_rate * (reward + discount_factor * max_next_q_value - q_values[action[0], action[1]])

    Q[state] = q_values

#Verificações de vitória/empate
def check_row(board, symbol):
    flag = False
    for i in range(3):
        if board[i][0] == symbol and board[i][1] == symbol and board[i][2] == symbol:
            flag = True
    return flag

def check_column(board, symbol):
    flag = False
    for i in range(3):
        if board[0][i] == symbol and board[1][i] == symbol and board[2][i] == symbol:
            flag = True
    return flag

def check_decreasing_diagonal(board, symbol):
    flag = 0
    for i in range(3):
        if board[i][i] == symbol:
            flag += 1
    if flag == 3:
        return True
    else:
        return False
    
def check_increasing_diagonal(board, symbol):
    flag = 0
    for i in range(3):
        if board[i][2 - i] == symbol:
            flag += 1
    if flag == 3:
        return True
    else:
        return False

def check_victory(board, symbol):
    return check_row(board, symbol) or check_column(board, symbol) or check_decreasing_diagonal(board, symbol) or check_increasing_diagonal(board, symbol)

def is_draw(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return False
    return True

#UI
class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Velha (Q-Learning)")
        self.master.resizable(False, False)

        self.board = [[' ']*3 for _ in range(3)]
        self.player_symbol = 'X'
        self.opponent_symbol = 'O'
        self.player_starts = True

        self.opponent_last_state = None
        self.opponent_last_action = None

        #MENU FRAME
        self.menu_frame = Frame(self.master, padx=16, pady=16)
        self.menu_frame.pack()

        Label(self.menu_frame, text="Jogo da Velha", font=("Verdana", 14, "bold")).pack(pady=(0, 10))

        self.starts_var = StringVar(value="player")
        starts_box = LabelFrame(self.menu_frame, text="Quem começa?", padx=10, pady=10)
        starts_box.pack(fill="x", pady=6)
        Radiobutton(starts_box, text="Você", variable=self.starts_var, value="player").pack(anchor="w")
        Radiobutton(starts_box, text="Máquina", variable=self.starts_var, value="opponent").pack(anchor="w")

        self.symbol_var = StringVar(value="X")
        symbol_box = LabelFrame(self.menu_frame, text="Seu símbolo", padx=10, pady=10)
        symbol_box.pack(fill="x", pady=6)
        Radiobutton(symbol_box, text="X", variable=self.symbol_var, value="X").pack(anchor="w")
        Radiobutton(symbol_box, text="O", variable=self.symbol_var, value="O").pack(anchor="w")

        Button(self.menu_frame, text="Iniciar jogo", width=16, command=self.start_game).pack(pady=(10, 4))

        #GAME FRAME
        self.game_frame = Frame(self.master, padx=12, pady=12)

        self.buttons = [[None]*3 for _ in range(3)]
        grid_frame = Frame(self.game_frame)
        grid_frame.pack()

        for i in range(3):
            for j in range(3):
                btn = Button(grid_frame, text=" ", width=4, height=2, font=("Verdana", 22), command=lambda x=i, y=j: self.player_move(x, y))
                btn.grid(row=i, column=j, padx=4, pady=4)
                self.buttons[i][j] = btn

        self.status = Label(self.game_frame, text="", font=("Verdana", 11))
        self.status.pack(pady=(10, 6))

        controls = Frame(self.game_frame)
        controls.pack()
        Button(controls, text="Jogar novamente", command=self.reset_board).grid(row=0, column=0, padx=6)
        Button(controls, text="Voltar ao menu", command=self.back_to_menu).grid(row=0, column=1, padx=6)

    #FUNÇÕES
    def start_game(self):
        self.player_starts = (self.starts_var.get() == "player")
        self.player_symbol = self.symbol_var.get()
        self.opponent_symbol = 'O' if self.player_symbol == 'X' else 'X'

        self.reset_board()
        self.menu_frame.pack_forget()
        self.game_frame.pack()

    def back_to_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack()

    def reset_board(self):
        self.board = [[' ']*3 for _ in range(3)]
        self.opponent_last_state = None
        self.opponent_last_action = None
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state=NORMAL)

        if not self.player_starts:
            self.status.config(text="Vez da máquina.")
            self.master.after(300, self.opponent_move)
        else:
            self.status.config(text="Sua vez.")

    def disable_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=DISABLED)

    def player_move(self, i, j):
        if self.board[i][j] != ' ':
            return
        self.board[i][j] = self.player_symbol
        self.buttons[i][j].config(text=self.player_symbol, state=DISABLED)

        if check_victory(self.board, self.player_symbol):
            self.status.config(text="Você venceu.")
            if self.opponent_last_state is not None and self.opponent_last_action is not None:
                cur_state = board_to_string(self.board)
                update_q_table(self.opponent_last_state, self.opponent_last_action, cur_state, reward=-1.0)
            self.disable_board()
            return
        
        if is_draw(self.board):
            self.status.config(text="O jogo empatou.")
            if self.opponent_last_state is not None and self.opponent_last_action is not None:
                cur_state = board_to_string(self.board)
                update_q_table(self.opponent_last_state, self.opponent_last_action, cur_state, reward=0.5)
            self.disable_board()
            return
        
        self.status.config(text="Vez da máquina.")
        self.master.after(300, self.opponent_move)

    def opponent_move(self):
        board_np = np.array(self.board)
        state = board_to_string(board_np)

        action = choose_action(board_np, exploration_rate)
        i, j = action
        self.board[i][j] = self.opponent_symbol
        self.buttons[i][j].config(text=self.opponent_symbol, state=DISABLED)

        next_state = board_to_string(self.board)
        if self.opponent_last_state is not None and self.opponent_last_action is not None:
            update_q_table(self.opponent_last_state, self.opponent_last_action, state, reward=0.0)

        self.opponent_last_state = state
        self.opponent_last_action = action

        if check_victory(self.board, self.opponent_symbol):
            self.status.config(text="A máquina venceu.")
            update_q_table(self.opponent_last_state, self.opponent_last_action, next_state, reward=+1.0)
            self.disable_board()
            return

        if is_draw(self.board):
            self.status.config(text="Empate.")
            update_q_table(self.opponent_last_state, self.opponent_last_action, next_state, reward=0.5)
            self.disable_board()
            return

        self.status.config(text="Sua vez.")

root = Tk()
app = Application(root)
root.mainloop()
