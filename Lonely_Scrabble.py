"""
@copyright (c) 2024 Eshita Kulai. All rights reserved.
Use is subjected to license terms

The following code is responsible for Lonely Scrabble's functionality.
Do not tamper the code as it can cause detrimental effects to the game.
"""
import pygame
from gc import collect
import pandas as pd
from random import sample
from sys import exit

# Initializes Pygame and the Pygame Screen
pygame.init()
pygame_screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Lonely Scrabble")
pygame_clock = pygame.time.Clock()
color_palette = [pygame.Color('#3F2842'), pygame.Color('#6B5167'), pygame.Color('#97798B'), pygame.Color('#C2A2B0'), pygame.Color('#EECAD4')]

# Variables that are CONSTANTLY used for the game's functionality
scenario: str = 'TITLE'
background = pygame.Rect(0, 0, 800, 800)
current_word:str = ''
all_current_words: list = []
score:int = 0
reshuffles_left: int = 3
start_time: int = 30
remaining_time: int = start_time

all_letters_csv = pd.read_csv("C:\Text_Files_To_Manipulate\All_Words.csv").values
current_letters: list = sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10)
notification:str = ''

timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)

# All text fonts that are used
small_text = pygame.font.Font('C:\\Notes\\Intro_to_Pygame\\Pixeltype.ttf', 60)
big_text = pygame.font.Font('C:\\Notes\\Intro_to_Pygame\\Pixeltype.ttf', 100)
smaller_text = pygame.font.Font('C:\\Notes\\Intro_to_Pygame\\Pixeltype.ttf', 40)

# The class is responsible for the buttons that are used to detect player's inputs
class Button(pygame.sprite.Sprite):
    def __init__(self, destination: str, caption: str, pos:tuple, sizePos: tuple, used_font):
        super().__init__()
        self.image = pygame.Surface(sizePos)  # Mandatory for the class to run without Exceptions
        self.rect = pygame.Rect(pos, sizePos)  # Mandatory for the class to run without Exceptions

        # Additional Variables
        self.destination = destination
        self.caption = caption
        self.colors = [color_palette[3], color_palette[2]]
        self.colors_index = 1
        self.used_font = used_font
        self.sizePos = sizePos

    # Sets the caption of the Button
    def set_title(self, caption):
        self.caption = caption
        self.image.fill(self.colors[self.colors_index])
        txt = self.used_font.render(caption, False, color_palette[0])
        txt_rect = txt.get_rect(size=self.sizePos)
        self.image.blit(txt, txt_rect)

    # checks for collision with the mouse. Returns True if mouse is on the button
    def is_collision(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    # returns the scenario variable
    def get_destination(self) -> str: return self.destination

    # sets the color whenever the mouse moves over the button
    def set_color(self): self.colors_index = 0 if self.is_collision() else 1

    """
    @override pygame.sprite.Sprite
    updates the title and color of the button in one pygame.time.Clock tick
    """
    def update(self):
        self.set_title(self.caption)
        self.set_color()

class KeyButtons(pygame.sprite.Sprite):
    def __init__(self, position: tuple, letter1: str):
        super().__init__()
        self.image = pygame.Surface((120, 120))
        self.rect = pygame.Rect(position, (120, 120))

        self.colors = [color_palette[1], color_palette[2], pygame.Color('#FFFDD0')]
        self.colors_index = 0
        self.letter1 = letter1

    # sets the letter in the box
    def set_letter(self):
        txt = big_text.render(self.letter1, False, color_palette[0])
        txt_rect = txt.get_rect(center=(65, 70))
        self.image.blit(txt, txt_rect)

    # fills the image in the color
    def fill_image(self): self.image.fill(self.colors[self.colors_index])

    # checks for collision with the mouse
    def is_collision_with_mouse(self) -> bool: return self.rect.collidepoint(pygame.mouse.get_pos())

    # sets the letter that is in the box
    def set_keyLetter(self, new_letter: str): self.letter1 = new_letter

    # returns the letter that is in the box
    def return_keyLetter(self) -> str: return self.letter1

    # sets the color of the letter button
    def set_index(self, index1:int): self.colors_index = index1

    # gets the color of the letter button
    def get_index(self) -> int: return self.colors_index

    def update(self):
        self.fill_image()
        self.set_letter()

# ALL Functions

# Changes the scenario based on what button is pressed
def set_scenario(sprite_group):
    global scenario
    for sprite1 in sprite_group:
        if sprite1.is_collision(): scenario = sprite1.get_destination()

# changes the letters whenever the reshuffle button is pressed
def change_letters(key_buttons):
    global current_letters
    current_letters = sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10)
    for i, val in enumerate(key_buttons): val.set_keyLetter(current_letters[i])

