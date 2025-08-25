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

game = [[' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]

tic_tac_toe(game)