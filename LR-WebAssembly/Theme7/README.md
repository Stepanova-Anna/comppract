Адрес Cloud Function

![image](https://github.com/user-attachments/assets/5f34f97b-70f6-43a2-8402-6814c71ed980)

![image](https://github.com/user-attachments/assets/91f9fc32-5b5f-4a7e-9abd-0dccc7acfd8b)

![image](https://github.com/user-attachments/assets/3594c03a-f5a9-4747-af56-9737e76e64a0)

API Gateway в Yandex Cloud перенаправляет все POST-запросы, отправленные на корневой путь (/), в указанную Cloud Function. Cloud Function обрабатывает запрос и отправляет ответ. API Gateway возвращает ответ Telegram Bot API (который, в свою очередь, передает его пользователю Telegram).

![image](https://github.com/user-attachments/assets/8a064dea-a139-4dd2-8572-9c11739d7c57)


Ник Telegram-бота: @ya_translaterbot