# changes the color based on what letter the player has selected
def check_buttons(sprite_group):
    global current_word, notification
    for letter_key in sprite_group:
        if letter_key.is_collision_with_mouse():
            notification = ''
            if letter_key.get_index() == 0:
                current_word += letter_key.return_keyLetter()
                letter_key.set_index(2)
            else:
                current_word = current_word.replace(letter_key.return_keyLetter(), '')
                letter_key.set_index(0)

# calculates the score of a word that is entered
def calculate_score(word) -> int:
    sum1: int = 0
    for s1 in word:
        if s1 in 'aeiousltnr': sum1 += 1
        elif s1 in 'dg': sum1 += 2
        elif s1 in 'bcmp': sum1 += 3
        elif s1 in 'fhvwy': sum1 += 4
        elif s1 == 'k': sum1 += 5
        elif s1 in 'jx': sum1 += 6
        else: sum1 += 10
    return sum1

# manages the game based on the player's inputs
def operations_on_game(sprite_group, key_buttons):
    global current_word, reshuffles_left, all_letters_csv, all_current_words, notification, score
    for c in sprite_group:
        if c.rect.collidepoint(pygame.mouse.get_pos()):
            match c.get_destination():
                case 'DELETE':
                    pass
                case 'RESHUFFLE':
                    if reshuffles_left > 0:
                        change_letters(key_buttons)
                        reshuffles_left -= 1
                        c.set_title(f'Reshuffle Left: {reshuffles_left}')
                case _:
                    current_word = current_word.lower()
                    if current_word not in all_letters_csv:
                        notification = "No Such Word Exists"
                    elif current_word in all_current_words:
                        notification = "You already Entered this word!"
                    else:
                        notification = ''
                        all_current_words.append(current_word)
                        score += calculate_score(current_word)
            current_word = ''
            for i in key_buttons: i.set_index(0)

# changes the time based on what button is pressed in the game. Nothing is displayed on the screen
def change_time(sprite_group):
    global start_time
    for sprite2 in sprite_group:
        if sprite2.is_collision():
            start_time = int(sprite2.get_destination())


# Title Screen Surface and Rect
title_screen = big_text.render("_.:'Lonely Scrabble':._", False, color_palette[0])
title_screen_rect = title_screen.get_rect(centerx=400, y=60)

# Buttons that are shown in the Title Screen
title_buttons = pygame.sprite.Group()
title_buttons.add(Button('START','Begin Game', (190, 200), (400, 150), big_text))
title_buttons.add(Button('SETTINGS','Settings', (190, 400), (400, 150), big_text))
title_buttons.add(Button('QUIT', 'Quit Game', (190, 600), (400, 150), big_text))

# Setting Title Surface and Rect
settings_title = big_text.render('--Settings--', False, color_palette[0])
setting_title_rect = settings_title.get_rect(centerx=400, y=60)

# Buttons that are shown in the Settings Screen
settings_buttons = pygame.sprite.GroupSingle()
settings_buttons.add(Button('TITLE', 'Go Back', (190, 600), (400, 150), big_text))

change_time_buttons = pygame.sprite.Group()
change_time_buttons.add(Button('30', '30 sec.', (80, 300), (200, 80), small_text))
change_time_buttons.add(Button('45', '45 sec.', (300, 300), (200, 80), small_text))
change_time_buttons.add(Button('60', '60 sec.', (520, 300), (200, 80), small_text))

# Start Screen Title & How-to-Play text
how_to_play_title = big_text.render('_.oO-How to Play-Oo._', False, color_palette[0])
how_to_play_rect = how_to_play_title.get_rect(centerx=400, y=60)
HTP_text: list = """You will be given 10 letters. Your 
goal is to make as many letters as
you can in the given time. You can 
reshuffle and get new letters 3 
times by pressing the 'reshuffle 
letters' button. You cannot have 
variants of the same word.""".splitlines()

# Buttons that are present in the How-to-Play Screen
start_buttons = pygame.sprite.Group()
start_buttons.add(Button("TITLE", 'Go Back', (40, 600), (330, 150), big_text))
start_buttons.add(Button('GAME', 'Start', (420, 600), (330, 150), big_text))

# Current_Word Text Surface and Rect that represent the word that the player's inputs
current_word_text = None
current_word_text_rect = None

# Buttons that are present in the game screen
Check_buttons = pygame.sprite.Group()
Check_buttons.add(Button("RIGHT", 'C', (670, 375), (50, 50), smaller_text))
Check_buttons.add(Button("DELETE", 'X', (730, 375), (50, 50), smaller_text))
Check_buttons.add(Button("RESHUFFLE", f'Reshuffle Left: {reshuffles_left}', (25, 363), (225, 75), smaller_text))

