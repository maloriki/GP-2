import time
import requests
import pandas as pd
import progressbar
import logging
import colouredlogs
import yaml

progressbar.streams.wrap_stderr()

logger = logging.getLogger(__name__)

colouredlogs.install(
    level='INFO',
    logger=logger,
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def load_api_key(file_path='api_key.yaml'):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            return config.get('key')
    except Exception as e:
        logger.error(f"Ошибка при загрузке API-ключа из файла {file_path}: {e}")
        exit()

API_KEY = load_api_key()

BASE_URL = 'https://www.googleapis.com/books/v1/volumes'

def fetch_books_by_isbn(isbn_list):
    books_data = []
    counter = 0
    for isbn in progressbar.progressbar(isbn_list):
        params = {
            'q': f'isbn:{isbn}',
            'key': API_KEY,
            'maxResults': 1
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                book = data['items'][0]
                volume_info = book.get('volumeInfo', {})
                books_data.append({
                    'title': volume_info.get('title', 'Нет названия'),
                    'authors': ', '.join(volume_info.get('authors', ['Автор неизвестен'])),
                    'publisher': volume_info.get('publisher', 'Нет издателя'),
                    'publishedDate': volume_info.get('publishedDate', 'Нет даты'),
                    'description': volume_info.get('description', 'Нет описания'),
                    'ISBN_10': volume_info.get('industryIdentifiers', [{}])[0].get('identifier', 'Нет ISBN'),
                    'pageCount': volume_info.get('pageCount', 'Нет данных'),
                    'categories': ', '.join(volume_info.get('categories', ['Нет категорий'])),
                    'language': volume_info.get('language', 'Нет данных')
                })
                logger.info(f"Успешно обработан ISBN: {isbn}")
            else:
                logger.warning(f"Книга с ISBN {isbn} не найдена.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе для ISBN {isbn}: {e}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка для ISBN {isbn}: {e}")

        counter += 1
        if counter % 100 == 0:
            logger.info(f"Обработано {counter} книг. Ожидание 2 секунды...")
            time.sleep(2)

    return books_data

try:
    df = pd.read_csv('books.csv')
    logger.info("Файл books.csv успешно загружен.")
except Exception as e:
    logger.error(f"Ошибка при загрузке файла books.csv: {e}")
    exit()

isbn_list = df['ISBN'].tolist()
logger.info(f"Извлечено {len(isbn_list)} ISBN для обработки.")

books_data = fetch_books_by_isbn(isbn_list)

df_books = pd.DataFrame(books_data)

try:
    df_books.to_csv('google_books_api_dataset.csv', index=False)
    logger.info("Информация о книгах успешно сохранена в файл 'google_books_api_dataset.csv'.")
except Exception as e:
    logger.error(f"Ошибка при сохранении файла google_books_api_dataset.csv: {e}")