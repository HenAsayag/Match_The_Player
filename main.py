import pygame
import random
import time
import os
import json
import requests
import re
import math
import webbrowser

# Set the absolute path
PATH = os.path.abspath('.') + '/'

pygame.init()
pygame.mixer.init()
pygame.font.init()

# Screen dimensions for landscape mode
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)

# FPS settings
clock = pygame.time.Clock()
fps_font = pygame.font.SysFont(None, 30)
entering_name = False
player_name_font = pygame.font.Font(PATH + "nrkis.ttf", 30)  # הגדרת הפונט לשם השחקן
player_name_font_2 = pygame.font.Font(PATH + "OzradCLM.otf", 28)  # הגדרת הפונט לשם השחקן
def display_player_name(player_name):
    name_text = player_name_font.render(f"{player_name}  ", True, pygame.Color('white'))
    screen.blit(name_text, (1100, 0))


def display_high_score_rank(high_scores, player_high_score):
    sorted_high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)

    # מצא את המיקום של הציון הגבוה ביותר של השחקן
    player_rank = None
    for index, entry in enumerate(sorted_high_scores):
        if entry['score'] == player_high_score:
            player_rank = index + 1
            break

    # הצג את המיקום על המסך
    if player_rank is not None:
        rank_text = large_font.render(f"Your Rank: {player_rank}", True, WHITE)
        screen.blit(rank_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    else:
        rank_text = large_font.render("Your Rank: N/A", True, WHITE)
        screen.blit(rank_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


def clean_player_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\d', '', name)
    name = name.replace('_', ' ')
    name = name.strip()
    return name


def display_highscore(high_score):
    name_text = player_name_font.render(f"{high_score}", True, pygame.Color('white'))
    screen.blit(name_text, (1110, 37))

def display_player_name(player_name):
    cleaned_name = clean_player_name(player_name)
    name_text = player_name_font.render(f"{cleaned_name}  ", True, pygame.Color('white'))
    screen.blit(name_text, (1100, 0))
def display_fps():
    fps = str(int(clock.get_fps()))
    fps_text = fps_font.render(fps, True, pygame.Color('white'))
    screen.blit(fps_text, (10, 10))


def update_high_score(high_scores, new_score_entry):
    updated = False
    for score_entry in high_scores:
        if score_entry['name'] == new_score_entry['name']:
            if new_score_entry['score'] > score_entry['score']:
                score_entry['score'] = new_score_entry['score']
            updated = True

            break
    if not updated:
        high_scores.append(new_score_entry)
    high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)[:10]
    for index, score_entry in enumerate(high_scores):
        score_entry['rank'] = index + 1  # המיקום הוא האינדקס + 1
    return high_scores


def update_player_high_score(new_score):
    if new_score > player_data['high_score']:
        player_data['high_score'] = new_score
        save_player_data(player_data)


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define fonts
font = pygame.font.Font(PATH + "nrkis.ttf", 100)
button_font = pygame.font.Font(PATH + "nrkis.ttf", 72)
points_font = pygame.font.Font("OzradCLM.otf", 100)
input_font = pygame.font.Font(PATH + "nrkis.ttf", 50)
large_font = pygame.font.Font(PATH + "nrkis.ttf", 60)

# Load the card image
card_image = pygame.transform.scale(pygame.image.load(PATH + 'card.png'), (294,408))
tutorial_button_image = pygame.transform.scale(pygame.image.load(PATH + 'tutorial_button.png'), (348, 123))


# Virtual keyboard class
class VirtualKeyboard:
    def __init__(self, screen):
        self.screen = screen
        self.keys = [
            'ק', 'ר', 'א', 'ט', 'ו', 'ן', 'ם', 'פ', ']', '[',
            'ש', 'ד', 'ג', 'כ', 'ע', 'י', 'ח', 'ל', 'ך', 'ף',
            'ז', 'ס', 'ב', 'ה', 'נ', 'מ', 'צ', 'ת', 'ץ',
            '<-', 'SPACE'
        ]
        self.key_size = (80, 80)  # שינוי גודל המקשים
        self.margin = 21  # שינוי הרווח בין המקשים
        self.font = pygame.font.Font(PATH+"nrkis.ttf", 40)  # שינוי הפונט והגודל
        self.create_keys()

    def create_keys(self):
        self.key_rects = []
        row = -0.5
        col = 0
        total_width = 10 * (self.key_size[0] + self.margin) - self.margin  # חישוב רוחב המקלדת הכוללת
        start_x = (SCREEN_WIDTH - total_width) // 2  # חישוב מיקום התחלתי אופקי כדי למרכז את המקלדת

        for key in self.keys:
            if key == 'SPACE':
                x = start_x
                y = SCREEN_HEIGHT - (3 - row) * (self.key_size[1] + self.margin) - self.margin
                self.key_rects.append(
                    (pygame.Rect(x, y, total_width, self.key_size[1]), key))  # מקש ה-Space באורך כל השורה
                col += 10  # דילוג על כל העמודה עבור מקש ה-Space
            else:
                x = start_x + col * (self.key_size[0] + self.margin)
                y = SCREEN_HEIGHT - (3 - row) * (self.key_size[1] + self.margin) - self.margin
                self.key_rects.append((pygame.Rect(x, y, self.key_size[0], self.key_size[1]), key))
                col += 1
            if col > 9:
                col = 0
                row += 1

    def draw(self, screen):
        card_rect = self.card_image.get_rect(center=(self.x, self.y))
        screen.blit(self.card_image, card_rect)
        player_image_rect = self.image.get_rect(center=card_rect.center)
        screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2 - 10))

    def get_key_at_pos(self, pos):
        for rect, key in self.key_rects:
            if rect.collidepoint(pos):
                return 'BACKSPACE' if key == '←' else key  # הפיכת '←' ל-'BACKSPACE'
        return None

# Load images for modes
mode1_image = pygame.transform.scale(pygame.image.load(PATH + 'mode1.png'), (400, 400))
mode2_image = pygame.transform.scale(pygame.image.load(PATH + 'mode2.png'), (400, 400))