# The letters that are present in the game
letter_choices = pygame.sprite.Group()
starting_pos: int = 20
vertical_pos: int = 485
for letter in current_letters:
    if starting_pos > 780:
        starting_pos = 20
        vertical_pos += 170
    letter_choices.add(KeyButtons((starting_pos, vertical_pos), letter))
    starting_pos += 160

# Buttons that are present in the Finished Screen
finished_buttons = pygame.sprite.Group()
finished_buttons.add(Button('QUIT', 'Quit Game', (50, 500), (300, 200), big_text))
finished_buttons.add(Button('TITLE', 'Back', (450, 500), (300, 200), big_text))


# MAIN GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == timer_event:
            if remaining_time == 1:
                scenario = 'DONE'
            else:
                remaining_time -= 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            match scenario:
                case 'TITLE':
                    set_scenario(title_buttons)
                case 'SETTINGS':
                    set_scenario(settings_buttons)
                    change_time(change_time_buttons)
                case 'START':
                    set_scenario(start_buttons)
                case "GAME":
                    check_buttons(letter_choices)
                    operations_on_game(Check_buttons, letter_choices)
                case "DONE":
                    set_scenario(finished_buttons)

    pygame_screen.fill(pygame.Color(color_palette[4]), background)
    match scenario:
        case "TITLE":
            pygame_screen.blit(title_screen, title_screen_rect)
            title_buttons.draw(pygame_screen)
            title_buttons.update()
            remaining_time = start_time
        case 'START':
            reshuffles_left = 3
            for index, c in enumerate(Check_buttons):
                if index == 2: c.set_title(f'Reshuffles Left: {reshuffles_left}')

            pygame_screen.blit(how_to_play_title, how_to_play_rect)
            y_pos:int = 200
            for s in HTP_text:
                surf = small_text.render(s, False, color_palette[1])
                surf_rect = surf.get_rect(center=(400, y_pos))
                pygame_screen.blit(surf, surf_rect)
                y_pos += 50

            for s in letter_choices: s.set_index(0)
            start_buttons.draw(pygame_screen)
            start_buttons.update()
            all_current_words.clear()
            current_word = ''
            score = 0
        case 'SETTINGS':
            pygame_screen.blit(settings_title, setting_title_rect)
            settings_buttons.draw(pygame_screen)
            settings_buttons.update()

            change_time_buttons.draw(pygame_screen)
            change_time_buttons.update()
        case 'QUIT':
            pygame.quit()
            exit()
        case 'GAME':
            pygame.draw.rect(pygame_screen, pygame.Color('#FFF4F2'), pygame.Rect(0, 350, 800, 200))
            pygame.draw.rect(pygame_screen, color_palette[3], pygame.Rect(0, 450, 800, 400))
            pygame.draw.rect(pygame_screen, color_palette[3], pygame.Rect(0,0,800, 50))

            current_word_text = small_text.render(current_word, False, color_palette[0])
            current_word_text_rect = current_word_text.get_rect(center=(450, 400))
            pygame_screen.blit(current_word_text, current_word_text_rect)

            x_pos, y_pos = 50, 60
            for s in all_current_words:
                surf = small_text.render(s, False, color_palette[1])
                surf_rect = surf.get_rect(topleft=(x_pos, y_pos))
                pygame_screen.blit(surf, surf_rect)
                if surf_rect.top > 290:
                    y_pos = 60
                    x_pos += 200
                else: y_pos += 40

            notification_surf = smaller_text.render(notification, False, color_palette[1])
            notification_rect = notification_surf.get_rect(topleft=(20, 10))

            score_surf = smaller_text.render(f'Score: {score}', False, color_palette[1])
            score_rect = score_surf.get_rect(topright=(780, 10))

            time_left_surf = smaller_text.render(f'{remaining_time} second(s) left', False, color_palette[1])
            time_left_rect = time_left_surf.get_rect(topleft=(420, 10))

            pygame_screen.blit(notification_surf, notification_rect)
            pygame_screen.blit(score_surf, score_rect)
            pygame_screen.blit(time_left_surf, time_left_rect)

            Check_buttons.draw(pygame_screen)
            Check_buttons.update()

            letter_choices.draw(pygame_screen)
            letter_choices.update()
        case 'DONE':
            final_score_txt = big_text.render(f'Final Score: {score}', False, color_palette[0])
            final_score_rect = final_score_txt.get_rect(center=(400,400))
            pygame_screen.blit(final_score_txt, final_score_rect)

            finished_buttons.draw(pygame_screen)
            finished_buttons.update()

    pygame.display.update()
    pygame_clock.tick(60)
    collect()

    