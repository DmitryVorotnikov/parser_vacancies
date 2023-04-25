from classes import HeadHunterAPI, JSONSaver, SuperJobAPI
from utils import working_with_data


def user_interaction():
    """
    Пользовательский интерфейс для парсера вакансий.
    """
    # Список платформ для парсинга.
    platforms = ["HeadHunter", "SuperJob"]

    # Приветствие.
    print(f"""          ПАРСЕР ВАКАНСИЙ
Перед началом: Пользователю необходимо выбирать варианты ответов посредством указания цифр.""")

    # Пользователь выбирает платформу из списка platforms.
    while True:
        try:
            users_input_platform = int(input(f"""На какой платформе хотите собрать информацию о вакансиях?
Варианты: 1 - {platforms[0]}, 2 - {platforms[1]}.\n"""))
        except ValueError:
            print('Введите корректные данные!')
        else:
            if users_input_platform not in range(1, len(platforms) + 1):
                print('Введите корректные данные!')
            else:
                break

    # Пользователь вводит поисковый запрос.
    users_input_keyword = input(f"Введите поисковый запрос:\n")

    # Если пользователь выбрал HeadHunter.
    if users_input_platform == 1:
        # Создание экземпляра класса для работы с API сайта с вакансиями.
        hh_api = HeadHunterAPI()
        # Получение вакансий с разных платформ.
        hh_vacancies = hh_api.get_vacancies(users_input_keyword)
        # Сохранение информации о вакансиях в файл user_input_keyword.json и переменную data.
        json_saver = JSONSaver(users_input_keyword)
        json_saver.add_vacancies(hh_vacancies)
        data = json_saver.select_hh()
        # Выбор пользователем способа валидации данных и возврат print_vacancies для печати в консоль.
        print_vacancies = working_with_data(data)
        # Печать в консоль.
        for i in print_vacancies:
            print(i, end=f'\n{"=" * 100}\n')

    # Если пользователь выбрал SuperJob.
    elif users_input_platform == 2:
        # Создание экземпляра класса для работы с API сайта с вакансиями.
        sj_api = SuperJobAPI()
        # Получение вакансий с разных платформ.
        sj_vacancies = sj_api.get_vacancies(users_input_keyword)
        # Сохранение информации о вакансиях в файл user_input_keyword.json и переменную data.
        json_saver = JSONSaver(users_input_keyword)
        json_saver.add_vacancies(sj_vacancies)
        data = json_saver.select_sj()
        # Выбор пользователем способа валидации данных и возврат print_vacancies для печати в консоль.
        print_vacancies = working_with_data(data)
        # Печать в консоль.
        for i in print_vacancies:
            print(i, end=f'\n{"=" * 100}\n')


while True:
    user_interaction()
