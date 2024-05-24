
# Function to check if the dice values are a winning combination
def check_combination(dice_values):
    return sorted(dice_values) == [1, 2, 4]

# Function to display a message on the screen
def display_message(screen, message, font, color):
    text = font.render(message, True, color)
    screen.blit(text, (400 - text.get_width() // 2, 50))
