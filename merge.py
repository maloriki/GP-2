import pandas as pd
import logging
import colouredlogs

logger = logging.getLogger(__name__)

colouredlogs.install(
    level='INFO',
    logger=logger,
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def load_and_merge_files(file1, file2, file3, merge_on=None):
    try:
        df1 = pd.read_csv(file1)
        logger.info(f"Файл {file1} успешно загружен.")
        df2 = pd.read_csv(file2)
        logger.info(f"Файл {file2} успешно загружен.")
        df3 = pd.read_csv(file3)
        logger.info(f"Файл {file3} успешно загружен.")
    except Exception as e:
        logger.error(f"Ошибка при загрузке файлов: {e}")
        exit()

    try:
        if merge_on:
            merged_df = df1.merge(df2, on=merge_on, how='outer').merge(df3, on=merge_on, how='outer')
            logger.info(f"Файлы объединены по столбцу '{merge_on}'.")
        else:
            merged_df = pd.concat([df1, df2, df3], ignore_index=True)
            logger.info("Файлы объединены по строкам.")
    except Exception as e:
        logger.error(f"Ошибка при объединении файлов: {e}")
        exit()

    return merged_df


file1 = 'books.csv'
file2 = 'google_books_api_dataset.csv'
file3 = 'eksmo.csv'

merged_df = load_and_merge_files(file1, file2, file3, merge_on='ISBN')

try:
    merged_df.to_csv('merged_books.csv', index=False)
    logger.info("Объединенный файл успешно сохранен как 'merged_books.csv'.")
except Exception as e:
    logger.error(f"Ошибка при сохранении объединенного файла: {e}")
