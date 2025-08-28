import numpy as np
import random

game = [[' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]

Q = {}


def flatten_list(matrix: list[list[str]]):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list

learning_rate = 0.1
discount_factor = 0.9
exploration_rate = 0.1


def board_to_string(board: np.ndarray):
    return ''.join(board.flatten())
          
def choose_action(board, exploration_rate):
    true_board = np.asarray(board, dtype=np.int32)
    state = board_to_string(board)
    
    if random.uniform(0,1) < exploration_rate or state not in Q:
        empty_cells = np.argwhere(true_board == ' ')
        action = tuple(random.choice(empty_cells))
    else:
        q_values = Q[state]
        empty_cells = np.argwhere(true_board == ' ')
        empty_q_values = [q_values[cell[0],cell[1]] for cell in empty_cells]
        max_q_value = max(empty_q_values)
        max_q_indices = [i for i in range(len(empty_cells)) if empty_q_values == max_q_value]
        max_q_index = random.choice(max_q_indices)
        action = tuple(empty_cells[max_q_index])
    return action

def update_q_table(state, action, next_state, reward):
    q_values = Q.get(state, np.zeros((3,3)))

    next_q_values = Q.get(board_to_string(next_state), np.zeros((3,3)))
    max_next_q_value = np.max(next_q_values)

    q_values[action[0], action[1]] += learning_rate * (reward + discount_factor * max_next_q_value - q_values[action[0], action[1]])

    Q[state] = q_values



def check_row(game, symbol):
    flag = False
    for i in range(3):
        if game[i][0] == symbol and game[i][1] == symbol and game[i][2] == symbol:
            flag = True
    return flag

def check_column(game, symbol):
    flag = False
    for i in range(3):
        if game[0][i] == symbol and game[1][i] == symbol and game[2][i] == symbol:
            flag = True
    return flag

def check_decreasing_diagonal(game, symbol):
    flag = 0
    for i in range(3):
        if game[i][i] == symbol:
            flag += 1
    if flag == 3:
        return True
    else:
        return False
    
def check_increasing_diagonal(game, symbol):
    flag = 0
    for i in range(3):
        if game[i][2 - i] == symbol:
            flag += 1
    if flag == 3:
        return True
    else:
        return False

def check_victory(game, symbol):
    return check_row(game, symbol) or check_column(game, symbol) or check_decreasing_diagonal(game, symbol) or check_increasing_diagonal(game, symbol)

def remaining_positions(game, symbol):
    n = 0
    positions = {}
    print("Posicoes restantes:")
    for i in range(3):
        for j in range(3):
            if game[i][j] == ' ':
                n += 1
                print(f"{n} - ({i + 1}, {j + 1})")
                positions[n] = [i, j]
    flag = False
    while flag == False:
        op = int(input("Escolha uma posicao para jogar: "))
        if op in positions:
            i, j = positions[op]
            game[i][j] = symbol
            flag = True
        else:
            print("Opcao invalida. Tente novamente")

def print_game(game):
    for i in game:
        print(i)

def choose_players():
    print("1 - O")
    print("2 - X")
    while True:
        op = int(input("Escolha o simbolo que jogara primeiro: "))
        if op == 1:
            print("O (O) jogara primeiro.")
            return 'O', 'X'
        elif op == 2:
            print("O (X) jogara primeiro.")
            return 'X', 'O'
        else:
            print("Opcao invalida. Tente novamente.")

def tic_tac_toe(game):
    player1, player2 = choose_players()
    for i in range(9):
        print_game(game)
        if i % 2 == 0:
            print(f"Vez do jogador 1 ({player1}):")
            remaining_positions(game, player1)
            if check_victory(game, player1):
                print_game(game)
                print(f"O jogador 1 ({player1}) venceu.")
                return
        else:
            print(f"Vez do jogador 2 ({player2}):")
            remaining_positions(game, player2)
            if check_victory(game, player2):
                print_game(game)
                print(f"O jogador 2 ({player2}) venceu.")
                return
    print_game(game)
    print("O jogo empatou.")
    return


tic_tac_toe(game)
