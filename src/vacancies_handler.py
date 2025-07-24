from src.api_request_handler import ApiRequestHandler
from src.base_vacancy import BaseVacancy


class VacanciesHandler:
    """ Класс объект которого обрабатывает все вакансии полученные с различных сайтов """

    vacancies: list[BaseVacancy]
    num_top_vacancies: int
    key_words: list

    def __init__(self, vacancies: list[BaseVacancy], num_top_vacancies: int, key_words: list) -> None:
        self.vacancies = vacancies
        self.num_top_vacancies = num_top_vacancies
        self.key_words = key_words

    def filter_vacancies(self) -> None:
        """ Фильтрует вакансии по ключевым слова, проверяет их вхождение в name и requirement.
         Если список ключевых слов пустой вернет не филтьрованный список. """

        filtered_vacancies =[]
        if len(self.key_words) == 0:
            return self.vacancies
        for vacancy in self.vacancies:
            for word in self.key_words:
                if vacancy.requirement and word in vacancy.requirement:
                    filtered_vacancies.append(vacancy)
                    break
                if vacancy.name and word in vacancy.name:
                    filtered_vacancies.append(vacancy)
                    break
        return filtered_vacancies

    def sort_vacancy(self, reverse=False) -> list:
        """ Сортерует список вакансий по полю salary. По умолчанию по возростанию,
        если reverse=True по убыванию """

        return sorted(self.vacancies, reverse=reverse)

    def get_top_vacancies(self) -> list:
        """ Возвращает список топ вакансий, длина списка в поле num_top_vacancies объекта """

        sorted_vacancies = self.sort_vacancy(reverse=True)
        return sorted_vacancies[:self.num_top_vacancies]
