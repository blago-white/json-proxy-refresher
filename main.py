import os
import json
import time


def get_validated_path(path_tip: str):
    path = input(path_tip)

    if not os.path.exists(path):
        print("! Введен неверный путь")
        raise ValueError

    return path


def get_proxies_list(path: str) -> list[str]:
    with open(path, encoding="utf-8") as file:
        proxies = file.readlines()

    return [p.lstrip().rstrip() for p in proxies]


def get_sessions_list(path: str) -> list[dict]:
    sessions_files = []
    sessions = []

    for (dirpath, dirnames, filenames) in os.walk(path):
        sessions_files.extend(filenames)
        break

    for session_file_path in sessions_files:
        with open(path + "\\" + session_file_path, encoding="utf-8") as file:
            sessions.append(json.loads(file.read()))

    return sessions


def update_sessions_config_file(sessions: list[dict], proxies: list[str]):
    number = 1

    for session, proxy in zip(sessions, proxies):
        proxy = proxy.split(":")

        session["bean"]["addr"] = proxy[0]
        session["bean"]["password"] = proxy[-1]
        session["bean"]["username"] = proxy[-2]
        session["bean"]["port"] = proxy[1]

        name: str = session["bean"]["name"]
        new_name = name.removesuffix("".join(list(filter(lambda c: c.isdigit(), name))))

        new_name += str(number)

        session["bean"]["name"] = new_name

        number += 1

    return sessions


def save_new_sessions(sessions: list[dict], path: str):
    sessions_files = []

    for (dirpath, dirnames, filenames) in os.walk(path):
        sessions_files.extend(filenames)
        break

    for idx, session_file_path in enumerate(sessions_files):
        with open(path + "\\" + session_file_path, encoding="utf-8", mode="w") as file:
            file.write(json.dumps(sessions[idx]))


print("Для прерывания ввода: Ctrl+C")

while True:
    time.sleep(1)

    try:
        proxies_file_path = get_validated_path(path_tip="Путь до файла прокси: ")

        accounts_json_file_path = get_validated_path(path_tip="Путь до файла сессий: ")
    except:
        continue

    proxies, sessions = get_proxies_list(
        proxies_file_path
    ), get_sessions_list(
        accounts_json_file_path
    )

    if len(sessions) > len(proxies):
        print("Ошибка: Кол-во сессий > кол-во прокси, вы можете ввести новые пути, или отредактировать файл(-ы)")
        continue

    if not len(proxies):
        print("Файлы пустые.")
        continue

    update_sessions_config_file(sessions=sessions, proxies=proxies)

    save_new_sessions(sessions=sessions, path="D:\\FDISKCOPY\\python\\json-proxy-refresher\\jsons")

    print("Обновлено!")
    break
