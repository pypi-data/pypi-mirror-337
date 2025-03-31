import os
import socket
import threading
import zipfile

local_ip = "0.0.0.0"
local_port = 8848

def get_drives():
    drives = [letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.isdir(f"{letter}:\\")]
    return drives

def list_files(path):
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Ошибка: {str(e)}"]

def zip_folder(folder_path, zip_path):
    print(f"Создаю ZIP для {folder_path} в {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                zipf.write(file_path, arcname)
    print(f"ZIP создан: {zip_path}, размер: {os.path.getsize(zip_path)} байт")
    return zip_path

def handle_client(client_socket):
    try:
        client_socket.send("Введите пароль: ".encode("utf-8"))
        password = client_socket.recv(1024).decode("utf-8", errors="ignore").strip()

        if password != "1613":
            client_socket.send("Неверный пароль.\n".encode("utf-8"))
            client_socket.close()
            return

        client_socket.send("Подключено к удалённому серверу.\n".encode("utf-8"))
        current_path = ""

        while True:
            drives = get_drives()
            drives_str = "Доступные диски: " + ", ".join(drives) + "\nВыберите диск (например, C, D) или 'exit' для выхода: "
            print(f"Отправляю клиенту: {drives_str.strip()}")
            client_socket.send(drives_str.encode("utf-8"))
            
            drive = client_socket.recv(1024).decode("utf-8", errors="ignore").strip()
            print(f"Получил от клиента: {drive}")
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
                print(f"Отправляю клиенту список файлов: {files_str.strip()}")
                client_socket.send(files_str.encode("utf-8"))

                file_choice = client_socket.recv(1024).decode("utf-8", errors="ignore").strip()
                print(f"Получил от клиента: {file_choice}")

                if file_choice.lower() == "back":
                    client_socket.send(f"Возврат к выбору дисков.\n".encode("utf-8"))
                    break

                new_path = os.path.join(current_path, file_choice)

                if file_choice.startswith("zip "):
                    folder_name = file_choice.split(" ", 1)[1].strip()
                    folder_path = os.path.join(current_path, folder_name)
                    print(f"Обрабатываю команду zip для папки: {folder_path}")
                    if os.path.isdir(folder_path):
                        zip_path = f"{folder_path}.zip"
                        try:
                            zip_folder(folder_path, zip_path)
                            file_size = os.path.getsize(zip_path)
                            msg = f"Архив {folder_name}.zip создан, отправка началась (размер: {file_size} байт)\n"
                            print(f"Отправляю клиенту: {msg.strip()}")
                            client_socket.send(msg.encode("utf-8"))
                            print(f"Отправляю размер файла: {file_size}")
                            client_socket.send(str(file_size).encode("utf-8") + b"\n")
                            print("Начинаю отправку данных...")
                            with open(zip_path, "rb") as f:
                                bytes_sent = 0
                                file_data = f.read(8192)
                                while file_data:
                                    client_socket.send(file_data)
                                    bytes_sent += len(file_data)
                                    print(f"Отправлено {bytes_sent}/{file_size} байт ({(bytes_sent/file_size)*100:.1f}%)...", end="\r")
                                    file_data = f.read(8192)
                                client_socket.send(b"")
                            print(f"\nОтправка {folder_name}.zip завершена ({bytes_sent} байт)")
                            client_socket.send(f"Архив {folder_name}.zip успешно отправлен\n".encode("utf-8"))
                            os.remove(zip_path)
                            print(f"Удалён временный файл {zip_path}")
                        except Exception as e:
                            error_msg = f"Ошибка при создании или отправке архива: {str(e)}\n"
                            print(f"Ошибка: {error_msg.strip()}")
                            client_socket.send(error_msg.encode("utf-8"))
                            if os.path.exists(zip_path):
                                os.remove(zip_path)
                    else:
                        client_socket.send(f"Папка {folder_name} не найдена\n".encode("utf-8"))
                elif os.path.isdir(new_path):
                    current_path = new_path
                    client_socket.send(f"Вы перешли в {new_path}\n".encode("utf-8"))
                elif os.path.isfile(new_path):
                    try:
                        file_size = os.path.getsize(new_path)
                        client_socket.send(f"Отправка файла {file_choice} началась (размер: {file_size} байт)\n".encode("utf-8"))
                        client_socket.send(str(file_size).encode("utf-8") + b"\n")
                        with open(new_path, "rb") as f:
                            bytes_sent = 0
                            file_data = f.read(8192)
                            while file_data:
                                client_socket.send(file_data)
                                bytes_sent += len(file_data)
                                print(f"Отправлено {bytes_sent} байт...", end="\r")
                                file_data = f.read(8192)
                            client_socket.send(b"")
                        print(f"\nОтправка {file_choice} завершена ({bytes_sent} байт)")
                        client_socket.send(f"Файл {file_choice} успешно отправлен\n".encode("utf-8"))
                    except Exception as e:
                        client_socket.send(f"Ошибка при отправке файла: {str(e)}\n".encode("utf-8"))
                elif file_choice.startswith("upload "):
                    file_name = file_choice.split(" ", 1)[1]
                    new_path = os.path.join(current_path, file_name)
                    try:
                        with open(new_path, "wb") as f:
                            while True:
                                file_data = client_socket.recv(8192)
                                if not file_data:
                                    break
                                f.write(file_data)
                        client_socket.send(f"Файл {file_name} успешно получен на сервере\n".encode("utf-8"))
                    except Exception as e:
                        client_socket.send(f"Ошибка при получении файла: {str(e)}\n".encode("utf-8"))
                else:
                    client_socket.send("Неверный выбор. Используйте 'zip <folder>', файл, папку или 'upload <filename>'\n".encode("utf-8"))

    except Exception as e:
        print(f"Ошибка в handle_client: {e}")
    finally:
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((local_ip, local_port))
server.listen(5)
print(f"Сервер запущен на {local_ip}:{local_port}")

while True:
    client, addr = server.accept()
    print(f"Подключён клиент: {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()