import hashlib
import webbrowser
from io import BytesIO

import requests
from PIL import Image


def get_image_from_hash(target_md5, target_sha256):
    # Сначала найдем исходную строку (предположительно название цвета)
    original_string = find_original_string(target_md5, target_sha256)

    if original_string:
        print(f"\nНайдена строка: '{original_string}'")
        print("Ищем изображение в интернете...")

        # Ищем изображение машины этого цвета
        search_and_display_image(original_string)
        return original_string
    else:
        print("Не удалось найти исходную строку по заданным хешам")
        return None


def find_original_string(target_md5, target_sha256):
    # Популярные названия цветов для автомобилей
    car_colors = [
        "red", "blue", "green", "black", "white", "yellow", "orange",
        "purple", "pink", "brown", "gray", "silver", "gold", "cyan",
        "magenta", "maroon", "navy", "teal", "olive", "lime", "aqua",
        "crimson", "coral", "indigo", "violet", "beige", "ivory"
    ]

    # Проверяем популярные цвета
    for color in car_colors:
        if (hashlib.md5(color.encode()).hexdigest() == target_md5 and
                hashlib.sha256(color.encode()).hexdigest() == target_sha256):
            return color

    # Если не нашли в популярных, пробуем варианты с заглавными буквами
    for color in car_colors:
        color_capitalized = color.capitalize()
        if (hashlib.md5(color_capitalized.encode()).hexdigest() == target_md5 and
                hashlib.sha256(color_capitalized.encode()).hexdigest() == target_sha256):
            return color_capitalized

    # Если все еще не нашли, пробуем перебор коротких строк
    import string
    alphabet = string.ascii_lowercase
    max_length = 6

    for length in range(1, max_length + 1):
        for candidate in generate_combinations(alphabet, length):
            candidate_str = ''.join(candidate)
            if (hashlib.md5(candidate_str.encode()).hexdigest() == target_md5 and
                    hashlib.sha256(candidate_str.encode()).hexdigest() == target_sha256):
                return candidate_str

    return None


def generate_combinations(alphabet, length):
    """Генератор комбинаций для перебора"""
    if length == 0:
        yield []
    else:
        for char in alphabet:
            for combo in generate_combinations(alphabet, length - 1):
                yield [char] + combo


def search_and_display_image(color_name):
    print(f"Цвет машины: {color_name}")

    # Формируем запрос для поиска
    query = f"{color_name} car vehicle automobile"

    try:
        # Пытаемся найти через Google Images (через прямой URL)
        google_url = f"https://www.google.com/search?tbm=isch&q={query}"
        webbrowser.open(google_url)
        print(f"Открыт поиск Google Images для: '{query}'")

        # Также попробуем найти через Unsplash (если есть API ключ)
        try_unsplash_search(color_name)

    except Exception as e:
        print(f"Ошибка при поиске изображения: {e}")


def try_unsplash_search(color_name):
    try:
        # Замените 'YOUR_ACCESS_KEY' на ваш настоящий Unsplash Access Key
        access_key = "YOUR_UNSPLASH_ACCESS_KEY"

        if access_key != "YOUR_UNSPLASH_ACCESS_KEY":
            url = f"https://api.unsplash.com/search/photos?query={color_name}+car&client_id={access_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    # Берем первое найденное изображение
                    image_url = data['results'][0]['urls']['regular']

                    # Скачиваем и показываем изображение
                    img_response = requests.get(image_url)
                    img = Image.open(BytesIO(img_response.content))
                    img.show()
                    print(f"Загружено и показано изображение с Unsplash")
                    return

        print("Unsplash API не настроен, используйте Google Images для просмотра")


    except Exception as e:
        print(f"Не удалось получить изображение через Unsplash: {e}")


if __name__ == "__main__":
    target_md5 = "743f0ed26d2bff34fb9a335588238ceb"
    target_sha256 = "ef581243eb6f7fa74ce03466b9051464275c6b34017a6f031f2548a6d5d0b711"

    print("Поиск изображения по хешам:")
    print(f"MD5: {target_md5}")
    print(f"SHA-256: {target_sha256}")
    print("=" * 60)

    result = get_image_from_hash(target_md5, target_sha256)

    if result:
        print("\n" + "=" * 60)
        print(f"УСПЕХ: Найден цвет '{result}' и выполнён поиск изображения")
        print("Изображение должно открыться в вашем браузере (Google Images)")
    else:
        print("\n" + "=" * 60)
        print("Не удалось найти соответствие для заданных хешей")
