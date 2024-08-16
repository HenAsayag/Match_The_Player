import os
import requests
from bs4 import BeautifulSoup
import re

TEAM_COLORS = {
    "מכבי חיפה": "GREEN",
    'בית"ר ירושלים': "YELLOW",
    "מכבי תל אביב": 'BLUE',
    "הפועל תל אביב": "RED"
}

def extract_years_and_club(rows):
    career_info = []
    years_pattern = re.compile(r'(\d{4})\s?[-–]?\s?(\d{4})?')

    for row in rows:
        td_elements = row.find_all('td')
        if len(td_elements) >= 2:
            years_text = td_elements[0].get_text(separator=' ').strip()
            clubs_html = td_elements[1].find_all('a')
            years = re.split(r'\s+', years_text)
            clubs = [club.get_text(separator=' ').strip() for club in clubs_html]

            for i, year_range in enumerate(years):
                match = years_pattern.match(year_range)
                if match:
                    start_year = int(match.group(1))
                    end_year = int(match.group(2)) if match.group(2) else start_year
                    if i < len(clubs):
                        club = clubs[i]
                        career_info.append((club, start_year, end_year))

    return career_info

def calculate_points(career_info):
    club_years = {}
    for club, start, end in career_info:
        if club in TEAM_COLORS:
            years = end - start + 1 if start != end else 1
            if club in club_years:
                club_years[club] += years
            else:
                club_years[club] = years

    if not club_years:
        return []

    max_years = max(club_years.values())
    points_info = [(TEAM_COLORS[club], int((years / max_years) * 100)) for club, years in club_years.items()]
    points_info.sort(key=lambda x: x[1], reverse=True)
    return points_info

def format_output(player_name, points_info):
    formatted_points = [(color, points) for color, points in points_info]
    points_str = ", ".join([f"({color}, {points})" for color, points in formatted_points])
    return f'"{player_name}": [{points_str}],'

def search_player_years(player_name):
    search_url = f"https://he.wikipedia.org/wiki/{player_name.replace(' ', '_')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"לא ניתן למצוא דף ויקיפדיה עבור {player_name}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all('table')
    for table in tables:
        header_found = False
        rows_to_process = []

        rows = table.find_all('tr')
        for row in rows:
            th_elements = row.find_all('th')
            if any("מועדונים מקצועיים כשחקן" in th.get_text() for th in th_elements):
                header_found = True
                continue
            if header_found:
                rows_to_process.append(row)

        if rows_to_process:
            career_info = extract_years_and_club(rows_to_process)
            points_info = calculate_points(career_info)

            if points_info:
                output = format_output(player_name, points_info)
                print(output)
                return

    print(f"לא נמצא מידע על השנים והקבוצות עבור {player_name}")

def main():
    folder_path = 'C:/Users/Hen Asayag/pythonProject1/HAPOEL1'
    if not os.path.exists(folder_path):
        print(f"תיקיית {folder_path} לא קיימת.")
        return

    files = os.listdir(folder_path)
    if not files:
        print(f"אין קבצים בתיקיית {folder_path}.")
        return

    for file in files:
        if file.endswith('.png'):
            player_name = os.path.splitext(file)[0]
            search_player_years(player_name)

if __name__ == "__main__":
    main()
