def working_with_data(data):
    """
    Функциям принимает выбранный пользователем способ валидации данных и возвращает список для печати в консоль.
    """
    # Список способов валидации данных по вакансиям.
    features = ["Показать сначала низко оплачиваемые", "показать сначала высоко оплачиваемые",
                "Показать топ N вакансий"]

    # Пользователь выбирает способ валидации данных по вакансиям.
    while True:
        try:
            users_input_feature = int(input(f"""Выберите способ валидации данных по вакансиям.
Варианты: 1 - {features[0]}, 2 - {features[1]}, 3 - {features[2]}.\n"""))
        except ValueError:
            print('Введите корректные данные!')
        else:
            if users_input_feature not in range(1, len(features) + 1):
                print('Введите корректные данные!')
            else:
                break

    # Если пользователь выбрал "Показать сначала низко оплачиваемые".
    if users_input_feature == 1:
        sort_by_salary_min_list = sort_by_salary_min(data)
        return sort_by_salary_min_list

    # Если пользователь выбрал "Показать сначала высоко оплачиваемые".
    if users_input_feature == 2:
        sort_by_salary_min_max = sort_by_salary_max(data)
        return sort_by_salary_min_max

    # Если пользователь выбрал "Показать топ N вакансий".
    if users_input_feature == 3:
        # Пользователь выбирает топ из скольки вакансий.
        while True:
            try:
                users_input_number = int(input('Выберите топ из скольки вакансий:\n'))
            except ValueError:
                print('Введите корректные данные!')
            else:
                break

        sort_by_salary_min_top_n = get_top_n(data, users_input_number)
        return sort_by_salary_min_top_n


def sort_by_salary_min(data: list) -> list:
    """
    Отсортирует вакансии "показать сначала низко оплачиваемые"
    """
    data = sorted(data, reverse=True)
    return data


def sort_by_salary_max(data: list) -> list:
    """
    Отсортирует вакансии "показать сначала высоко оплачиваемые"
    """
    data = sorted(data, key=lambda x: (x.salary_sort_max is not None, x.salary_sort_max), reverse=True)
    return data


def get_top_n(data: list, number: int) -> list:
    """
    Вернет топ number вакансий по зарплате.
    """
    data = sorted(data, key=lambda x: (x.salary_max is not None, x.salary_max), reverse=True)
    return data[:number]
