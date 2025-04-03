import os
import pygame
from random import choice
current_path = os.path.dirname(__file__) 

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Rock Paper Scissors')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

game_choices = ['rock', 'paper', 'scissors']
player_score = 0
computer_score = 0

rock_img = pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'assets', 'rock.png')), (100, 100))
rock_rect = rock_img.get_rect()
rock_rect.topleft = (80, 450)

paper_img = pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'assets', 'paper.png')), (100, 100))
paper_rect = paper_img.get_rect()
paper_rect.topleft = (350, 450)

scissors_img = pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'assets', 'scissors.png')), (100, 100))
scissors_rect = scissors_img.get_rect()
scissors_rect.topright = (720, 450)

font = pygame.font.SysFont('terminal', 32)
font_s = pygame.font.SysFont('terminal', 20)

def get_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "tie"
    elif (
        (player_choice == "rock" and computer_choice == "scissors")
        or (player_choice == "paper" and computer_choice == "rock")
        or (player_choice == "scissors" and computer_choice == "paper")
    ):
        return "player"
    else:
        return "computer"
    
def repead_func(winner, before_winner) :
    if winner == before_winner:
        return True
    else :
        return False
    
player_choice = ''
computer_choice = ''
repead = 1
clicked = False

runnung = True
while runnung :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnung = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            player_choice = ''
            computer_choice = ''
            round_winner = ''
            try :
                before_winner = winner
            except :
                None
            if rock_rect.collidepoint(event.pos):
                player_choice = 'rock'
                clicked = True
            elif paper_rect.collidepoint(event.pos):
                player_choice = 'paper'
                clicked = True
            elif scissors_rect.collidepoint(event.pos):
                player_choice = 'scissors'
                clicked = True
            if player_choice != '' :
                computer_choice = choice(game_choices)
            if clicked:
                winner = get_winner(player_choice, computer_choice)
                if winner == 'player' :
                    player_score += 1
                    round_winner = 'player'
                    text = 'is winner'
                    t_color = GREEN
                elif winner == 'computer' :
                    computer_score += 1
                    round_winner = 'computer'
                    text = 'is winner'
                    t_color = RED
                else : 
                    t_color = WHITE
                    text = 'it\'s tie'
    
                try :
                    reap = repead_func(winner, before_winner)
                except :
                    None
                try :
                    if reap :
                        repead += 1
                    else :
                        repead = 1
                except :
                    None
    
                if repead <= 1 :
                    winner_text = font.render(f'{round_winner} {text}', True, t_color)
                    winner_rect = winner_text.get_rect()
                    winner_rect.center = (400, 300)
                else :
                    winner_text = font.render(f'{round_winner} {text}X{repead}', True, t_color)
                    winner_rect = winner_text.get_rect()
                    winner_rect.center = (400, 300)
            else:
                repead = 0
                winner_text = ''

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

    screen.fill(BLACK)

    pscore_text = font.render(f'player score : {player_score}', True, WHITE)
    pscore_rect = pscore_text.get_rect()
    pscore_rect.topleft = (50, 60)

    cscore_text = font.render(f'computer score : {computer_score}', True, WHITE)
    cscore_rect = cscore_text.get_rect()
    cscore_rect.topright = (750, 60)

    player_choice_text = font_s.render(f'player choice : {player_choice}', True, WHITE)
    player_choice_rect = player_choice_text.get_rect()
    player_choice_rect.topleft = (50, 100)

    computer_choice_text = font_s.render(f'computer choice : {computer_choice}', True, WHITE)
    computer_choice_rect = computer_choice_text.get_rect()
    computer_choice_rect.topleft = (552, 100)

    screen.blit(rock_img, rock_rect)
    screen.blit(paper_img, paper_rect)
    screen.blit(scissors_img, scissors_rect)
    screen.blit(pscore_text, pscore_rect)
    screen.blit(cscore_text, cscore_rect)
    screen.blit(player_choice_text, player_choice_rect)
    screen.blit(computer_choice_text, computer_choice_rect)
    try :
        screen.blit(winner_text, winner_rect)
    except :
        None

    pygame.display.update()

pygame.quit()