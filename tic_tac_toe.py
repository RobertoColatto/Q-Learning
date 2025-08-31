import numpy as np
import random

board = [[' ', ' ', ' '],
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
    state = board_to_string(board)
    empty_cells = np.argwhere(board == ' ')
    
    if random.uniform(0,1) < exploration_rate or state not in Q:
        action = tuple(random.choice(empty_cells))
    else:
        q_values = Q[state]
        empty_q_values = [q_values[cell[0],cell[1]] for cell in empty_cells]
        max_q_value = max(empty_q_values)
        max_q_indices = [i for i in range(len(empty_cells)) if empty_q_values == max_q_value]
        max_q_index = random.choice(max_q_indices)
        action = tuple(empty_cells[max_q_index])
    return action

def update_q_table(state, action, next_state, reward):
    q_values = Q.get(state, np.zeros((3,3)))

    next_q_values = Q.get(next_state, np.zeros((3,3)))
    max_next_q_value = np.max(next_q_values)

    q_values[action[0], action[1]] += learning_rate * (reward + discount_factor * max_next_q_value - q_values[action[0], action[1]])

    Q[state] = q_values



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

def remaining_positions(board, symbol):
    n = 0
    positions = {}
    print("Posicoes restantes:")
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                n += 1
                print(f"{n} - ({i + 1}, {j + 1})")
                positions[n] = [i, j]
    flag = False
    while flag == False:
        op = int(input("Escolha uma posicao para jogar: "))
        if op in positions:
            i, j = positions[op]
            board[i][j] = symbol
            flag = True
        else:
            print("Opcao invalida. Tente novamente")

def print_board(board):
    for i in board:
        print(i)

def choose_players():
    you_plays_first = True
    
    while True:
        print("1 - Voce")
        print("2 - Maquina")
        op1 = int(input("Escolha quem devera jogar primeiro: "))
        if op1 == 1:
            print("Você jogara primeiro.")
            you_plays_first = True
            break
        elif op1 == 2:
            print("A maquina jogara primeiro.")
            you_plays_first = False
            break
        else:
            print("Opção invalida. Tente novamente.")
    
    print("1 - O")
    print("2 - X")
    while True:
        op2 = int(input("Escolha o simbolo como o qual deseja jogar: "))
        if op2 == 1:
            print("Você jogara como (O).")
            return you_plays_first, 'O', 'X'
        elif op2 == 2:
            print("Você jogara como (X).")
            return you_plays_first, 'X', 'O'
        else:
            print("Opção inválida. Tente novamente.")

def tic_tac_toe(board):
    you_play_first, player, opponent = choose_players()
    state = board_to_string(np.array(board))

    if you_play_first == True:
        n = 0
    else:
        n = 1

    for i in range(9):
        print_board(board)

        if i % 2 == n:
            # Jogador humano
            print(f"Sua vez:")
            remaining_positions(board, player)
            next_state = board_to_string(np.array(board))
            if check_victory(board, player):
                print_board(board)
                print(f"Voce venceu.")
                # Atualiza Q da máquina (derrota)
                update_q_table(state, action, next_state, -1)
                return
            
        else:
            # Jogador máquina (Q-learning)
            print(f"Vez da maquina:")
            board_np = np.array(board)
            action = choose_action(board_np, exploration_rate)
            board[action[0]][action[1]] = opponent
            next_state = board_to_string(np.array(board))

            if check_victory(board, opponent):
                print_board(board)
                print(f"A maquina venceu.")
                # Atualiza Q da máquina (vitória)
                update_q_table(state, action, next_state, +1)
                return
            else:
                # Movimento normal sem recompensa
                update_q_table(state, action, next_state, 0)

        state = next_state

    print_board(board)
    print("O jogo empatou.")
    # Empate: recompensa menor
    update_q_table(state, action, state, 0.5)
    return


tic_tac_toe(board)
