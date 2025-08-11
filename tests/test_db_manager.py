import psycopg2

from src.db_manager import DBManager

def test_db_manager() -> None:
    column_names = ['id_vacancy', 'hh_id_vacancy', 'name_vacancy', 'id_salary', 'id_employeer',
                    'description', 'requirement', 'url']
    db_manager = DBManager('localhost', 'hh_vacancies', 'andrdd17', 'u|D".s&qcX')
    with psycopg2.connect(
            host=db_manager.host,
            database=db_manager.database,
            user=db_manager.user,
            password=db_manager.password) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'vacancies'
                ORDER BY ordinal_position
            """)
            rows = cur.fetchall()
            for i in range(len(rows)):
                assert rows[i][0] == column_names[i]