# Load background images for each mode
background_images = {
    'mode1': pygame.transform.scale(pygame.image.load(PATH + 'background1.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    'mode2': pygame.transform.scale(pygame.image.load(PATH + 'background2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
}

# Load home background image
home_background = pygame.transform.scale(pygame.image.load(PATH + 'home_background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
rules_image = pygame.transform.scale(pygame.image.load(PATH + 'rules.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load mode selection background image
mode_selection_background = pygame.transform.scale(pygame.image.load(PATH + 'mode_selection_background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
difficulty_selection_background = pygame.transform.scale(pygame.image.load(PATH + 'difficulty_selection_background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load mute and unmute button images
mute_image = pygame.transform.scale(pygame.image.load(PATH + 'mute.png'), (308,93))
unmute_image = pygame.transform.scale(pygame.image.load(PATH + 'unmute.png'),(308,93))

name_input_background = pygame.transform.scale(pygame.image.load(PATH + 'name_input_background.png').convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
high_score_background = pygame.transform.scale(pygame.image.load(PATH + 'high_score_background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sounds
sounds = {
    RED: pygame.mixer.Sound(PATH + 'sounds/red_sound.wav'),
    GREEN: pygame.mixer.Sound(PATH + 'sounds/green_sound.wav'),
    BLUE: pygame.mixer.Sound(PATH + 'sounds/blue_sound.wav'),
    YELLOW: pygame.mixer.Sound(PATH + 'sounds/yellow_sound.wav'),
    'error': pygame.mixer.Sound(PATH + 'sounds/error_sound.wav'),
}
Click = pygame.mixer.Sound(PATH + 'sounds/click.wav')

# Function to play sound
def play_sound(sound, muted):
    if not muted:
        pygame.mixer.stop()  # Stop any currently playing sounds
        sound.play()


# Function to load images from directories
def load_images_from_folder(folder):
    images = {}
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            images[filename.split('.')[0]] = img  # שים לב שהעובדה של הכוונה למאגר בלי שינוי גודל בשלב זה
    return images

# Load character images by color
character_images = load_images_from_folder((PATH + 'images/ISRAELILEAUGE'))


# Load corner images
corner_images = {
    RED: pygame.transform.scale(pygame.image.load(PATH + 'corner_red.png').convert_alpha(), (329, 297)),
    BLUE: pygame.transform.scale(pygame.image.load(PATH + 'corner_blue.png').convert_alpha(), (379, 339)),
    YELLOW: pygame.transform.scale(pygame.image.load(PATH + 'corner_yellow.png').convert_alpha(), (297, 325)),
    GREEN: pygame.transform.scale(pygame.image.load(PATH + 'corner_green.png').convert_alpha(), (327, 295))
}

class Ball:
    def __init__(self, color, character_images, card_image):
        self.color = color
        self.character = random.choice(list(character_images.keys()))
        self.original_image = character_images[self.character]
        self.image = pygame.transform.scale(self.original_image, (361, 246))
        self.card_image = card_image
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = SCREEN_HEIGHT - self.radius
        self.dy = get_initial_velocity()
        self.gravity = 0.8
        self.dragging = False

        # חיפוש שם הדמות המקורי לפי המיפוי
        self.original_character_name = None
        for hebrew_name, english_name in name_mapping.items():
            if english_name.split('.')[0] == self.character:
                self.original_character_name = hebrew_name.replace(".png", "")
                break

        if self.original_character_name is None:
            print(f"Warning: Original character name not found for {self.character}")
        else:
            print(f"Original character name found: {self.original_character_name}")

        # בדיקה אם הדמות קיימת במפת הצבעים
        if self.original_character_name and self.original_character_name not in character_color_map:
            print(f"Warning: Character {self.original_character_name} not found in character_color_map")
        else:
            possible_colors = [color for color, points in character_color_map.get(self.original_character_name, [])]
            if self.color not in possible_colors:
                print(f"Warning: Character {self.original_character_name} color {self.color} does not match any color in character_color_map")

    def draw(self, screen):
        card_rect = self.card_image.get_rect(center=(self.x, self.y))
        screen.blit(self.card_image, card_rect)
        player_image_rect = self.image.get_rect(center=card_rect.center)
        screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2 - 10))

        cleaned_name = clean_player_name(self.original_character_name or self.character)
        player_name_text = player_name_font_2.render(cleaned_name[::-1], True, WHITE)
        name_text_rect = player_name_text.get_rect(center=(self.x, self.y + card_rect.height // 2 - 58))
        screen.blit(player_name_text, name_text_rect)

    def create_new_ball(color, character_images, card_image):
        ball = Ball(color, character_images, card_image)
        ball.x = random.randint(ball.radius, SCREEN_WIDTH - ball.radius)
        ball.y = random.randint(ball.radius, SCREEN_HEIGHT - ball.radius)

        # בדוק אם שם הדמות קיים במפת הצבעים לפי השם המקורי בעברית
        if ball.original_character_name not in character_color_map:
            print(f"Warning: Character {ball.original_character_name} not found in character_color_map")
        else:
            ball.color = random.choice([color for color, points in character_color_map[ball.original_character_name]])

        if selected_difficulty == 'impossible':
            ball.gravity = 0.5  # האטת הכדור ברמה הבלתי אפשרית
        return ball
    def move(self):
        if not self.dragging:
            self.y += self.dy
            self.dy += self.gravity  # Apply gravity

    def has_fallen_off_screen(self):
        return self.y - self.radius > SCREEN_HEIGHT

    def snap_to_corner(self):
        MARGIN = 50  # מרחק מקסימלי למרכז הפינה

        snapped = False
        for corner_name, (x1, y1, width, height, color) in corners.items():
            # חשב את המרכז של הפינה
            corner_center_x = x1 + width // 2
            corner_center_y = y1 + height // 2

            # חשב את המרחק בין מרכז הקלף למרכז הפינה
            distance = math.hypot(self.x - corner_center_x, self.y - corner_center_y)

            if distance <= MARGIN and self.color == color:
                # אם המרחק קטן מהמקסימום המותר, קבע את הקלף במרכז הפינה
                self.x = corner_center_x
                self.y = corner_center_y
                snapped = True
                break

        if not snapped:
            # אם לא קיימת התאמה לפינה, השאר את הקלף במקום רנדומלי
            self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
            self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)

    def is_in_correct_corner(self):
        MARGIN = 50  # מרחק מקסימלי למרכז הפינה

        for corner_name, (x1, y1, width, height, color) in corners.items():
            # חשב את המרכז של הפינה
            corner_center_x = x1 + width // 2
            corner_center_y = y1 + height // 2

            # חשב את המרחק בין מרכז הקלף למרכז הפינה
            distance = math.hypot(self.x - corner_center_x, self.y - corner_center_y)

            if distance <= MARGIN and self.color == color:
                return True
        return False

    def has_fallen_off_screen(self):
        return self.y - self.radius > SCREEN_HEIGHT

def create_parallel_balls(num_balls, color, character_images, card_image):
    balls = []
    for _ in range(num_balls):
        ball = create_new_ball(color, character_images, card_image)
        balls.append(ball)
    return balls

# Define corner areas (larger size)
CORNER_SIZE = 310  # Increase size to match image corners

corners = {
    "top_left": (0, 0, CORNER_SIZE, CORNER_SIZE, RED),
    "top_right": ((SCREEN_WIDTH - CORNER_SIZE) + 15, 0, CORNER_SIZE, CORNER_SIZE, YELLOW),
    "bottom_left": (0, (SCREEN_HEIGHT - CORNER_SIZE) - 25, CORNER_SIZE, CORNER_SIZE, BLUE),
    "bottom_right": ((SCREEN_WIDTH - CORNER_SIZE) - 16, (SCREEN_HEIGHT - CORNER_SIZE) + 13, CORNER_SIZE, CORNER_SIZE, GREEN)
}
name_mapping ={"אאוג'ן_טריקה.png": 'image_1.png', 'אבי_בנימין_(כדורגלן).png': 'image_2.png', 'אבישי_כהן_(כדורגלן).png': 'image_3.png', 'אברהם_בית_הלוי.png': 'image_4.png', 'אדוארדו_גררו.png': 'image_5.png', 'אדווין_גיאסי.png': 'image_6.png', 'אדי_גוטליב.png': 'image_7.png', 'אהרן_אמר.png': 'image_8.png', 'אובונג_מוזס_אקפאי.png': 'image_9.png', 'אוסקר_גלוך.png': 'image_10.png', 'אופק_ביטון.png': 'image_11.png', 'אור_אינברום.png': 'image_12.png', 'אורי_אוזן.png': 'image_13.png', 'אושר_דוידה.png': 'image_14.png', 'אושרי_גיטא.png': 'image_15.png', 'איאד_אבו_עביד.png': 'image_16.png', 'איבזיטו_אוגבונה.png': 'image_17.png', 'איברהים_באנגורה.png': 'image_18.png', 'איוואן_גצקו.png': 'image_19.png', 'אייל_בן_עמי.png': 'image_20.png', "אייל_ברקוביץ'.png": 'image_21.png', 'אייל_גולסה.png': 'image_22.png', 'איציק_כהן_(בלם).png': 'image_23.png', 'איתן_טיבי.png': 'image_24.png', 'אלון_חרזי.png': 'image_25.png', 'אלי_אוחנה.png': 'image_26.png', 'אלי_דסה.png': 'image_27.png', 'אלי_כהן_(מאמן).png': 'image_28.png', 'אליניב_ברדה.png': 'image_29.png', 'אליסון_דוס_סנטוס_(כדורגלן).png': 'image_30.png', 'אלירן_דנין.png': 'image_31.png', 'אלירן_חודדה.png': 'image_32.png', 'אלכסנדר_אובארוב.png': 'image_33.png', "אלכסנדר_בולייביץ'.png": 'image_34.png', "אלן_אוז'בולט.png": 'image_35.png', 'אנדרס_טונייס.png': 'image_36.png', 'אנתוני_אנאן.png': 'image_37.png', 'אסי_דומב.png': 'image_38.png', 'אפולה_אדל.png': 'image_39.png', 'ארון_אולנארה.png': 'image_40.png', 'אריק_בנדו.png': 'image_41.png', 'בוני_גינצבורג.png': 'image_42.png', 'בירם_כיאל.png': 'image_43.png', 'בן_ביטון.png': 'image_44.png', 'ברוך_דגו.png': 'image_45.png', 'ברק_בדש.png': 'image_46.png', 'ברק_יצחקי.png': 'image_47.png', 'ברק_לוי.png': 'image_48.png', "ג'וניור_ויסה.png": 'image_49.png', "ג'ונתן_אסוס.png": 'image_50.png', "ג'ורג'ה_יובאנוביץ'.png": 'image_51.png', 'גדי_ברומר.png': 'image_52.png', 'גודסוויי_דוניו.png': 'image_53.png', 'גיא_אסולין.png': 'image_54.png', 'גיא_בדש.png': 'image_55.png', 'גיא_חיימוב.png': 'image_56.png', 'גיורא_אנטמן.png': 'image_57.png', 'גיל_יצחק.png': 'image_58.png', 'גילי_ורמוט.png': 'image_59.png', 'גל_אלברמן.png': 'image_60.png', 'דאגלס_דה_סילבה.png': 'image_61.png', 'דדי_בן_דיין.png': 'image_62.png', 'דוד_אמסלם_(כדורגלן).png': 'image_63.png', 'אברהם_גרנט.png': 'image_64.png', 'דודו_אוואט.png': 'image_65.png', 'דודו_ביטון.png': 'image_66.png', 'דודו_דהאן.png': 'image_67.png', 'דור_אלו.png': 'image_68.png', 'דור_חוגי.png': 'image_69.png', 'דור_כוכב.png': 'image_70.png', 'דיוגו_ורדשקה.png': 'image_71.png', 'דינו_אנדלובו.png': 'image_72.png', 'דן_איינבינדר.png': 'image_73.png', 'דן_ביטון_(כדורגלן).png': 'image_74.png', 'דני_איימוס.png': 'image_75.png', "דני_הוצ'קו.png": 'image_76.png', 'דניאל_בריילובסקי.png': 'image_77.png', 'דניאל_דה_רידר.png': 'image_78.png', 'דניאל_הבר.png': 'image_79.png', 'דניאל_פרץ.png': 'image_80.png', 'דניאל_פרץ_(2000).png': 'image_81.png', 'דניל_לסובוי.png': 'image_82.png', 'דנילו_אספרייה.png': 'image_83.png', 'דרק_בואטנג.png': 'image_84.png', 'וינסנט_אניימה.png': 'image_85.png', "ז'והאן_אודל.png": 'image_86.png', "ז'ורז'יניו_(1991).png": 'image_87.png', "זאב_חיימוביץ'.png": 'image_88.png', 'חיים_מגרלשוילי.png': 'image_89.png', 'חסן_אבו_זייד.png': 'image_90.png', "חסן_בדג'ייב.png": 'image_91.png', 'טל_בן-חיים_(1982).png': 'image_92.png', 'טל_בן-חיים_(1989).png': 'image_93.png', "יואב_ג'ראפי.png": 'image_94.png', 'יואב_זיו.png': 'image_95.png', 'יוחנן_וולך.png': 'image_96.png', 'יונתן_כהן.png': 'image_97.png', 'יוסי_אבוקסיס.png': 'image_98.png', 'יוריס_ואן_אובריים.png': 'image_99.png', 'יניב_בריק.png': 'image_100.png', 'יעקב_אסייג.png': 'image_101.png', 'ירו_בלו.png': 'image_102.png', 'ירוסלב_באקו.png': 'image_103.png', 'כפיר_אדרי.png': 'image_104.png', 'כפיר_אודי.png': 'image_105.png', 'כריסטיאן_אלברס.png': 'image_106.png', 'לואיס_הרננדס_רודריגס.png': 'image_107.png', 'ליאור_אסולין.png': 'image_108.png', 'ליביו_אנטל.png': 'image_109.png', 'ליוואי_גארסיה.png': 'image_110.png', 'מאור_בוזגלו.png': 'image_111.png', 'מארק_ואליינטה.png': 'image_112.png', 'מואנס_דבור.png': 'image_113.png', 'מוחמד_אבו_פאני.png': 'image_114.png', 'מוחמד_גדיר.png': 'image_115.png', 'מוחמד_כליבאת.png': 'image_116.png', 'מוטי_איוניר.png': 'image_117.png', 'מוטי_ברשצקי.png': 'image_118.png', 'מיכאיל_אוסינוב.png': 'image_119.png', 'מיכאל_זנדברג.png': 'image_120.png', 'מיקאל_אלפונס.png': 'image_121.png', 'מיקו_בלו.png': 'image_122.png', 'מני_בסון.png': 'image_123.png', "מקסים_גרצ'קין.png": 'image_124.png', 'מרלון_דה_חסוס.png': 'image_125.png', "מרקו_יאנקוביץ'.png": 'image_126.png', 'משה_בן_לולו.png': 'image_127.png', 'מתן_אוחיון.png': 'image_128.png', 'נטע_לביא.png': 'image_129.png', 'ניב_זריהן.png': 'image_130.png', "ניר_דוידוביץ'.png": 'image_131.png', 'סטיב_גורי.png': 'image_132.png', 'סטפנוס_אתנסיאדיס.png': 'image_133.png', 'עאיד_חבשי.png': 'image_134.png', 'עדן_בן_בסט.png': 'image_135.png', 'עודד_בלוש.png': 'image_136.png', 'עומר_אצילי.png': 'image_137.png', 'עומר_בוקסנבוים.png': 'image_138.png', 'עומר_דמארי.png': 'image_139.png', 'עומרי_גלזר.png': 'image_140.png', 'עופר_טלקר.png': 'image_141.png', 'עידן_ורד.png': 'image_142.png', 'עידן_טל.png': 'image_143.png', 'עמית_ביטון.png': 'image_144.png', 'עמרי_אפק.png': 'image_145.png', 'ערן_לוי_(כדורגלן).png': 'image_146.png', 'פבלו_ברנדאן.png': 'image_147.png', 'פטריק_טומאסי.png': 'image_148.png', 'פלמן_גלבוב.png': 'image_149.png', "צ'יקו_אופואדו.png": 'image_150.png', 'צבי_ארליך.png': 'image_151.png', 'קייס_גאנם.png': 'image_152.png', 'קמיל_ואצק.png': 'image_153.png', 'קרלוס_גרסיה.png': 'image_154.png', 'רביד_גזל.png': 'image_155.png', 'רדובן_הרומאדקו.png': 'image_156.png', 'רודי_חדד.png': 'image_157.png', 'רונאלדו_ואסקס.png': 'image_158.png', 'רוני_לוי.png': 'image_159.png', 'רועי_גורדנה.png': 'image_160.png', 'רז_מאיר.png': 'image_161.png', "ריצ'מונד_בואצ'י.png": 'image_162.png', 'רמי_אבו_לבן.png': 'image_163.png', 'רן_אבוקרט.png': 'image_164.png', 'רן_בנימין.png': 'image_165.png', 'רפי_אוסמו.png': 'image_166.png', 'שאבייר_אנדרסון.png': 'image_167.png', 'שביט_אלימלך.png': 'image_168.png', 'שולי_גילארדי.png': 'image_169.png', 'שון_גולדברג.png': 'image_170.png', 'שון_וייסמן.png': 'image_171.png', 'שחר_הירש.png': 'image_172.png', 'שי_אליאס.png': 'image_173.png', 'שי_הולצמן.png': 'image_174.png', 'שלום_אביטן.png': 'image_175.png', 'שלומי_אזולאי_(קשר).png': 'image_176.png', 'שלומי_ארבייטמן.png': 'image_177.png', 'שמעון_גרשון.png': 'image_178.png', 'שרן_ייני.png': 'image_179.png', 'תום_אלמדון.png': 'image_180.png'}

# Characters to colors mapping with scores
character_color_map = {
    "אאוג'ן_טריקה": [(BLUE, 100)],
    "אבי_בנימין_(כדורגלן)": [(RED, 100)],
    "אבישי_כהן_(כדורגלן)": [(YELLOW, 100), (BLUE, 14)],
    "אברהם_בית_הלוי": [(RED, 100), (BLUE, 9)],
    "אדוארדו_גררו": [(YELLOW, 100)],
    "אדווין_גיאסי": [(YELLOW, 100)],
    "אדי_גוטליב": [(RED, 100), (YELLOW, 22)],
    "אהרן_אמר": [(GREEN, 100)],
    "אובונג_מוזס_אקפאי": [(GREEN, 100)],
    "אוסקר_גלוך": [(BLUE, 100)],
    "אופק_ביטון": [(RED, 100)],
    "אור_אינברום": [(YELLOW, 100), (RED, 100)],
    "אורי_אוזן": [(GREEN, 100), (RED, 66), (YELLOW, 33), (BLUE, 33)],
    "אושר_דוידה": [(RED, 100), (BLUE, 25)],
    "אושרי_גיטא": [(GREEN, 100)],
    "איאד_אבו_עביד": [(RED, 100), (GREEN, 40)],
    "איבזיטו_אוגבונה": [(RED, 100)],
    "איברהים_באנגורה": [(YELLOW, 100)],
    "איוואן_גצקו": [(GREEN, 100)],
    "אייל_ברקוביץ'": [(GREEN, 100), (BLUE, 25)],
    "אייל_גולסה": [(BLUE, 100), (GREEN, 77)],
    "איציק_כהן_(בלם)": [(GREEN, 100)],
    "איתן_טיבי": [(BLUE, 100), (YELLOW, 50)],
    "אלון_חרזי": [(YELLOW, 100), (GREEN, 10)],
    "אלי_אוחנה": [(YELLOW, 100)],
    "אלי_דסה": [(YELLOW, 100), (BLUE, 83)],
    "אלי_כהן_(מאמן)": [(GREEN, 100), (YELLOW, 37)],
    "אליניב_ברדה": [(GREEN, 100), (RED, 100)],
    "אליסון_דוס_סנטוס_(כדורגלן)": [(GREEN, 100)],
    "אלירן_דנין": [(YELLOW, 100), (GREEN, 25), (RED, 25)],
    "אלירן_חודדה": [(YELLOW, 100)],
    "אלכסנדר_אובארוב": [(BLUE, 100)],
    "אלכסנדר_בולייביץ'": [(RED, 100)],
    "אלן_אוז'בולט": [(RED, 100)],
    "אנדרס_טונייס": [(YELLOW, 100)],
    "אנתוני_אנאן": [(YELLOW, 100)],
    "אסי_דומב": [(RED, 100), (YELLOW, 33)],
    "אפולה_אדל": [(RED, 100)],
    "ארון_אולנארה": [(YELLOW, 100)],
    "אריק_בנדו": [(GREEN, 100), (YELLOW, 44)],
    "בוני_גינצבורג": [(BLUE, 100), (GREEN, 75), (YELLOW, 25)],
    "בירם_כיאל": [(GREEN, 100)],
    "בן_ביטון": [(RED, 100), (BLUE, 20), (YELLOW, 20)],
    "ברוך_דגו": [(RED, 100), (BLUE, 33)],
    "ברק_בדש": [(BLUE, 100), (RED, 50)],
    "ברק_יצחקי": [(BLUE, 100), (YELLOW, 90)],
    "ברק_לוי": [(BLUE, 100)],
    "ג'וניור_ויסה": [(YELLOW, 100)],
    "ג'ונתן_אסוס": [(BLUE, 100)],
    "ג'ורג'ה_יובאנוביץ'": [(BLUE, 100)],
    "גדי_ברומר": [(BLUE, 100)],
    "גודסוויי_דוניו": [(GREEN, 100)],
    "גיא_אסולין": [(RED, 100)],
    "גיא_בדש": [(RED, 100)],
    "גיא_חיימוב": [(BLUE, 100), (GREEN, 27)],
    "גיורא_אנטמן": [(YELLOW, 100), (RED, 75), (GREEN, 50)],
    "גיל_יצחק": [(GREEN, 100), (RED, 100)],
    "גילי_ורמוט": [(RED, 100), (BLUE, 100), (GREEN, 50)],
    "גל_אלברמן": [(BLUE, 100), (GREEN, 100), (YELLOW, 50)],
    "דאגלס_דה_סילבה": [(RED, 100)],
    "דדי_בן_דיין": [(BLUE, 100), (RED, 66)],
    "דוד_אמסלם_(כדורגלן)": [(YELLOW, 100), (RED, 33)],
    "אברהם_גרנט": [(BLUE, 100)],
    "דודו_אוואט": [(GREEN, 100)],
    "דודו_ביטון": [(RED, 100), (BLUE, 66), (GREEN, 33)],
    "דודו_דהאן": [(RED, 100)],
    "דור_אלו": [(RED, 100)],
    "דור_חוגי": [(GREEN, 100), (RED, 33)],
    "דור_כוכב": [(GREEN, 100)],
    "דיוגו_ורדשקה": [(YELLOW, 100)],
    "דינו_אנדלובו": [(GREEN, 100)],
    "דן_איינבינדר": [(YELLOW, 100), (RED, 36), (BLUE, 27)],
    "דניאל_פרץ":[BLUE,100],
    "דן_ביטון_(כדורגלן)": [(BLUE, 100)],
    "דני_איימוס": [(RED, 100)],
    "דני_הוצ'קו": [(YELLOW, 100)],
    "דניאל_בריילובסקי": [(GREEN, 100)],
    "דניאל_דה_רידר": [(RED, 100)],
    "דניאל_הבר": [(GREEN, 100)],
    "דניאל_פרץ_(2000)": [(BLUE, 100)],
    "דניל_לסובוי": [(GREEN, 100)],
    "דנילו_אספרייה": [(YELLOW, 100)],
    "דרק_בואטנג": [(YELLOW, 100)],
    "וינסנט_אניימה": [(RED, 100), (BLUE, 40)],
    "ז'והאן_אודל": [(YELLOW, 100)],
    "ז'ורז'יניו_(1991)": [(YELLOW, 100)],
    "זאב_חיימוביץ'": [(RED, 100), (YELLOW, 66)],
    "חיים_מגרלשוילי": [(GREEN, 100), (YELLOW, 33), (BLUE, 16)],
    "חסן_אבו_זייד": [(BLUE, 100), (RED, 25)],
    "חסן_בדג'ייב": [(RED, 100)],
    "טל_בן-חיים_(1982)": [(BLUE, 100), (YELLOW, 57)],
    "טל_בן-חיים_(1989)": [(BLUE, 100), (RED, 25)],
    "יואב_ג'ראפי": [(RED, 100)],
    "יואב_זיו": [(BLUE, 100), (YELLOW, 71), (GREEN, 28)],
    "יוחנן_וולך": [(GREEN, 100)],
    "יונתן_כהן": [(BLUE, 100)],
    "יוסי_אבוקסיס": [(RED, 100), (YELLOW, 43)],
    "יוריס_ואן_אובריים": [(BLUE, 100)],
    "יניב_בריק": [(GREEN, 100)],
    "יעקב_אסייג": [(YELLOW, 100)],
    "ירו_בלו": [(GREEN, 100)],
    "ירוסלב_באקו": [(RED, 100)],
    "כפיר_אדרי": [(BLUE, 100), (YELLOW, 50), (RED, 50)],
    "כפיר_אודי": [(RED, 100)],
    "כריסטיאן_אלברס": [(YELLOW, 100)],
    "לואיס_הרננדס_רודריגס": [(BLUE, 100)],
    "ליאור_אסולין": [(YELLOW, 100), (RED, 66)],
    "ליביו_אנטל": [(RED, 100), (YELLOW, 33)],
    "ליוואי_גארסיה": [(YELLOW, 100)],
    "מאור_בוזגלו": [(GREEN, 100), (BLUE, 66), (YELLOW, 33), (RED, 33)],
    "מארק_ואליינטה": [(GREEN, 100)],
    "מואנס_דבור": [(BLUE, 100)],
    "מוחמד_אבו_פאני": [(GREEN, 100)],
    "מוחמד_גדיר": [(GREEN, 100)],
    "מוחמד_כליבאת": [(GREEN, 100)],
    "מוטי_איוניר": [(BLUE, 100), (RED, 14)],
    "מוטי_ברשצקי": [(RED, 100)],
    "מיכאיל_אוסינוב": [(BLUE, 100)],
    "מיכאל_זנדברג": [(GREEN, 100), (YELLOW, 80), (RED, 40)],
    "מיקאל_אלפונס": [(GREEN, 100)],
    "מיקו_בלו": [(BLUE, 100)],
    "מני_בסון": [(BLUE, 100)],
    "מקסים_גרצ'קין": [(YELLOW, 100)],
    "מרלון_דה_חסוס": [(GREEN, 100)],
    "מרקו_יאנקוביץ'": [(YELLOW, 100), (RED, 100)],
    "משה_בן_לולו": [(YELLOW, 100)],
    "מתן_אוחיון": [(GREEN, 100), (RED, 100)],
    "נטע_לביא": [(GREEN, 100)],
    "ניב_זריהן": [(YELLOW, 100), (RED, 100)],
    "ניר_דוידוביץ'": [(GREEN, 100)],
    "סטיב_גורי": [(BLUE, 100)],
    "סטפנוס_אתנסיאדיס": [(GREEN, 100)],
    "עאיד_חבשי": [(GREEN, 100)],
    "עדן_בן_בסט": [(GREEN, 100), (BLUE, 66), (RED, 16)],
    "עודד_בלוש": [(GREEN, 100)],
    "עומר_אצילי": [(YELLOW, 100), (BLUE, 100), (GREEN, 75)],
    "עומר_בוקסנבוים": [(GREEN, 100)],
    "עומר_דמארי": [(RED, 100), (GREEN, 50)],
    "עומרי_גלזר": [(GREEN, 100)],
    "עופר_טלקר": [(YELLOW, 100)],
    "עידן_ורד": [(YELLOW, 100), (GREEN, 60), (RED, 30)],
    "עידן_טל": [(YELLOW, 100), (GREEN, 80), (RED, 20)],
    "עמית_ביטון": [(RED, 100)],
    "עמרי_אפק": [(RED, 100), (YELLOW, 60), (GREEN, 60)],
    "ערן_לוי_(כדורגלן)": [(GREEN, 100), (YELLOW, 100), (BLUE, 25)],
    "פבלו_ברנדאן": [(YELLOW, 100)],
    "פטריק_טומאסי": [(YELLOW, 100)],
    "פלמן_גלבוב": [(YELLOW, 100)],
    "צ'יקו_אופואדו": [(BLUE, 100)],
    "צבי_ארליך": [(RED, 100)],
    "קייס_גאנם": [(RED, 100)],
    "קמיל_ואצק": [(GREEN, 100)],
    "קרלוס_גרסיה": [(BLUE, 100)],
    "רביד_גזל": [(GREEN, 100), (BLUE, 50)],
    "רדובן_הרומאדקו": [(GREEN, 100)],
    "רונאלדו_ואסקס": [(RED, 100)],
    "רוני_לוי": [(GREEN, 100), (YELLOW, 100)],
    "רועי_גורדנה": [(RED, 100)],
    "רז_מאיר": [(GREEN, 100), (RED, 10)],
    "ריצ'מונד_בואצ'י": [(YELLOW, 100)],
    "רמי_אבו_לבן": [(RED, 100)],
    "רן_אבוקרט": [(GREEN, 100)],
    "רן_בנימין": [(RED, 100)],
    "רפי_אוסמו": [(GREEN, 100)],
    "שאבייר_אנדרסון": [(GREEN, 100)],
    "שביט_אלימלך": [(RED, 100), (BLUE, 38)],
    "שולי_גילארדי": [(RED, 100)],
    "שון_גולדברג": [(BLUE, 100), (YELLOW, 40), (RED, 20), (GREEN, 20)],
    "שון_וייסמן": [(GREEN, 100)],
    "שחר_הירש": [(RED, 100), (GREEN, 66)],
    "שי_אליאס": [(RED, 100)],
    "שי_הולצמן": [(GREEN, 100), (YELLOW, 100)],
    "שלום_אביטן": [(YELLOW, 100), (RED, 66)],
    "שלומי_אזולאי_(קשר)": [(GREEN, 100), (BLUE, 42), (RED, 42), (YELLOW, 28)],
    "שלומי_ארבייטמן": [(GREEN, 100), (YELLOW, 33), (RED, 16)],
    "שמעון_גרשון": [(RED, 100), (YELLOW, 45)],
    "שרן_ייני": [(BLUE, 100)],
    "תום_אלמדון": [(GREEN, 100), (RED, 40)],

}

# Function to create a new ball
next_ball_time = 0
MAX_BALLS = 2  # Set the maximum number of balls

def create_new_ball(color, character_images, card_image):
    # יצירת כדור חדש
    ball = Ball(color, character_images, card_image)
    ball.x = random.randint(ball.radius, SCREEN_WIDTH - ball.radius)
    ball.y = random.randint(ball.radius, SCREEN_HEIGHT - ball.radius)
    if selected_difficulty == 'impossible':
        ball.gravity = 0.5  # האטת הכדור ברמה הבלתי אפשרית
    return ball


# Create rectangles for the buttons with increased length and space between them
save_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 700, SCREEN_HEIGHT // 2 -300), (400, 300))  # Adjusted position
continue_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 210), (400, 60))  # Adjusted position
input_rect = pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 120), (400, 100))  # Adjusted position
tutorial_button_rect = tutorial_button_image.get_rect(center=(SCREEN_WIDTH // 2 -450 , SCREEN_HEIGHT // 2 + 293))

# Game state variables
game_active = False
viewing_high_score = False
choosing_mode = False
choosing_difficulty = False
viewing_rules = False
high_score = 0
score = 0
points_change = 0
points_change_time = 0
game_duration = 60  # Game duration in seconds
selected_mode = None
selected_difficulty = None
muted = False
background_image = None  # Initialize background_image
input_active = False
input_text = ""
high_scores = []
dragging_ball = None  # משתנה למעקב אחר הכדור הנגרר ברמת "בלתי אפשרית"
high_score_display = 'easy'  # Start by displaying easy high scores

# Load high scores from file
# Load high scores from file
HIGH_SCORES_EASY_URL = 'https://api.github.com/gists/fc96578ab19c5acc1b8426a9b024377d'
HIGH_SCORES_HARD_URL = 'https://api.github.com/gists/c3f09bfb8e681d42a595fc47261077ae'
HIGH_SCORES_IMPOSSIBLE_URL = 'https://api.github.com/gists/655cfbffae4d025a6c003b85f404af6e'

# GitHub token for authentication
GITHUB_T_Example = 'Github_Token_Here'

# Headers for GitHub API requests
headers = {
    'Authorization': f'token {GITHUB_T_Example}',
    'Accept': 'application/vnd.github.v3+json'
}
def play_background_music():
    if not muted:
        pygame.mixer.music.load(PATH + 'background_music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # לנגן בלופ

def stop_background_music():
    pygame.mixer.music.stop()


def download_json(gist_url):
    response = requests.get(gist_url, headers=headers)
    response.raise_for_status()
    gist_data = response.json()
    file_content = next(iter(gist_data['files'].values()))['content']
    return json.loads(file_content)

def upload_json(gist_url, data):
    response = requests.get(gist_url, headers=headers)
    response.raise_for_status()
    gist_data = response.json()
    file_name = next(iter(gist_data['files'].keys()))
    update_data = {
        "files": {
            file_name: {
                "content": json.dumps(data, indent=4)
            }
        }
    }
    response = requests.patch(gist_url, headers=headers, data=json.dumps(update_data))
    response.raise_for_status()
    return response.json()

def load_high_scores():
    global high_scores_easy, high_scores_hard, high_scores_impossible
    try:
        high_scores_easy = download_json(HIGH_SCORES_EASY_URL)
    except Exception as e:
        print(f"Error loading high scores (easy): {e}")
        high_scores_easy = []

    try:
        high_scores_hard = download_json(HIGH_SCORES_HARD_URL)
    except Exception as e:
        print(f"Error loading high scores (hard): {e}")
        high_scores_hard = []

    try:
        high_scores_impossible = download_json(HIGH_SCORES_IMPOSSIBLE_URL)
    except Exception as e:
        print(f"Error loading high scores (impossible): {e}")
        high_scores_impossible = []

def save_high_scores():
    try:
        upload_json(HIGH_SCORES_EASY_URL, high_scores_easy)
    except Exception as e:
        print(f"Error saving high scores (easy): {e}")

    try:
        upload_json(HIGH_SCORES_HARD_URL, high_scores_hard)
    except Exception as e:
        print(f"Error saving high scores (hard): {e}")

    try:
        upload_json(HIGH_SCORES_IMPOSSIBLE_URL, high_scores_impossible)
    except Exception as e:
        print(f"Error saving high scores (impossible): {e}")

load_high_scores()

# Load and save player name and high score
PLAYER_DATA_FILE = 'player_data.json'

def load_player_data():
    if os.path.exists(PLAYER_DATA_FILE):
        with open(PLAYER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {'name': '', 'high_score': 0}

def save_player_data(player_data):
    with open(PLAYER_DATA_FILE, 'w') as file:
        json.dump(player_data, file)

player_data = load_player_data()

# Create the buttons
start_button_text = button_font.render("                             ", True, WHITE)
start_button_rect = start_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))

high_score_button_text = button_font.render("         ", True, WHITE)
high_score_button_rect = high_score_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

rules_button_text = button_font.render("       ", True, WHITE)
rules_button_rect = rules_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

mute_button_rect = mute_image.get_rect(center=(SCREEN_WIDTH - 165, SCREEN_HEIGHT - 70))

mode1_button_rect = mode1_image.get_rect(center=(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
mode2_button_rect = mode2_image.get_rect(center=(SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2))

easy_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 120), (350, 100))
hard_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2+20), (350, 100))
impossible_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 160), (350, 100))

# Create the back button
back_button_rect = pygame.Rect(550, 620, 150, 50).inflate(100, 20)  # Adjust the size and position as needed
back_button_text = button_font.render("      ", True, WHITE)

# Create virtual keyboard instance
virtual_keyboard = VirtualKeyboard(screen)
button_spacing = 20  # Adjust the spacing between buttons
button_y_start = 500  # Starting Y position for the buttons

high_score_easy_button_rect = pygame.Rect((5, 150), (200, 60))
high_score_hard_button_rect = pygame.Rect((5, 230), (200, 60))
high_score_impossible_button_rect = pygame.Rect((5, 310), (200, 60))

high_scores_easy_text = large_font.render("      ", True, WHITE)
high_scores_hard_text = large_font.render("      ", True, WHITE)
high_scores_impossible_text = large_font.render("       ", True, WHITE)

def draw_corners(ball):
    if ball.dragging:
        for corner_name, (x1, y1, width, height, color) in corners.items():
            if x1 <= ball.x <= x1 + width and y1 <= ball.y <= y1 + height:
                screen.blit(corner_images[color], (x1, y1))

def get_initial_velocity():
    if selected_difficulty == 'easy':
        return -29
    elif selected_difficulty == 'hard':
        return -19
    elif selected_difficulty == 'impossible':
        return -14  # Same as 'hard', but balls move in parallel
    return -10  # Default velocity

# Main loop
running = True
balls = []  # Initialize balls list
saved = False  # אפס את המשתנה לשמירה שלא בוצעה
key_repeat_delay = 300  # Delay in milliseconds before key repeat starts
key_repeat_interval = 50  # Interval in milliseconds between key repeats
play_background_music()
pygame.key.set_repeat(key_repeat_delay, key_repeat_interval)

# Display the name input screen if the player name is not set
if player_data['name'] == '':
    entering_name = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_active and not viewing_high_score and not choosing_mode and not viewing_rules and not entering_name and not choosing_difficulty:
            mouse_x, mouse_y = event.pos
            play_sound(Click,muted)

            if start_button_rect.collidepoint(mouse_x, mouse_y):
                choosing_mode = True
            elif high_score_button_rect.collidepoint(mouse_x, mouse_y):
                viewing_high_score = True
            elif rules_button_rect.collidepoint(mouse_x, mouse_y):
                viewing_rules = True
            elif mute_button_rect.collidepoint(mouse_x, mouse_y):
                muted = not muted
                if muted:
                    stop_background_music()
                else:
                    play_background_music()

        elif game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_active = False
            play_background_music()

        elif not game_active and event.type == pygame.KEYDOWN:
            play_background_music()
        elif event.type == pygame.MOUSEBUTTONDOWN and viewing_high_score:
            play_sound(Click,muted)
            mouse_x, mouse_y = event.pos
            if high_score_easy_button_rect.collidepoint(mouse_x, mouse_y):
                high_score_display = 'easy'
            elif high_score_hard_button_rect.collidepoint(mouse_x, mouse_y):
                high_score_display = 'hard'
            elif high_score_impossible_button_rect.collidepoint(mouse_x, mouse_y):
                high_score_display = 'impossible'
            else:
                viewing_high_score = False
        elif event.type == pygame.MOUSEBUTTONDOWN and viewing_rules:
            play_sound(Click,muted)
            viewing_rules = False

        elif event.type == pygame.MOUSEBUTTONDOWN and choosing_mode:
            play_sound(Click,muted)
            mouse_x, mouse_y = event.pos
            if mode1_button_rect.collidepoint(mouse_x, mouse_y):
                play_sound(Click, muted)
                choosing_difficulty = True
                choosing_mode = False

        elif event.type == pygame.MOUSEBUTTONDOWN and choosing_difficulty:
            play_sound(Click,muted)
            mouse_x, mouse_y = event.pos
            if easy_button_rect.collidepoint(mouse_x, mouse_y):
                play_sound(Click, muted)
                selected_difficulty = 'easy'
                background_image = background_images['mode1']
                game_active = True
                choosing_difficulty = False
                start_time = time.time()
                score = 0
                balls = [create_new_ball(RED, character_images, card_image)]
            elif hard_button_rect.collidepoint(mouse_x, mouse_y):
                selected_difficulty = 'hard'
                background_image = background_images['mode1']
                game_active = True
                choosing_difficulty = False
                start_time = time.time()
                score = 0
                balls = [create_new_ball(RED, character_images, card_image)]
            elif impossible_button_rect.collidepoint(mouse_x, mouse_y):
                selected_difficulty = 'impossible'
                background_image = background_images['mode1']
                game_active = True
                choosing_difficulty = False
                start_time = time.time()
                score = 0
                balls = create_parallel_balls(1, RED, character_images, card_image)  # Create one ball initially for impossible mode
                next_ball_time = time.time() + random.uniform(2, 5)  # Random time between 2 to 5 seconds for next ball
            elif tutorial_button_rect.collidepoint(mouse_x, mouse_y):
                webbrowser.open("https://www.youtube.com/watch?v=rEm6cCNRX3Q")
        if game_active:
            display_player_name(player_data['name'])
            stop_background_music()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    game_active = False
                else:
                    if selected_difficulty == 'impossible':
                        ball = balls[0]
                        card_rect = ball.card_image.get_rect(center=(ball.x, ball.y))
                        if card_rect.collidepoint(event.pos):
                            ball.dragging = True
                            offset_x = ball.x - mouse_x
                            offset_y = ball.y - mouse_y
                            dragging_ball = ball  # הגדרת הכדור הנגרר
                    else:
                        for ball in balls:
                            card_rect = ball.card_image.get_rect(center=(ball.x, ball.y))
                            if card_rect.collidepoint(event.pos):
                                ball.dragging = True
                                offset_x = ball.x - mouse_x
                                offset_y = ball.y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                for ball in balls:
                    if ball.dragging:
                        mouse_x, mouse_y = event.pos
                        ball.x = mouse_x + offset_x
                        ball.y = mouse_y + offset_y
                        correct = False
                        for color, points in character_color_map[ball.original_character_name]:
                            if any(corner_name for corner_name, (x1, y1, width, height, c) in corners.items() if
                                   x1 <= ball.x <= x1 + width and y1 <= ball.y <= y1 + height and c == color):
                                score += points
                                points_change = points
                                points_change_time = time.time()
                                play_sound(sounds[color], muted)
                                ball.snap_to_corner()  # Snap the ball to the corner
                                correct = True
                                break
                        if not correct:
                            score -= 50
                            points_change = -50
                            points_change_time = time.time()
                            play_sound(sounds['error'], muted)
                        if not ball.has_fallen_off_screen():
                            balls.remove(ball)
                            balls.append(create_new_ball(random.choice([RED, BLUE, YELLOW, GREEN]), character_images, card_image))
                    ball.dragging = False
                    dragging_ball = None  # אפס את הכדור הנגרר
            elif event.type == pygame.MOUSEMOTION:
                for ball in balls:
                    if ball.dragging:
                        mouse_x, mouse_y = event.pos
                        ball.x = mouse_x + offset_x
                        ball.y = mouse_y + offset_y
            else:
                play_background_music()
        if entering_name:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        player_data['name'] = input_text
                        save_player_data(player_data)
                        entering_name = False
                        input_text = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                play_sound(Click, muted)  # Play click sound
                mouse_x, mouse_y = event.pos
                if save_button_rect.collidepoint(mouse_x, mouse_y) and not saved:
                    if input_text.strip():
                        # Simulate ENTER key press
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
                elif continue_button_rect.collidepoint(mouse_x, mouse_y):
                    entering_name = False
                    input_text = ""  # אפס את input_text ללא שמירה
                    saved = False  # אפס את המשתנה לשמירה שלא בוצעה
                else:
                    key = virtual_keyboard.get_key_at_pos(event.pos)
                    if key:
                        if key == 'BACKSPACE':
                            input_text = input_text[1:]  # הסר את התו הראשון עבור עברית
                        elif key == 'SPACE':
                            input_text = ' ' + input_text  # הוסף רווח בתחילת המחרוזת עבור עברית
                        else:
                            input_text = key + input_text
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                play_sound(Click, muted)  # Play click sound
                if save_button_rect.collidepoint(mouse_x, mouse_y):
                    if input_text.strip():
                        # Simulate ENTER key press
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
                        saved = True  # עדכון המשתנה לשמירה שבוצעה
                elif continue_button_rect.collidepoint(mouse_x, mouse_y):
                    entering_name = False
                    input_text = ""  # אפס את input_text ללא שמירה
                    saved = False  # אפס את המשתנה לשמירה שלא בוצעה
                else:
                    key = virtual_keyboard.get_key_at_pos(event.pos)
                    if key:
                        play_sound(Click, muted)  # Play click sound
                        if key == 'BACKSPACE':
                            input_text = input_text[1:]  # הסר את התו הראשון עבור עברית
                        elif key == 'SPACE':
                            input_text = ' ' + input_text  # הוסף רווח בתחילת המחרוזת עבור עברית
                        else:
                            input_text = key + input_text  # הוסף את התו בתחילת המחרוזת עבור עברית

    if game_active:
        elapsed_time = time.time() - start_time
        remaining_time = game_duration - elapsed_time
        if remaining_time <= 0:
            game_active = False
            entering_name = player_data['name'] == ''  # Activate name inpu# t screen only if name is not set

            if not entering_name:  # אם השם כבר מוגדר, פשוט עדכן את הציון הגבוה
                new_score_entry = {'name': player_data['name'], 'score': score}
                if selected_difficulty == 'easy':
                    high_scores_easy = update_high_score(high_scores_easy, new_score_entry)
                    save_high_scores()
                    update_player_high_score(score)  # Update the player's high score
                elif selected_difficulty == 'hard':
                    high_scores_hard = update_high_score(high_scores_hard, new_score_entry)
                    save_high_scores()
                    update_player_high_score(score)  # Update the player's high score
                elif selected_difficulty == 'impossible':
                    high_scores_impossible = update_high_score(high_scores_impossible, new_score_entry)
                    save_high_scores()
                    update_player_high_score(score)  # Update the player's high score
        else:
            play_background_music()
        screen.blit(background_image, (0, 0))  # Draw background
        for ball in balls:
            ball.move()
            ball.draw(screen)
            if ball.dragging:
                draw_corners(ball)

        # Check if it's time to add another ball in impossible mode
        if selected_difficulty == 'impossible' and len(balls) < MAX_BALLS and time.time() > next_ball_time:
            balls.append(create_new_ball(random.choice([RED, BLUE, YELLOW, GREEN]), character_images, card_image))
            next_ball_time = time.time() + random.uniform(2, 5)  # Random time between 2 to 5 seconds for next ball

        # Check if ball has fallen off screen
        for ball in balls:
            if ball.has_fallen_off_screen():
                score -= 50
                points_change = -50
                points_change_time = time.time()
                play_sound(sounds['error'], muted)
                balls.remove(ball)
                balls.append(create_new_ball(random.choice([RED, BLUE, YELLOW, GREEN]), character_images, card_image))

        # Display score and timer
        small_font = pygame.font.Font('OzradCLM.otf', 40)
        score_text = small_font.render(f"  : {score}", True, WHITE)
        timer_text = small_font.render(f"    : {int(remaining_time)}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(score_text, score_rect)
        screen.blit(timer_text, timer_rect)

        # Display points change
        if time.time() - points_change_time < 1:  # Display points change for 1 second
            points_change_text = points_font.render(f"{points_change}", True, WHITE)
            points_change_rect = points_change_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(points_change_text, points_change_rect)

        # Display back button
        screen.blit(back_button_text, back_button_rect)

        draw_corners(ball)  # Draw the corner images only during game and when ball is dragging

        if input_active:
            input_rect = pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50), (400, 100))
            pygame.draw.rect(screen, WHITE, input_rect, 2)
            input_text_surface = input_font.render(input_text, True, WHITE)
            screen.blit(input_text_surface, (input_rect.x + 10, input_rect.y + 10))

    elif entering_name:
        screen.blit(name_input_background, (0, 0))  # Draw name input background

        # Display the input_text directly
        input_text_surface = input_font.render(input_text, True, WHITE)
        input_text_rect = input_text_surface.get_rect(center=input_rect.center)
        screen.blit(input_text_surface, input_text_rect)

        # Render the button text and center it within the button rectangles
        save_button_text = button_font.render("        ", True, BLACK)
        save_button_text_rect = save_button_text.get_rect(center=save_button_rect.center)
        screen.blit(save_button_text, save_button_text_rect)

        continue_button_text = button_font.render("                 ", True, BLACK)
        continue_button_text_rect = continue_button_text.get_rect(center=continue_button_rect.center)
        screen.blit(continue_button_text, continue_button_text_rect)
    elif viewing_high_score:
        screen.blit(high_score_background, (0, 0))  # Draw high score background
        screen.blit(high_scores_easy_text, high_score_easy_button_rect)
        screen.blit(high_scores_hard_text, high_score_hard_button_rect)
        screen.blit(high_scores_impossible_text, high_score_impossible_button_rect)
        if high_score_display == 'easy':
            scores_to_display = high_scores_easy
            display_high_score_rank(high_scores_easy, player_data['high_score'])
        elif high_score_display == 'hard':
            scores_to_display = high_scores_hard
            display_high_score_rank(high_scores_hard, player_data['high_score'])
        else:
            scores_to_display = high_scores_impossible
            display_high_score_rank(high_scores_impossible, player_data['high_score'])


        high_score_text = large_font.render(f" ({high_score_display.capitalize()})", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 50))
        y_offset = 140

        top_scores = scores_to_display[:5]

        for index, entry in enumerate(top_scores):
            text_color = BLACK if index in [3, 4] else WHITE
            name_text = large_font.render(entry['name'], True, text_color)
            score_text = large_font.render(f"{entry['score']}", True, text_color)
            score_x = SCREEN_WIDTH // 2 - 370  # Fixed position for scores
            name_x = SCREEN_WIDTH - name_text.get_width() - 250  # Fixed position for names aligned to the right
            screen.blit(name_text, (name_x, y_offset))
            screen.blit(score_text, (score_x, y_offset))
            y_offset += 120

        continue_text = large_font.render("Press any key to continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(continue_text, continue_rect)

    elif choosing_mode:
        screen.blit(mode_selection_background, (0, 0))  # Draw mode selection background
        screen.blit(mode1_image, mode1_button_rect)
        screen.blit(mode2_image, mode2_button_rect)

    elif choosing_difficulty:
        screen.blit(difficulty_selection_background, (0, 0))  # Draw difficulty selection background
        screen.blit(tutorial_button_image, tutorial_button_rect)

        easy_text = button_font.render("Easy", True, BLACK)
        hard_text = button_font.render("Hard", True, BLACK)
        impossible_text = button_font.render("Impossible", True, BLACK)

    elif viewing_rules:
        screen.blit(rules_image, (0, 0))
        continue_text = button_font.render("            ", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(continue_text, continue_rect)

    else:
        screen.blit(home_background, (0, 0))  # Draw home background
        screen.blit(start_button_text, start_button_rect)
        screen.blit(high_score_button_text, high_score_button_rect)
        screen.blit(rules_button_text, rules_button_rect)
        screen.blit(unmute_image if not muted else mute_image, mute_button_rect)
    display_fps()
    display_highscore(player_data['high_score'])
    display_player_name(player_data['name'])# Display the FPS counter
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
