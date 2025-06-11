import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

# Настройки Yandex Cloud S3
ENDPOINT_URL = "https://storage.yandexcloud.net"
BUCKET_NAME = "lr9-bucket" # Ваше название бакета
TEST_FILE = "test.txt"

# Инициализация клиента (ключи берутся автоматически из ~/.aws/credentials)
s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL
)


def create_test_file():
    """Создает тестовый файл, если он не существует"""
    if not os.path.exists(TEST_FILE):
        with open(TEST_FILE, 'w') as f:
            f.write("Тестовое содержимое файла")
        print(f"Создан тестовый файл {TEST_FILE}")


def list_files():
    """Получение списка файлов в бакете"""
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if "Contents" in response:
            print("\nСодержимое бакета:")
            for obj in response["Contents"]:
                print(f"- {obj['Key']} (размер: {obj['Size']} байт)")
        else:
            print("\nБакет пуст.")
    except NoCredentialsError:
        print("Ошибка аутентификации. Проверьте ключи.")
    except ClientError as e:
        print(f"Ошибка при доступе к бакету: {e}")


def upload_file(file_path, object_name):
    """Загрузка файла в бакет"""
    try:
        if not os.path.exists(file_path):
            print(f"Ошибка: файл {file_path} не найден")
            return False

        s3.upload_file(
            file_path,
            BUCKET_NAME,
            object_name,
            ExtraArgs={"StorageClass": "STANDARD"},
        )
        print(f"\nФайл {object_name} успешно загружен.")
        return True
    except NoCredentialsError:
        print("Ошибка аутентификации.")
        return False
    except ClientError as e:
        print(f"Ошибка загрузки: {e}")
        return False


def download_file(object_name, output_path):
    """Скачивание файла"""
    try:
        s3.download_file(BUCKET_NAME, object_name, output_path)
        print(f"\nФайл {object_name} скачан в {output_path}.")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"\nФайл {object_name} не найден в бакете")
        else:
            print(f"\nОшибка скачивания: {e}")
        return False


def delete_file(object_name):
    """Удаление файла"""
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=object_name)
        print(f"\nФайл {object_name} удалён.")
        return True
    except ClientError as e:
        print(f"\nОшибка удаления: {e}")
        return False


if __name__ == "__main__":
    # 1. Создаем тестовый файл
    create_test_file()

    # 2. Показываем начальное состояние бакета
    print("Начальное состояние бакета:")
    list_files()

    # 3. Загружаем файл
    object_name = "test-file.txt"
    if upload_file(TEST_FILE, object_name):
        # 4. Показываем содержимое после загрузки
        print("\nПосле загрузки:")
        list_files()

        # 5. Скачиваем файл
        downloaded_file = "downloaded.txt"
        if download_file(object_name, downloaded_file):
            print(f"Файл успешно сохранен локально как {downloaded_file}")

            # 6. Удаляем файл из бакета
            if delete_file(object_name):
                # 7. Показываем финальное состояние
                print("\nФинальное состояние бакета:")
                list_files()
