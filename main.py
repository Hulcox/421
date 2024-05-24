import pygame
import random
from dice import draw_dice, roll_dice, animate_dice_roll
from utils import check_combination, display_message

# Initialize Pygame
pygame.init()

# Define colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen configuration
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('421 Dice Game')

# Font for text
font = pygame.font.Font(None, 36)

# Button configuration
button_rect = pygame.Rect(350, 450, 100, 50)
button_radius = 10  # Corner radius for the button

# Start button configuration
start_width = 200
start_height = 50
start_x = (800 - start_width) // 2  # Centrer horizontalement
start_y = 250  # Position verticale arbitraire

start_rect = pygame.Rect(start_x, start_y, start_width, start_height)

# Restart button configuration
restart_rect = pygame.Rect(300, 450, 200, 50)

# Initial values for dice and their states
dice_values = [random.randint(1, 6) for _ in range(3)]
dice_states = [False, False, False]  # False means the dice will be rolled
rolls_left = 3

running = True
game_started = False
game_over = False

def roll_dice_with_animation():
    global rolls_left, game_over
    animate_dice_roll(screen, dice_values, dice_states, font, button_rect, rolls_left)
    roll_dice(dice_values, dice_states)
    rolls_left -= 1
    if check_combination(dice_values):
        game_over = True
    elif rolls_left == 0:
        game_over = True

def start_game():
    global game_started
    game_started = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not game_over:
                if not game_started and start_rect.collidepoint(x, y):
                    start_game()
                elif button_rect.collidepoint(x, y):
                    roll_dice_with_animation()
                elif game_started:
                    positions = [(200, 300), (350, 300), (500, 300)]
                    for i, (px, py) in enumerate(positions):
                        if px < x < px + 100 and py < y < py + 100:
                            dice_states[i] = not dice_states[i]
            elif game_over and restart_rect.collidepoint(x, y):
                # Restart the game
                dice_values = [random.randint(1, 6) for _ in range(3)]
                dice_states = [False, False, False]
                rolls_left = 3
                game_over = False
                game_started = False

    screen.fill(BLACK)  # Set the background to black

    if game_started:  # Afficher les dés uniquement lorsque le jeu a démarré
        draw_dice(screen, dice_values, dice_states)

    if game_over:
        if check_combination(dice_values):
            display_message(screen, "You win!", font, WHITE)
        else:
            display_message(screen, "You lose!", font, WHITE)
        pygame.draw.rect(screen, GREEN, restart_rect, border_radius=button_radius)
        restart_text = font.render('Restart', True, BLACK)
        screen.blit(restart_text, (restart_rect.x + 30, restart_rect.y + 10))
    else:
        if not game_started:
            pygame.draw.rect(screen, GREEN, start_rect, border_radius=button_radius)
            start_text = font.render('Start try', True, BLACK)
            screen.blit(start_text, (start_rect.x + 50, start_rect.y + 10))
        else:
            # Draw the button
            pygame.draw.rect(screen, GREEN, button_rect, border_radius=button_radius)
            button_text = font.render('Roll', True, BLACK)
            screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

            display_message(screen, f"Rolls left: {rolls_left}", font, WHITE)
            instruction_text = font.render("Click on a die to save it", True, WHITE)
            screen.blit(instruction_text, (400 - instruction_text.get_width() // 2, 100))
    pygame.display.flip()

pygame.quit()
