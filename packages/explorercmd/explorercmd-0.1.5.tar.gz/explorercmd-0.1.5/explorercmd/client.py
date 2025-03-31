import socket
import os
import sys

def main():
    remote_ip = "figure-rendering.gl.at.ply.gg"
    remote_port = 65300

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(None)

    try:
        print(f"Пытаюсь подключиться к {remote_ip}:{remote_port}...")
        client.connect((remote_ip, remote_port))
        print("Запускаю клиентскую версию explorercmd...")
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        sys.exit(1)

    response = client.recv(1024).decode("utf-8")
    print(response, end="")
    password = input()
    client.send(password.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)

    if "Неверный пароль" in response:
        client.close()
        sys.exit(1)

    print("Куда сохранять файлы? (Например, C:\\ или C:\\Downloads, оставьте пустым для C:\\)")
    save_path = input().strip()
    if not save_path:
        save_path = "C:\\"
    
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        if not os.path.isdir(save_path):
            print(f"Ошибка: {save_path} не является директорией")
            client.close()
            sys.exit(1)
    except Exception as e:
        print(f"Ошибка при создании директории {save_path}: {e}")
        client.close()
        sys.exit(1)

    print(f"Файлы будут сохраняться в {save_path}")

    while True:
        try:
            print("Ожидаю данные от сервера...")
            response = client.recv(1024).decode("utf-8")
            print(response, end="")
            print("Готов к вводу выбора диска или команды...")
            choice = input()
            print(f"Отправляю серверу: {choice}")
            client.send(choice.encode("utf-8"))

            if choice.lower() == "exit":
                response = client.recv(1024).decode("utf-8")
                print(response)
                break

            print("Ожидаю подтверждение от сервера...")
            response = client.recv(1024).decode("utf-8")
            print(response)

            while True:
                print("Ожидаю список файлов...")
                response = client.recv(4096).decode("utf-8")
                print(response)
                file_choice = input("Введите имя файла, папку, 'zip <folder>', 'upload <filename>' или 'back': ")
                print(f"Отправляю серверу: {file_choice}")
                client.send(file_choice.encode("utf-8"))

                print("Ожидаю ответ от сервера...")
                # Читаем текстовый ответ до новой строки
                response_data = b""
                while b"\n" not in response_data:
                    chunk = client.recv(1)
                    if not chunk:
                        raise Exception("Соединение прервано во время чтения ответа")
                    response_data += chunk
                response = response_data.decode("utf-8")
                print(response)

                if file_choice.lower() == "back":
                    break

                if "Отправка файла" in response or ("Архив" in response and "отправка началась" in response):
                    file_name = file_choice.split(" ", 1)[1] + ".zip" if file_choice.startswith("zip ") else file_choice
                    file_path = os.path.join(save_path, file_name)
                    temp_file_path = file_path + ".tmp"

                    try:
                        # Читаем размер файла до новой строки
                        size_data = b""
                        while b"\n" not in size_data:
                            chunk = client.recv(1)
                            if not chunk:
                                raise Exception("Не удалось получить размер файла")
                            size_data += chunk
                        file_size = int(size_data.decode("utf-8").strip())
                        print(f"Начинаю загрузку {file_name} в {save_path} (размер: {file_size} байт)...")

                        # Принимаем бинарные данные
                        bytes_received = 0
                        with open(temp_file_path, "wb") as f:
                            while bytes_received < file_size:
                                remaining = file_size - bytes_received
                                buffer_size = min(8192, remaining)
                                file_data = client.recv(buffer_size)
                                if not file_data:
                                    print(f"\nСоединение прервано: Получено только {bytes_received} из {file_size} байт")
                                    break
                                f.write(file_data)
                                bytes_received += len(file_data)
                                if bytes_received % 1048576 == 0 or bytes_received == file_size:
                                    print(f"Получено {bytes_received}/{file_size} байт ({(bytes_received/file_size)*100:.1f}%)...")
                        
                        print(f"\nЗагрузка завершена: получено {bytes_received} из {file_size} байт")
                        if bytes_received == file_size:
                            os.rename(temp_file_path, file_path)
                            print(f"Файл успешно сохранён как {file_path}")
                        else:
                            print(f"Ошибка: Файл не полностью загружен, удаляю {temp_file_path}")
                            if os.path.exists(temp_file_path):
                                os.remove(temp_file_path)
                        
                        response = client.recv(1024).decode("utf-8")
                        print(response)
                    except Exception as e:
                        print(f"\nОшибка при загрузке файла {file_name}: {e}")
                        if os.path.exists(temp_file_path):
                            os.remove(temp_file_path)

                elif file_choice.startswith("upload "):
                    file_name = file_choice.split(" ", 1)[1]
                    if os.path.isfile(file_name):
                        try:
                            with open(file_name, "rb") as f:
                                file_data = f.read(8192)
                                while file_data:
                                    client.send(file_data)
                                    file_data = f.read(8192)
                                client.send(b"")
                            print(f"Файл {file_name} успешно отправлен на сервер.")
                            response = client.recv(1024).decode("utf-8")
                            print(response)
                        except Exception as e:
                            print(f"Ошибка при отправке файла: {e}")
                    else:
                        print(f"Файл {file_name} не найден на клиенте.")
        except Exception as e:
            print(f"Ошибка соединения: {e}")
            break

    client.close()
    print("Соединение закрыто.")

if __name__ == "__main__":
    main()