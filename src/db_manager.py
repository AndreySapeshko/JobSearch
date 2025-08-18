from typing import Any

import psycopg2

from pathlib import Path

from src.hh_reader_vacancies import HhReaderVacancies
from src.vacancy import Vacancy

import psycopg2

class DBManager:
    host: str
    database: str
    user: str
    password: str

    def __init__(self, host: str, database: str, user: str, password: str) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def get_data_from_table(self, cursor, table_name: str) -> list:
        data = []
        queri = f'SELECT * FROM {table_name}'
        cursor.execute(queri)
        rows = cursor.fetchall()
        for row in rows:
            data.append(row)
        return data

    def get_arg_from_saved_data(self, *args, saved_data: list) -> Any:
        value = None
        for data in saved_data:
            if set(data).issubset(set(args)):
                value = data[0]
                break
        return value



    def update_database(self, pages: int) -> None:
        hh_reader = HhReaderVacancies(pages)
        vacancies: list[Vacancy] = hh_reader.get_vacancies()
        with psycopg2.connect(host=self.host, database=self.database,
                              user=self.user, password=self.password) as conn:
            with conn.cursor() as cur:
                saved_employers = self.get_data_from_table(cur, 'employers')
                saved_salary = self.get_data_from_table(cur, 'salary')
                for vacancy in vacancies:
                    hh_id_vacancy = vacancy.id
                    name_vacancy = vacancy.name
                    avg_salary = vacancy.salary
                    salary_range = vacancy.salary_range
                    name_employer = vacancy.employer
                    hh_id_employer = vacancy.employer_id
                    description = vacancy.description
                    requirement = vacancy.requirement
                    url = vacancy.url
                    id_salary = self.get_arg_from_saved_data([avg_salary, salary_range], saved_data=saved_salary)
                    if not id_salary:
                        cur.execute('''
                            INSERT INTO salary (avg_salary, range_salary)
                            VALUES (%s, %s)
                            RETURNING id_salary
                        ''', (avg_salary, salary_range))
                        id_salary = cur.fetchone()[0]
                        conn.commit()
                    id_employer = self.get_from_saved_data([hh_id_employer, name_employer], saved_data=saved_employers)
                    if not id_employer:
                        cur.execute('''
                            INSERT INTO employers (hh_id_employer, name_employer)
                            VALUES (%s, %s)
                            RETURNING id_employer
                        ''', (hh_id_employer, name_employer))
                        id_employer = cur.fetchone()[0]
                        saved_employers.append((id_employer, hh_id_employer, name_employer))
                        conn.commit()
                    cur.execute('''
                        INSERT INTO vacancies (hh_id_vacancy, name_vacancy, id_salary, 
                        id_employer, description, requirement, url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (hh_id_vacancy, name_vacancy, id_salary, id_employer, description, requirement, url))
                    conn.commit()


with psycopg2.connect(host='localhost', database='home_work_18_1', user='andrdd17', password='u|D".s&qcX') as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM employees")
        rows = cur.fetchall()
        print(rows[0])
        print(type(rows[0]))
