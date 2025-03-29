# explorerdev/client.py
import socket
import os
import sys

def main():
    """Точка входа для команды explorerdev."""
    local_ip = "127.0.0.1"
    local_port = 8848

    # Создаём сокет
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10)

    # Подключение к серверу
    try:
        client.connect((local_ip, local_port))
        print("Запускаю клиентскую версию explorerdev...")
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу.")
        sys.exit(1)

    # Авторизация
    response = client.recv(1024).decode("utf-8")
    print(response, end="")
    password = input()
    client.send(password.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)

    while True:
        # Выбор диска
        response = client.recv(1024).decode("utf-8")
        print(response, end="")
        choice = input()
        client.send(choice.encode("utf-8"))

        if choice.lower() == "exit":
            response = client.recv(1024).decode("utf-8")
            print(response)
            break

        # Ответ сервера после выбора диска
        response = client.recv(1024).decode("utf-8")
        print(response)

        while True:
            # Получаем список файлов
            response = client.recv(4096).decode("utf-8")
            print(response)
            file_choice = input("Введите имя файла для скачивания, название папки чтобы перейти или 'back' для возврата: ")
            client.send(file_choice.encode("utf-8"))

            # Получаем ответ от сервера
            response = client.recv(1024).decode("utf-8")
            print(response)

            if file_choice.lower() == "back":
                break

            # Скачивание файла
            if "Отправка файла" in response:
                file_name = file_choice
                try:
                    with open(file_name, "wb") as f:
                        while True:
                            file_data = client.recv(1024)
                            if not file_data:  # Пустой пакет — конец данных файла
                                break
                            f.write(file_data)
                    print(f"Файл {file_name} успешно загружен на клиент.")
                    # Получаем подтверждение от сервера
                    response = client.recv(1024).decode("utf-8")
                    print(response)
                except Exception as e:
                    print(f"Ошибка при загрузке файла: {e}")

            # Загрузка файла на сервер (хотя в твоём примере этой функции нет, оставлю для совместимости)
            elif file_choice.startswith("upload "):
                file_name = file_choice.split(" ", 1)[1]
                if os.path.isfile(file_name):
                    try:
                        with open(file_name, "rb") as f:
                            file_data = f.read(1024)
                            while file_data:
                                client.send(file_data)
                                file_data = f.read(1024)
                            client.send(b"")
                        print(f"Файл {file_name} успешно отправлен на сервер.")
                        response = client.recv(1024).decode("utf-8")
                        print(response)
                    except Exception as e:
                        print(f"Ошибка при отправке файла: {e}")
                else:
                    print(f"Файл {file_name} не найден на клиенте.")

    client.close()
    print("Соединение закрыто.")

if __name__ == "__main__":
    main()