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

learning_rate = 0.001
discount_factor = 0.9
exploration_rate = 0.5

def board_to_string(board_matrix):
    arr = np.array(board_matrix)
    return ''.join(arr.flatten())
          
def choose_action(board, exploration_rate):
    print(exploration_rate)
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

        train_box = LabelFrame(self.menu_frame, text="Treinar Bot vs Bot", padx=10, pady=10)
        train_box.pack(fill="x", pady=6)
        Label(train_box, text="Nº de jogos:").pack(side="left")
        self.train_games_entry = Entry(train_box, width=6)
        self.train_games_entry.insert(0, "1000")  # default
        self.train_games_entry.pack(side="left", padx=6)
        Button(train_box, text="Treinar", command=self.run_bot_training).pack(side="left")

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

    def simulate_bot_vs_bot(self,num_games=1000):
        exploration_rate = 0.5
        for game in range(num_games):
            board = [[' ']*3 for _ in range(3)]
            state = board_to_string(board)
            last_state_X, last_action_X = None, None
            last_state_O, last_action_O = None, None
            current_symbol = 'X'

            while True:
                board_np = np.array(board)
                action = choose_action(board_np, exploration_rate)
                i, j = action
                board[i][j] = current_symbol
                next_state = board_to_string(board)

                if current_symbol == 'X' and last_state_X is not None:
                    #pass
                    update_q_table(last_state_X, last_action_X, next_state, reward=0.0)
                if current_symbol == 'O' and last_state_O is not None:
                    #pass
                    update_q_table(last_state_O, last_action_O, next_state, reward=0.0)

                if current_symbol == 'X':
                    last_state_X, last_action_X = state, action
                else:
                    last_state_O, last_action_O = state, action

                state = next_state

                # check for terminal states
                if check_victory(board, current_symbol):
                    if current_symbol == 'X':
                        update_q_table(last_state_X, last_action_X, state, reward=+1.0)
                        update_q_table(last_state_O, last_action_O, state, reward=-1.0)
                    else:
                        update_q_table(last_state_O, last_action_O, state, reward=+1.0)
                        update_q_table(last_state_X, last_action_X, state, reward=-1.0)
                    break

                if is_draw(board):
                    #if last_state_X is not None:
                    update_q_table(last_state_X, last_action_X, state, reward=0.5)
                    #if last_state_O is not None:
                    update_q_table(last_state_O, last_action_O, state, reward=0.5)
                    break
                exploration_rate *= 0.99
                
                
                current_symbol = 'O' if current_symbol == 'X' else 'X'
    def run_bot_training(self):
        try:
            n = int(self.train_games_entry.get())
        except ValueError:
            n = 1000
        self.simulate_bot_vs_bot(n)
        Label(self.menu_frame, text=f"Treino concluído ({n} jogos).", fg="green").pack()


        

root = Tk()
app = Application(root)
root.mainloop()
