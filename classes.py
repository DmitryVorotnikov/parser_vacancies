from __future__ import annotations

import json
from abc import ABC, abstractmethod

import requests


class Engine(ABC):
    """
    Абстрактный класс от которого наследуются классы для взаимодействия с API.
    """

    @abstractmethod
    def get_request(self, keyword: str, page: str) -> list:
        """
        Абстрактный метод, возвращает список-ответ от API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list:
        """
        Метод возвращает список-ответ от API с 5 страниц.
        """
        pass


class HeadHunterAPI(Engine):
    """
    Класс для работы с API HeadHunter.
    """

    def get_request(self, keyword: str, page: int) -> list:
        """
        Метод возвращает список-ответ от API с одной страницы.
        """
        params = {
            "text": keyword,
            "page": page,
            "per_page": 100,
        }
        return requests.get("https://api.hh.ru/vacancies", params=params).json()['items']

    def get_vacancies(self, keyword: str) -> list:
        """
        Метод возвращает список-ответ от API с 5 страниц.
        """
        pages = 5
        response = []

        for page in range(pages):
            print(f'Парсинг страницы {page + 1}', end=': ')
            values = self.get_request(keyword, page)
            print(f'Найдено {len(values)} вакансий.\n')
            response.extend(values)

        return response


class SuperJobAPI(Engine):
    """
    Класс для работы с API SuperJob.
    """
    superjob_key = 'v3.r.137501496.9e6dec807889aca00645427d37f8eabccf7d345b.9aa8abd7103384abb524f6682cc2aa5cfa21399d'

    def get_request(self, keyword: str, page: int) -> list:
        """
        Метод возвращает список-ответ от API с одной страницы.
        """
        params = {
            "keyword": keyword,
            "page": page,
            "per_page": 100,
            "count": 100,
        }
        my_auth_data = {'X-Api-App-Id': self.superjob_key}

        return requests.get('https://api.superjob.ru/2.0/vacancies/', headers=my_auth_data, params=params).json()[
            'objects']

    def get_vacancies(self, keyword: str) -> list:
        """
        Метод возвращает список-ответ от API с 5 страниц.
        """
        pages = 5
        response = []

        for page in range(pages):
            print(f'Парсинг страницы {page + 1}', end=': ')
            values = self.get_request(keyword, page)
            print(f'Найдено {len(values)} вакансий.\n')
            response.extend(values)

        return response


class Vacancy:
    """
    Класс для работы с вакансиями.
    """
    __slots__ = (
        'title', 'salary_min', 'salary_max', 'currency', 'employer', 'link', 'salary_sort_min', 'salary_sort_max')

    def __init__(self, title: str, salary_min: int, salary_max: int, currency: str, employer: str, link: str) -> None:
        self.title = title  # Заголовок вакансии.
        self.salary_min = salary_min  # Минимальная зарплата.
        self.salary_max = salary_max  # Максимальная зарплата.
        self.currency = currency  # Валюта зарплаты.
        self.employer = employer  # Имя работодателя.
        self.link = link  # Ссылка на работодателя.

        self.salary_sort_min: int = salary_min
        self.salary_sort_max: int = salary_max

        # Для сравнения зарплат 'USD' и 'RUB'. Курс по умолчанию 81.
        if currency and currency == 'USD' or 'usd':
            self.salary_sort_min = self.salary_sort_min * 81 if self.salary_sort_min else None
            self.salary_sort_max = self.salary_sort_max * 81 if self.salary_sort_max else None

    def __str__(self) -> str:
        """
        Метод для печати в консоль вакансий.
        """
        salary_min = f'От {self.salary_min}' if self.salary_min else ''
        salary_max = f'От {self.salary_max}' if self.salary_max else ''
        currency = self.currency if self.currency else ''
        if self.salary_min is None and self.salary_max is None:
            salary_min = 'Не указана'
        return f'{self.employer}: {self.title} \n{salary_min} {salary_max} {currency} \nURL: {self.link}'

    def __gt__(self, other: Vacancy) -> bool:
        """
        Метод для сравнения зарплат.
        """
        if not other.salary_sort_min:
            return True
        if not self.salary_sort_min:
            return False
        return self.salary_sort_min >= other.salary_sort_min


class JSONSaver:
    """
    Метод для работы с json файлом с вакансиями.
    """

    def __init__(self, keyword: str) -> None:
        """
        Инициализатор сохранит в атрибут self.__filename название файла с вакансиями.
        """
        self.__filename = f'{keyword.title()}.json'

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data: list) -> None:
        """
        Метод создаст и перезапишет файл с вакансиями.
        """
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select_hh(self) -> list:
        """
        Метод прочтет файл с вакансиями из HeadHunter и создаст список с экземплярами класса Vacancy.
        """
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []

        for row in data:
            salary_min, salary_max, currency = None, None, None
            if row['salary']:
                salary_min, salary_max, currency = row['salary']['from'], row['salary']['to'], row['salary']['currency']
            vacancies.append(
                Vacancy(row['name'], salary_min, salary_max, currency, row['employer']['name'], row['alternate_url']))
        return vacancies

    def select_sj(self) -> list:
        """
        Метод прочтет файл с вакансиями из SuperJob и создаст список с экземплярами класса Vacancy.
        """
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []

        for row in data:
            try:
                salary_min, salary_max, currency = None, None, None
                salary_min, salary_max, currency = row['payment_from'], row['payment_to'], row['currency']
                vacancies.append(Vacancy(row['profession'], salary_min, salary_max, currency, row['client']['title'],
                                         row['client']['url']))
            except KeyError:
                continue
        return vacancies
