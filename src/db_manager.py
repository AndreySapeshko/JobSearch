from typing import Any
from dotenv import load_dotenv
from psycopg2 import OperationalError

from src.vacancy import Vacancy

import psycopg2
import os

class DBManager:
    host: str
    database: str
    user: str
    password: str

    def __init__(self) -> None:
        load_dotenv()
        self.host = os.getenv('DATABASE_HOST')
        self.database = os.getenv('DATABASE_NAME')
        self.user = os.getenv('DATABASE_USER')
        self.password = os.getenv('DATABASE_PASSWORD')

    def get_data_from_table(self, cursor, table_name: str) -> list:
        data = []
        try:
            queri = f'SELECT * FROM {table_name}'
            cursor.execute(queri)
            rows = cursor.fetchall()
            for row in rows:
                data.append(row)
        except Exception as e:
            print(f'Не удалось получить данные из таблицы {table_name}, ошибка: {e}')
            data = []
        return data

    def get_arg_from_saved_data(self, args: dict, saved_data: list) -> Any:
        value = None
        if saved_data:
            for data in saved_data:
                is_in_saved_data = True
                for arg in args.values():
                    if arg not in data:
                        is_in_saved_data = False
                if is_in_saved_data:
                    return data[0]
        return value

    def create_insert_sql_query(self,table_name: str, values: dict, returning=None) -> str:
        named_values = ''
        for key in values.keys():
            named_values += f'%({key})s, '
        named_values = named_values[:-2]
        query = (f'INSERT INTO {table_name} ({', '.join(values.keys())})\n'
                 f'VALUES ({named_values})\n')
        if returning:
            query += f'RETURNING {returning}'
        return query

    def check_database_exists(self, db_name: str) -> Any:
        """Проверяет существование базы данных"""

        try:
            conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database='postgres'
            )

            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (db_name,)
                )
                exists = cursor.fetchone() is not None

            conn.close()
            return exists

        except OperationalError as e:
            print(f"Ошибка подключения: {e}")
            return None

    def create_database_with_tables(self, name_database: str) -> None:
        try:
            conn = psycopg2.connect(host=self.host, database='postgres',
                             user=self.user, password=self.password)
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(f'CREATE DATABASE {name_database}')
            conn.close()
        except Exception as e:
            print(f'Ошибка при создании базы: {e}')
            return
        with psycopg2.connect(host=self.host, database=self.database,
                              user=self.user, password=self.password) as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute('''
                        CREATE TABLE salary (
                            id_salary serial,
                            range_salary varchar(40),
                            avg_salary int,

                            CONSTRAINT salary_id_salary PRIMARY KEY (id_salary)
                        )
                    ''')
                    cur.execute('''
                        CREATE TABLE employers (
                            id_employer serial,
                            hh_id_employer varchar(15),
                            name_employer varchar(150),

                            CONSTRAINT employers_id_employer PRIMARY KEY (id_employer)
                        )
                    ''')
                    cur.execute('''
                        CREATE TABLE vacancies (
                            id_vacancy serial,
                            hh_id_vacancy varchar(20),
                            name_vacancy varchar(150),
                            id_salary int,
                            id_employer int,
                            description varchar(1000),
                            requirement varchar(1000),
                            url varchar(50),

                            CONSTRAINT pk_vacancies_id_vacancy PRIMARY KEY (id_vacancy),
                            CONSTRAINT fk_vacancies_salary FOREIGN KEY(id_salary) 
                            REFERENCES salary(id_salary),
                            CONSTRAINT fk_vacancies_employers FOREIGN KEY(id_employer) 
                            REFERENCES employers(id_employer)
                        )
                    ''')
            except Exception as e:
                conn.rollback()
                print(f'Ошибка при создании таблиц: {e}')

    def add_if_new(self, cursor, args: dict, saved_data: list, name_table: str, returning: str = None) -> int:
        id_arg = self.get_arg_from_saved_data(args, saved_data)
        if not id_arg:
            query_to_insert = self.create_insert_sql_query(name_table, args, returning)
            cursor.execute(query_to_insert, args)
            id_arg = cursor.fetchone()[0]
            new_element = [id_arg]
            for arg in args.values():
                new_element.append(arg)
            saved_data.append(tuple(new_element))
        return id_arg


    def update_database(self, vacancies: list[Vacancy]) -> None:
        """ Получает список вакансий, провереяет есть ли такие в БД и записывает новые """

        # Проверяем есть ли необхадимая БД, если нет создаем
        is_database_exist = self.check_database_exists(self.database)
        if is_database_exist is None:
            return
        if not is_database_exist:
            self.create_database_with_tables(self.database)
        with psycopg2.connect(host=self.host, database=self.database,
                              user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                # Получаем данные из таблиц БД
                saved_employers = self.get_data_from_table(cur, 'employers')
                saved_salary = self.get_data_from_table(cur, 'salary')
                saved_vacancies = self.get_data_from_table(cur, 'vacancies')
                for vacancy in vacancies:
                    # Подготавливаем данные из полученных вакансий для таблиц salary и employers в БД
                    table_salary = {
                        'avg_salary': vacancy.salary,
                        'range_salary': vacancy.salary_range[:40]
                    }
                    table_employers = {
                        'name_employer': vacancy.employer[:150],
                        'hh_id_employer': vacancy.employer_id[:15]
                    }
                    # Проверяем есть ли такая запись в таблице salary, если нет записываем и добавляем в список
                    print(saved_salary)
                    id_salary = self.add_if_new(cur, table_salary, saved_salary, 'salary', 'id_salary')

                    # Проверяем есть ли такая запись в таблице employers, если нет записываем и добавляем в список
                    id_employer = self.add_if_new(cur, table_employers, saved_employers, 'employers', 'id_employer')

                    # Подготавливаем данные из полученных вакансий для таблиц vacancies в БД
                    table_vacancies = {
                        'hh_id_vacancy': vacancy.id[:20],
                        'name_vacancy': vacancy.name[:150],
                        'id_salary': id_salary,
                        'id_employer': id_employer,
                        'description': vacancy.description[:1000],
                        'requirement': vacancy.requirement[:1000],
                        'url': vacancy.url[:50]
                    }

                    # Проверяем есть ли такая запись в таблице vacancies, если нет записываем и добавляем в список
                    self.add_if_new(cur, table_vacancies, saved_vacancies, 'vacancies', 'id_vacancy')
