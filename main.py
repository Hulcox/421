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

# Initial values for dice and their states
dice_values = [random.randint(1, 6) for _ in range(3)]
dice_states = [False, False, False]  # False means the dice will be rolled
rolls_left = 3

running = True
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if button_rect.collidepoint(x, y) and not game_over:
                roll_dice_with_animation()
            elif not game_over:
                positions = [(200, 300), (350, 300), (500, 300)]
                for i, (px, py) in enumerate(positions):
                    if px < x < px + 100 and py < y < py + 100:
                        dice_states[i] = not dice_states[i]

    screen.fill(BLACK)  # Set the background to black
    draw_dice(screen, dice_values, dice_states)

    # Draw the button
    pygame.draw.rect(screen, GREEN, button_rect)
    button_text = font.render('Roll', True, BLACK)
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

    if game_over:
        if check_combination(dice_values):
            display_message(screen, "You win!", font, WHITE)
        else:
            display_message(screen, "You lose!", font, WHITE)
    else:
        display_message(screen, f"Rolls left: {rolls_left}", font, WHITE)
        instruction_text = font.render("Click on a die to save it", True, WHITE)
        screen.blit(instruction_text, (400 - instruction_text.get_width() // 2, 100))
    pygame.display.flip()

pygame.quit()
