import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
import threading
from datetime import datetime

# Загрузка .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Инициализация Supabase
supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)


def move_books(book_id, from_branch_id, to_branch_id, quantity):
    try:
        print(f"[{datetime.now()}] Попытка перемещения {quantity} книг из {from_branch_id} в {to_branch_id}")

        # Вызываем хранимую процедуру
        result = supabase.rpc('move_books_safe', {
            'p_book_id': book_id,
            'p_from_branch_id': from_branch_id,
            'p_to_branch_id': to_branch_id,
            'p_quantity': quantity
        }).execute()

        if 'error' in result.data:
            print(f"[{datetime.now()}] Ошибка: {result.data['error']}")
        else:
            print(f"[{datetime.now()}] Успешно перемещено {quantity} книг")

    except Exception as e:
        print(f"[{datetime.now()}] Исключение: {str(e)}")


def simulate_lost_update():
    print("\nМоделирование 'потерянного обновления'")

    try:
        # 1. Сначала добавляем книгу
        book = supabase.table('books').insert({'name': 'Война и мир'}).execute()
        book_id = book.data[0]['id']
        print(f"Добавлена книга с ID: {book_id}")

        # 2. Добавляем филиалы
        branches = supabase.table('branches').insert([
            {'name': 'Центральный'},
            {'name': 'Северный'},
            {'name': 'Южный'}
        ]).execute()
        branch_ids = [b['id'] for b in branches.data]
        print(f"Добавлены филиалы с ID: {branch_ids}")

        # 3. Добавляем начальные запасы (только после создания книги и филиалов)
        supabase.table('stock').insert({
            'book_id': book_id,
            'branch_id': branch_ids[0],  # Центральный филиал
            'quantity': 10
        }).execute()
        print("Добавлены начальные запасы")

        # 4. Создаем потоки для перемещения
        thread1 = threading.Thread(
            target=move_books,
            args=(book_id, branch_ids[0], branch_ids[1], 5)  # В северный филиал
        )

        thread2 = threading.Thread(
            target=move_books,
            args=(book_id, branch_ids[0], branch_ids[2], 5)  # В южный филиал
        )

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # 5. Вывод результатов
        print("\nСостояние запасов:")
        stocks = supabase.table('stock').select('*').execute()
        for stock in stocks.data:
            print(f"Книга {stock['book_id']} в филиале {stock['branch_id']}: {stock['quantity']} экз.")

        print("\nИстория перемещений:")
        moves = supabase.table('movements').select('*').execute()
        for move in moves.data:
            print(f"Из {move['from_branch_id']} в {move['to_branch_id']}: {move['quantity']} экз.")

    except Exception as e:
        print(f"Ошибка при инициализации данных: {str(e)}")


if __name__ == "__main__":
    # Очистка таблиц
    supabase.table('movements').delete().neq('id', 0).execute()
    supabase.table('stock').delete().neq('book_id', 0).execute()
    supabase.table('branches').delete().neq('id', 0).execute()
    supabase.table('books').delete().neq('id', 0).execute()

    simulate_lost_update()