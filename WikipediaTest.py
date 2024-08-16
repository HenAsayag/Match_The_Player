import requests
from bs4 import BeautifulSoup
from rembg import remove
from PIL import Image
from io import BytesIO
import os
import time
import cv2
import numpy as np

CX = '127f0e4a5e31c4614'
API_KEYS = ['AIzaSyAKeZ6sytMyf9fTFFUVULkg-KFyafguCtY', 'AIzaSyD4aHA27MrO-L6ep_i5Rzpxh6WRenx2TUU', 'AIzaSyBwyEJyHO3OyCL2ovcFvmnvRqansr8CEBA']  # רשימת המפתחות שלך
current_key_index = 0

def get_api_key():
    global current_key_index
    key = API_KEYS[current_key_index]
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    return key

def search_image_on_google(player_name):
    search_query = f"{player_name} national team"
    search_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&cx={CX}&key={get_api_key()}&searchType=image"


def is_clear_image(image_url):
    try:
        headers = {'User-Agent': USER_AGENT}
        img_response = requests.get(image_url, headers=headers, timeout=10)
        img_response.raise_for_status()
        img = Image.open(BytesIO(img_response.content))
        width, height = img.size
        return width > 100 and height > 100  # Example threshold for image clarity
    except Exception as e:
        print(f"Error checking image clarity: {e}")
        return False


def detect_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces) > 0


# עדכון הזמן המתנה
def search_image_on_google(player_name):
    search_query = f"{player_name} national team"
    search_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&cx={CX}&key={get_api_key()}&searchType=image"
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        search_results = response.json()
        if 'items' in search_results:
            for item in search_results['items']:
                image_url = item['link']
                if is_clear_image(image_url):
                    img_response = requests.get(image_url, headers={'User-Agent': USER_AGENT}, timeout=10)
                    img_response.raise_for_status()
                    img_array = np.array(Image.open(BytesIO(img_response.content)))
                    if detect_face(img_array):
                        return image_url
    except requests.exceptions.RequestException as e:
        print(f"Error searching image on Google: {e}")
    return None

def remove_background(image_url):
    try:
        headers = {'User-Agent': USER_AGENT}
        img_response = requests.get(image_url, headers=headers, timeout=10)
        img_response.raise_for_status()
        img = Image.open(BytesIO(img_response.content))
        output = remove(img)
        return output
    except Exception as e:
        print(f"Error removing background: {e}")
        return None


# רשימת שחקנים לפי קבוצות
categories = {
    "Manchester City": [
        "Kevin_De_Bruyne",
        "Erling Haaland",
        "Ederson",
        "Bernardo Silva",
        "Rodri",
        "Ruben Dias",
        "John Stones",
        "Kyle Walker",
        "Kalvin Phillips",
        "Jack Grealish",
        "Phil Foden",
        "Manuel Akanji",
        "Mateo Kovacic",
        "Julian Alvarez"
    ],
    "Liverpool": [
        "Mohamed Salah",
        "Virgil van Dijk",
        "Alisson",
        "Thiago",
        "Luis Díaz",
        "Darwin Núñez",
        "Cody Gakpo",
        "Andrew Robertson",
        "Trent Alexander-Arnold",
        "Ibrahima Konaté"
    ],
    "Manchester United": [
        "Bruno Fernandes",
        "Marcus Rashford",
        "Raphael Varane",
        "Casemiro",
        "Mason Mount",
        "Harry Maguire",
        "Luke Shaw",
        "Lisandro Martínez",
        "Antony",
        "Christian Eriksen",
        "Jadon Sancho"
    ],
    "Chelsea": [
        "Christopher Nkunku",
        "Reece James",
        "Raheem Sterling",
        "Enzo Fernández",
        "Mykhailo Mudryk",
        "Benoît Badiashile",
        "Noni Madueke",
        "Ben Chilwell",
        "Thiago Silva",
        "Malo Gusto"
    ]
}

# יצירת תיקיית פלט
output_dir = "PREMIERLEAGUEPLAYERS"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# עיבוד כל קבוצה
for team, players in categories.items():
    team_dir = os.path.join(output_dir, team.replace(" ", "_"))
    if not os.path.exists(team_dir):
        os.makedirs(team_dir)

    players_and_images = []

    # עיבוד כל שחקן בקבוצה
    for player_name in players:
        image_url = search_image_on_google(player_name)
        if image_url:
            print(f"Found image for {player_name} (Team: {team}): {image_url}")
            output_image = remove_background(image_url)
            if output_image:
                output_path = os.path.join(team_dir, f"{player_name.replace(' ', '_')}.png")
                output_image.save(output_path)
                print(f"Saved image: {output_path}")
                players_and_images.append((player_name, output_path))
            time.sleep(5)  # Respectful delay between requests

    # Display the results
    for name, image_path in players_and_images:
        print(f"Team: {team}, Player: {name}, Image Path: {image_path}")
