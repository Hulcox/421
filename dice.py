import pygame
import random

# Define colors
BLUE = (59, 85, 109)
WHITE = (255, 255, 255)
BLACK = (11, 22, 44)
GREEN = (95, 194, 186)

# Function to draw a single die
def draw_single_die(screen, position, value, selected):
    die_size = 100
    corner_radius = 10  # Corner radius for the die

    x, y = position

    # Draw the square for the die with rounded corners
    pygame.draw.rect(screen, WHITE, (x, y, die_size, die_size), border_radius=corner_radius)
    if selected:
        pygame.draw.rect(screen, BLUE, (x, y, die_size, die_size), 5, border_radius=corner_radius)

    # Calculate the positions of the dots
    offset = die_size // 4
    centers = [
        (x + offset, y + offset),
        (x + 3 * offset, y + offset),
        (x + offset, y + 2 * offset),
        (x + 3 * offset, y + 2 * offset),
        (x + offset, y + 3 * offset),
        (x + 3 * offset, y + 3 * offset),
        (x + 2 * offset, y + 2 * offset)
    ]

    # Draw the dots based on the die value
    dots_to_draw = []
    if value == 1:
        dots_to_draw = [centers[6]]
    elif value == 2:
        dots_to_draw = [centers[0], centers[5]]
    elif value == 3:
        dots_to_draw = [centers[0], centers[6], centers[5]]
    elif value == 4:
        dots_to_draw = [centers[0], centers[1], centers[4], centers[5]]
    elif value == 5:
        dots_to_draw = [centers[0], centers[1], centers[4], centers[5], centers[6]]
    elif value == 6:
        dots_to_draw = [centers[0], centers[1], centers[2], centers[3], centers[4], centers[5]]

    for dot in dots_to_draw:
        pygame.draw.circle(screen, BLACK, dot, 10)

# Function to draw all dice
def draw_dice(screen, dice_values, dice_states):
    positions = [(200, 300), (350, 300), (500, 300)]
    for i, value in enumerate(dice_values):
        draw_single_die(screen, positions[i], value, dice_states[i])

# Function to roll dice
def roll_dice(dice_values, dice_states):
    for i in range(len(dice_values)):
        if not dice_states[i]:
            dice_values[i] = random.randint(1, 6)

# Function to animate dice roll
def animate_dice_roll(screen, dice_values, dice_states, font, button_rect, rolls_left):
    positions = [(200, 300), (350, 300), (500, 300)]
    for _ in range(15):  # Show 15 random frames
        for i in range(len(dice_values)):
            if not dice_states[i]:
                dice_values[i] = random.randint(1, 6)
        screen.fill(BLACK)  # Set the background to black
        draw_dice(screen, dice_values, dice_states)

        # Draw the button
        pygame.draw.rect(screen, GREEN, button_rect, border_radius=10)
        button_text = font.render('...', True, BLACK)
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

        pygame.display.flip()
        pygame.time.delay(100)  # Delay to show the animation
