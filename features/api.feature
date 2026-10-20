Feature: test

  @test
  Scenario: test
    Given я планирую вызвать метод "/api/v1/clean/address"
#    When запрос будет содержать следующие заголовки:
#    """
#    { "Content-Type": "application/json"}
#    """
    When тело запроса будет:
    """
    {"payload": ["мск сухонска 11/-89"]}
    """
    When я делаю "POST" вызов
    Then статус ответа будет 200
#    When тело ответа метода совпадает с ответом из json "features/data/response.json"
    When тело ответа метода игнорирует ключ в ответе "metro" и совпадает с ответом из json "features/data/response.json"
