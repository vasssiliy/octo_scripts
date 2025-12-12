import requests
import pandas as pd
import time

API_TOKEN = ""
OUTPUT_FILE = "octobrowser_profiles_full.xlsx"

BASE_URL = "https://app.octobrowser.net/api/v2/automation/profiles"

def fetch_all_profiles():
    headers = {
        "X-Octo-Api-Token": API_TOKEN,
        "Accept": "application/json"
    }

    all_profiles = []
    page = 0
    page_len = 100  # максимум разрешенный API

    while True:
        params = {
            "page": page,
            "page_len": page_len,
            "fields": "title,description,proxy,start_pages,tags,status,last_active,version,storage_options,created_at,updated_at,has_user_password,pinned_tag,launch_args,images_load_limit,local_cache" 
        }

        print(f"Загружаю страницу {page}...")
        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code == 401:
            print("Ошибка: Unauthorized — проверь токен.")
            break

        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code, response.text)
            break

        data = response.json()

        profiles = data.get("data") or data.get("items") or []

        if not profiles:
            print("Профили закончились.")
            break

        all_profiles.extend(profiles)

        if len(profiles) < page_len:
            break

        page += 1
        time.sleep(0.2)

    return all_profiles


def save_to_excel(profiles):
    if not profiles:
        print("Нет данных для сохранения.")
        return

    df = pd.DataFrame(profiles)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Файл сохранён: {OUTPUT_FILE}")
    print(f"Всего выгружено профилей: {len(profiles)}")


if __name__ == "__main__":
    print("Старт выгрузки всех данных профилей из OctoBrowser API v2...")
    profiles = fetch_all_profiles()
    save_to_excel(profiles)