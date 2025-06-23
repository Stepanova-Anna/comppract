import redis

# Имя ключа, с которым мы будем работать в Redis
MY_KEY = "my_secret_code"


def run_redis_operations():
    print("Подключаемся к локальному серверу Redis...")
    try:
        # Подключаемся к Redis.
        # Для простоты сразу будем получать строки, а не байты.
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

        # Проверим соединение
        r.ping()
        print("Успешное подключение к Redis!")
        print("------------------------------------")

    except redis.exceptions.ConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")
        print("Убедитесь, что ваш сервер Redis запущен (команда 'redis-server').")
        return

    # 1. Создание ключа и установка первоначального значения
    initial_value = "ПарольРыбаМеч"
    # ВАШ КОД ЗДЕСЬ (1):
    # Используйте команду r.set() для установки значения `initial_value` для ключа `MY_KEY`.
    r.set(MY_KEY, initial_value)
    print(f"1. Установлено значение '{initial_value}' для ключа '{MY_KEY}'.")

    # 2. Чтение значения ключа
    # ВАШ КОД ЗДЕСЬ (2):
    # Используйте команду r.get() для получения значения ключа `MY_KEY`.
    # Сохраните результат в переменную `retrieved_value_1`.
    retrieved_value_1 = r.get(MY_KEY)
    print(f"2. Прочитанное значение: {retrieved_value_1}")
    print("------------------------------------")

    # 3. Изменение значения ключа
    new_value = "СекретБелкиВКолесе"
    # ВАШ КОД ЗДЕСЬ (3):
    # Снова используйте команду r.set() для установки нового значения `new_value` для того же ключа `MY_KEY`.
    r.set(MY_KEY, new_value)
    print(f"3. Изменено значение для ключа '{MY_KEY}' на '{new_value}'.")

    # 4. Чтение измененного значения
    # ВАШ КОД ЗДЕСЬ (4):
    # Используйте команду r.get() еще раз для получения нового значения ключа `MY_KEY`.
    # Сохраните результат в переменную `retrieved_value_2`.
    retrieved_value_2 = r.get(MY_KEY)
    print(f"4. Прочитанное новое значение: {retrieved_value_2}")
    print("------------------------------------")

    # (Необязательно, но хорошая практика для чистоты) Удаление ключа после тестов
    r.delete(MY_KEY)
    print(f"Ключ '{MY_KEY}' удален для чистоты.")


if __name__ == "__main__":
    # Инициализация переменных
    retrieved_value_1 = None
    retrieved_value_2 = None
    run_redis_operations()