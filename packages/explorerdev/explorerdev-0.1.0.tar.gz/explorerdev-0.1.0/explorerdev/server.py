import os
import socket
import threading

local_ip = "127.0.0.1"
local_port = 8848

def get_drives():
    drives = [letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.isdir(f"{letter}:\\")]
    return drives

def list_files(path):
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Ошибка: {str(e)}"]

def handle_client(client_socket):
    client_socket.send("Введите пароль: ".encode("utf-8"))
    password = client_socket.recv(1024).decode("utf-8", errors="ignore").strip()

    if password != "1613":
        client_socket.send("Неверный пароль.\n".encode("utf-8"))
        client_socket.close()
        return

    client_socket.send("Подключено к удаленному серверу.\n".encode("utf-8"))
    current_path = ""

    while True:
        drives = get_drives()
        drives_str = "Доступные диски: " + ", ".join(drives) + "\nВыберите диск (например, C, D) или 'exit' для выхода: "
        client_socket.send(drives_str.encode("utf-8"))
        
        drive = client_socket.recv(1024).decode("utf-8", errors="ignore").strip()
        if drive.lower() == "exit":
            client_socket.send("До свидания!\n".encode("utf-8"))
            break

        if drive.upper() in drives:
            current_path = f"{drive.upper()}:\\"
            client_socket.send(f"Вы находитесь в {current_path}\n".encode("utf-8"))
        else:
            client_socket.send("Неверный диск.\n".encode("utf-8"))
            continue

        while True:
            files = list_files(current_path)
            files_str = f"Вы находитесь в {current_path}\nСписок файлов и папок:\n" + "\n".join([f"  {f}" for f in files]) + "\n"
            client_socket.send(files_str.encode("utf-8"))

            file_choice = client_socket.recv(1024).decode("utf-8", errors="ignore").strip()
            if file_choice.lower() == "back":
                client_socket.send(f"Возврат к выбору дисков.\n".encode("utf-8"))
                break

            new_path = os.path.join(current_path, file_choice)

            if os.path.isdir(new_path):
                current_path = new_path
                client_socket.send(f"Вы перешли в {new_path}\n".encode("utf-8"))
            elif os.path.isfile(new_path):
                try:
                    with open(new_path, "rb") as f:
                        client_socket.send(f"Отправка файла {file_choice} началась\n".encode("utf-8"))
                        file_data = f.read(1024)
                        while file_data:
                            client_socket.send(file_data)
                            file_data = f.read(1024)
                        client_socket.send(b"")  # Сигнал окончания данных файла
                    # Отправляем сообщение о завершении после файла
                    client_socket.send(f"Файл {file_choice} успешно отправлен на клиент.\n".encode("utf-8"))
                except Exception as e:
                    client_socket.send(f"Ошибка при отправке файла: {str(e)}\n".encode("utf-8"))
            elif file_choice.startswith("upload "):
                file_name = file_choice.split(" ", 1)[1]
                new_path = os.path.join(current_path, file_name)
                try:
                    with open(new_path, "wb") as f:
                        while True:
                            file_data = client_socket.recv(1024)
                            if not file_data:
                                break
                            f.write(file_data)
                    client_socket.send(f"Файл {file_name} успешно получен на сервере.\n".encode("utf-8"))
                except Exception as e:
                    client_socket.send(f"Ошибка при получении файла: {str(e)}\n".encode("utf-8"))
            else:
                client_socket.send("Неверный выбор. Выберите существующий файл, папку или используйте 'upload <filename>'.\n".encode("utf-8"))

    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((local_ip, local_port))
server.listen(5)
print(f"Сервер запущен на {local_ip}:{local_port}")

while True:
    client, addr = server.accept()
    print(f"Подключен клиент: {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()