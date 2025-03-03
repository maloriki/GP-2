import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

driver = webdriver.Chrome()
chrome_options = Options()
books = []

with open('genres', 'r', encoding='UTF-8') as f:
    genres = f.read().split(';')
print(genres)
for i in genres:
    time.sleep(2)
    print(f'Сейчас на жанре {i} уже спарсино {len(books)}')
    url = f"https://www.livelib.ru/genre/{i}/top/"
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    book_items = soup.find_all("li", class_="book-item__item")


    for book in book_items:
        try:
            
            title_tag = book.find("a", class_="book-item__title")
            title = title_tag.text.strip() if title_tag else "Не найдено"

            
            author_tag = book.find("a", class_="book-item__author")
            author = author_tag.text.strip() if author_tag else "Не найдено"

            
            rating_tag = book.find("div", class_="book-item__rating")
            rating = rating_tag.text.strip() if rating_tag else "Не найдено"

           
            isbn_tag = book.find("td", class_="book-item-edition__col1", text="ISBN:")
            isbn = isbn_tag.find_next_sibling("td").text.strip() if isbn_tag else "Не найдено"

     
            year_tag = book.find("td", class_="book-item-edition__col1", text="Год издания:")
            year = year_tag.find_next_sibling("td").text.strip() if year_tag else "Не найдено"

      
            publisher_tag = book.find("td", class_="book-item-edition__col1", text="Издательство:")
            publisher = publisher_tag.find_next_sibling("td").text.strip() if publisher_tag else "Не найдено"

         
            readers_tag = book.find("a", class_="icon-added-grey")
            readers = readers_tag.text.strip() if readers_tag else "Не найдено"

   
            reviews_tag = book.find("a", class_="icon-review-grey")
            reviews = reviews_tag.text.strip() if reviews_tag else "Не найдено"


            description_tag = book.find("div", class_="book-item__text")
            description = description_tag.text.strip() if description_tag else "Не найдено"


            books.append({
                "Название": title,
                "Автор": author,
                "Рейтинг": rating,
                "ISBN": isbn,
                "Год издания": year,
                "Издательство": publisher,
                "Прочитали": readers,
                "Рецензии": reviews,
                "Описание": description
            })
        except Exception as e:
            print(f"Ошибка при обработке книги на жанре {i}: {e}")
    print(f"Спарсили {len(book_items)} книг с жанра {i}")



df = pd.DataFrame(books)
df.to_csv('books.csv')
