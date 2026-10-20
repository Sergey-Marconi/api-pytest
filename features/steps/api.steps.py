import json

import requests
import os
from behave import given, when, then

from helpers import get_base_url, build_url, assert_dicts_equal

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

headers = {
         "Accept": "application/json",
         "Authorization": f"Token {API_KEY}",
         "X-Secret": f"{SECRET_KEY}"
     }


@given('я планирую вызвать метод "{path}"')
def step_get_url(context, path):
    url = get_base_url()
    context.path = build_url(url, path)


@when("тело запроса будет:")
def step_set_body(context):
    body_text = context.text
    context.payload = json.loads(body_text)

# @when("запрос будет содержать следующие заголовки:")
# def step_set_headers(context):
#     context.headers = set_headers(context.text)


@when('я делаю "{method}" вызов')
def set_method(context, method):
    method = method.upper()
    # headers = context.payload['headers']
    payload = context.payload['payload']
    req = getattr(requests, method.lower())
    context.resp = req(context.path, headers=headers, json=payload)


@then('статус ответа будет {code:d}')
def assert_code(context, code):
    actual_code = context.resp.status_code
    if actual_code != code:
        raise AssertionError(f"\nExpected {code} status code\nActual {actual_code} status code")
    assert actual_code == code

@when('тело ответа метода игнорирует ключ {ignore_key} и совпадает с ответом из json {path}')
def resp_equal_with_ignore(context, ignore_key, path):
      with open(path, "r", encoding="utf-8") as f:
        file_obj = json.load(f)
    resp_obj = context.resp.json()  # или json.loads(context.resp.text)
    assert_dicts_equal(resp_obj, file_obj, ignore_key=[ignore_key])


@when("тело ответа метода совпадает с ответом из json {}")
def resp_equal(context, path):
    with open(path, "r", encoding="utf-8") as f:
        file_obj = json.load(f)
    resp_obj = context.resp.json()
    assert_dicts_equal(resp_obj, file_obj)
