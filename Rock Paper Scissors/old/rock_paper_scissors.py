from colorama import init, Fore, Back, Style
init()
Bot_score = 0
player_score = 0
done = True
while done:
    continue_word = input('Do you want to Play?? ').lower()
    if continue_word.startswith('n') :
        done = False
        if player_score > Bot_score :
            winner = 'player is winner'
        if Bot_score > player_score :
            winner = '  BOT is winner '
        if player_score == Bot_score :
            winner = '  game is equal '
        end_message = ('''
                                           ___________________________________________
                                           |             player_score is : '''f'{player_score}''''         |
                                           |             Bot_score is : '''f'{Bot_score}''''            |
                                           |             '''f'{winner}''''            |
                                           \\_________________________________________/''')
        if player_score > Bot_score :
            end_message = Fore.GREEN + end_message
        if Bot_score > player_score :
            end_message = Fore.RED + end_message
        if player_score == Bot_score :
            end_message = Fore.BLUE + end_message
        print(end_message)
    if not continue_word.startswith('n') :
        import random
        ACTIONS = 'rock','paper','scissors'
        Bot_act = (random.choice(ACTIONS))
        player_act = input('choose : rock,paper or scissors??(r, p, s) : ').lower()
        if player_act.startswith('r') :
            player_act = 'rock'
        if player_act.startswith('p') :
            player_act = 'paper'
        if player_act.startswith('s') :
            player_act = 'scissors'
        print('Bot selection is : 'f'{Bot_act}')
        if player_act == 'rock' and Bot_act == 'rock' :
            print('equal')
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')
        if player_act == 'rock' and Bot_act == 'paper' :
            print('bot is win')
            Bot_score += 1
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')
        if player_act == 'rock' and Bot_act == 'scissors' :
            print('paler is win')
            player_score += 1
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')
        if player_act == 'paper' and Bot_act == 'paper' :
            print('equal')
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')
        if player_act == 'paper' and Bot_act == 'rock' :
            print('player is win')
            player_score += 1
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')
        if player_act == 'paper' and Bot_act == 'scissors' :
            print('bot is win')
            Bot_score += 1
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')
        if player_act == 'scissors' and Bot_act == 'scissors' :
            print('equal')
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')
        if player_act == 'scissors' and Bot_act == 'paper' :
            print('player is win')
            player_score += 1
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')
        if player_act == 'scissors' and Bot_act == 'rock' :
            print('bot is win')
            Bot_score += 1
            print('Bot_score : 'f'{Bot_score}')
            print('Player_score : 'f'{player_score}')