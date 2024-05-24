import pygame
import random
from dice import draw_dice, roll_dice, animate_dice_roll
from utils import check_combination, display_message

# Initialize Pygame
pygame.init()

# Define colors
BLUE = (59, 85, 109)
WHITE = (255, 255, 255)
BLACK = (11, 22, 44)
GREEN = (95, 194, 186)
RED = (59, 85, 109)

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
start_x = (800 - start_width) // 2  # Center horizontally
start_y = 250  # Arbitrary vertical position

start_rect = pygame.Rect(start_x, start_y, start_width, start_height)

# Restart button configuration
restart_rect = pygame.Rect(300, 450, 200, 50)

# Retry and Quit button configuration
retry_rect = pygame.Rect(350, 450, 100, 50)
quit_rect = pygame.Rect(275, 520, 250, 50)
home_rect = pygame.Rect(275, 520, 250, 50)

# Initial values for dice and their states
dice_values = [random.randint(1, 6) for _ in range(3)]
dice_states = [False, False, False]  # False means the dice will be rolled
rolls_left = 3
try_count = 1

running = True
game_started = False
game_over = False
show_intro_page = True

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
    global game_started, show_intro_page
    game_started = True
    show_intro_page = False

def restart_game():
    global game_started, game_over, rolls_left, try_count
    game_started = False
    game_over = False
    rolls_left = 3  # Réinitialise le nombre de lancers restants
    try_count += 1  # Incrémente le nombre d'essais
    start_game()

def save_game_result(won, try_count):
    with open('game_result.txt', 'a') as file:
        result = "Gagné" if won else "Perdu"
        file.write(f"Résultat: {result}, Nombre d'essais: {try_count}\n")

def get_last_game_result():
    try:
        with open('game_result.txt', 'r') as file:
            lines = file.readlines()
            if lines:
                last_result = lines[-1].strip()
                return last_result
            else:
                return "Aucun résultat enregistré"
    except FileNotFoundError:
        return "Aucun résultat enregistré"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if show_intro_page:
                if start_rect.collidepoint(x, y):
                    start_game()
            elif not game_over:
                if button_rect.collidepoint(x, y):
                    roll_dice_with_animation()
                elif game_started:
                    positions = [(200, 300), (350, 300), (500, 300)]
                    for i, (px, py) in enumerate(positions):
                        if px < x < px + 100 and py < y < py + 100:
                            dice_states[i] = not dice_states[i]
            elif game_over:
                if retry_rect.collidepoint(x, y):
                    restart_game()
                elif home_rect.collidepoint(x, y):  # Bouton "Retourner à la page d'accueil"
                    show_intro_page = True
                    save_game_result(check_combination(dice_values), try_count)

    screen.fill(BLACK)  # Set the background to black

    if show_intro_page:
        display_message(screen, "Jeux du 421", font, WHITE)
        rules_text = font.render(f"Dernier {get_last_game_result()}", True, WHITE)  # Ajoutez les règles du jeu ici
        screen.blit(rules_text, (150, 350))
        pygame.draw.rect(screen, GREEN, start_rect, border_radius=button_radius)
        start_font = pygame.font.Font(None, 24)
        start_text = start_font.render('Commencer une partie', True, BLACK)
        text_x = start_rect.x + (start_rect.width - start_text.get_width()) // 2  # Centrer le texte horizontalement
        text_y = start_rect.y + (start_rect.height - start_text.get_height()) // 2  # Centrer le texte verticalement
        screen.blit(start_text, (text_x, text_y))
    else:
        if game_started:  # Afficher les dés uniquement lorsque le jeu a démarré
            draw_dice(screen, dice_values, dice_states)

        if game_over:
            if check_combination(dice_values):
                display_message(screen, "Tu as gagner!", font, WHITE)
            else:
                display_message(screen, "Tu as perdu!", font, WHITE)
            pygame.draw.rect(screen, GREEN, retry_rect, border_radius=button_radius)
            retry_font = pygame.font.Font(None, 24)
            retry_text = retry_font.render('Réessayer', True, BLACK)
            texte_x = retry_rect.x + (retry_rect.width - retry_text.get_width()) // 2  # Centrer le texte horizontalement
            texte_y = retry_rect.y + (retry_rect.height - retry_text.get_height()) // 2  # Centrer le texte verticalement
            screen.blit(retry_text, (texte_x, texte_y))
            pygame.draw.rect(screen, GREEN, home_rect, border_radius=button_radius)
            home_font = pygame.font.Font(None, 24)
            home_text_render = home_font.render('Retourner à la page d\'accueil', True, BLACK)
            text_x = home_rect.x + (home_rect.width - home_text_render.get_width()) // 2  # Centrer le texte horizontalement
            text_y = home_rect.y + (home_rect.height - home_text_render.get_height()) // 2  # Centrer le texte verticalement
            screen.blit(home_text_render, (text_x, text_y))
                
        else:
            if not game_started:
                pygame.draw.rect(screen, GREEN, start_rect, border_radius=button_radius)
                start_text = font.render('Start try', True, BLACK)
                screen.blit(start_text, (start_rect.x + 50, start_rect.y + 10))
            else:
                # Draw the button
                pygame.draw.rect(screen, GREEN, button_rect, border_radius=button_radius)
                button_text = font.render('Lancé', True, BLACK)
                screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

                display_message(screen, f"Lancé restant: {rolls_left}", font, WHITE)
                instruction_text = font.render("Pour gagner essaye d'avoir 4, 2 et 1 !", True, WHITE)
                screen.blit(instruction_text, (400 - instruction_text.get_width() // 2, 100))
                instruction_text = font.render("Cliquer sur un dé pour le sauvegarder", True, WHITE)
                screen.blit(instruction_text, (400 - instruction_text.get_width() // 2, 150))

                instruction_text = font.render(f"Nombre d'essaye: {try_count}", True, WHITE)
                screen.blit(instruction_text, (650 - instruction_text.get_width() // 2, 10))

    pygame.display.flip()

pygame.quit()
