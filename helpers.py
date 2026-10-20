import os

from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
# API_KEY = os.getenv("API_KEY")
# SECRET_KEY = os.getenv("SECRET_KEY")

def get_base_url():
    if not BASE_URL:
        raise AssertionError("Base URL not set")
    return BASE_URL

def build_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + "/" + path.lstrip("/")

# def set_headers(headers: dict):
#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Token {API_KEY}",
#         "X-Secret": f"{SECRET_KEY}"
#     }
#     return headers

import json


def assert_dicts_equal(actual, expected, path="", ignore_keys=None):
    if ignore_keys is None:
        ignore_keys = []

    # --- Защита от строк ---
    if isinstance(actual, str):
        import json
        actual = json.loads(actual)
    if isinstance(expected, str):
        import json
        expected = json.loads(expected)

    # --- Защита от списков (если пришел [{...}]) ---
    if isinstance(actual, list) and len(actual) > 0:
        actual = actual[0]
    if isinstance(expected, list) and len(expected) > 0:
        expected = expected[0]

    errors = []

    for key in expected:
        # ПРОПУСКАЕМ ИГНОРИРУЕМЫЕ КЛЮЧИ
        if key in ignore_keys:
            continue

        current_path = f"{path}.{key}" if path else key

        if key not in actual:
            errors.append(f"Отсутствует ключ '{current_path}' в ответе")
        elif isinstance(expected[key], dict) and isinstance(actual[key], dict):
            # Рекурсивный вызов (передаем ignore_keys дальше)
            assert_dicts_equal(actual[key], expected[key], current_path, ignore_keys)
        elif actual[key] != expected[key]:
            errors.append(f"Ключ '{current_path}': ожидалось {expected[key]!r}, получено {actual[key]!r}")

    for key in actual:
        if key in ignore_keys:
            continue

        current_path = f"{path}.{key}" if path else key
        if key not in expected:
            errors.append(f"Лишний ключ '{current_path}' в ответе")

    if errors:
        error_message = "\n".join(f" - {err}" for err in errors)
        raise AssertionError(f"Ответ не совпадает с эталоном:\n{error_message}")
