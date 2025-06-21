# Лабораторная работа №5

## Задание

Задание - доделать проект по WebAssembly - budget_planner_project.zip

1. Изучить файл README.md внутри проекта и сделать первичное изучение кода самого проекта, понять общих принцип работы кода.
2. Скачать и установить компилятор для WebAssembly с сайта https://emscripten.org (см. README.md).
3. Добиться компиляции и работы самого приложения.
4. Самостоятельно придумать какое-либо улучшение (improvment) для проекта, основываясь на исходных примерах кода в проекте.
5. Сделать отчёт о проделано работе в формате Markdown.
6. Закомитить всё в один репозиторий на GitHub и прислать ответ в виде ссылке на него.

## Решение 

Выполнить через https://emscripten.org не удалось из-за ошибки с SSL-сертификатами

![image](https://github.com/user-attachments/assets/d5f9a898-8f00-4711-8649-d103dab77f63)

Вариантом решения стал Docker-образ:

* Запуск контейнера с Emscripten

```
docker pull emscripten/emsdk
```

```
docker run -it --rm -v ${PWD}:/src emscripten/emsdk bash
```

![image](https://github.com/user-attachments/assets/ca857c29-2fba-4166-b41c-8dc220646241)


* Работа внутри контейнера

Переходим в директорию с проектом

```
cd /src
```

Проверяем файлы

```
ls -la
```

* Компиляция проекта

Выполняем команду из README.md, адаптированную для Docker

```
emcc main.c -o index.js -s WASM=1 -O2 \
-s EXPORTED_RUNTIME_METHODS='["stringToUTF8","UTF8ToString"]' \
-s EXPORTED_FUNCTIONS='["_main","_jsAddExpense","_jsDeleteExpense","_jsClearAllExpenses","_jsGetTotalExpenses","_jsGetExpenseCount","_jsGetCategoryCount","_getExpenseJSON","_getCategoryTotalJSON","_freeMemory","_malloc","_free"]' \
--shell-file index.html -s ALLOW_MEMORY_GROWTH=1
```

* Запуск приложения

Выходим из контейнера

```
exit
```

![image](https://github.com/user-attachments/assets/95cf49f9-545b-4966-bdaf-4a0b1cfd8ff9)


Запускаем веб-сервер для тестирования

```
python -m http.server 8000
```

![image](https://github.com/user-attachments/assets/6d045173-7531-4df3-8fe3-87b10b6a41eb)


Открываем в браузере адрес

```
http://localhost:8000
```

![image](https://github.com/user-attachments/assets/0c15144f-03fd-4203-80ce-780c83edbc5a)
