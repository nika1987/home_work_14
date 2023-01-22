import sqlite3

from constants import DB_FILE, DB_TABLE


def get_data(query: str):
    '''
    Функция возвращает весь список названиев фильмов
    '''
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            result = []

            for i in cursor.execute(query).fetchall():
                result.append(dict(i))

            return result
    except Exception as e:
        print(f"Ошибка {e}")
        return []


def get_movies(start_year, end_year):
    '''
    Функция возвращает название и год выпуска, отсортированных по дате выпуска
    '''
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            result = []
            query = f"""
            SELECT title, release_year
            FROM {DB_TABLE}
            WHERE release_year between {start_year} AND {end_year}
            LIMIT 100
            """

            for i in conn.execute(query).fetchall():
                result.append(dict(i))

            return result

    except Exception as e:
        print(f"Ошибка {e}")
        return []


def get_movie_rating(rating):
    '''
    Функция возвращает название фильмов по возрасту
    '''
    try:
        trans_rating = {
            'children': ('G', 'G'),
            'family': ('G', 'PG', 'PG-13'),
            'adult': ('R', 'NC-17')
        }
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row

        result = []
        query = f"""
                SELECT title, rating, description
                FROM {DB_TABLE}
                WHERE rating in {trans_rating[rating]}
                """

        for i in conn.execute(query).fetchall():
            result.append(dict(i))

        return result
    except Exception as e:
        print(f"Такого возвраста нет {e}")
        return []


def get_movie_desc(genre):
    '''
    Функция возвращает название фильмов по жанру
    '''

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        result = []
        query = f"""
        SELECT title, listed_in
        FROM {DB_TABLE}
        WHERE listed_in LIKE '%{genre}%'
        order by release_year desc 
        limit 10
        
        """

        for i in conn.execute(query).fetchall():
            result.append(dict(i))
    return result


def get_all_actor(one_actor, two_actor):
    '''
    Функция возвращает список актеров
    '''

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        result = []
        query = f"""
        SELECT "cast"
        FROM {DB_TABLE}
        WHERE "cast" LIKE '%{one_actor}%'
        AND "cast" LIKE '%{two_actor}%'
        """
        conn.execute(query)

        for i in conn.execute(query).fetchall():
            result.append(dict(i))
    return result


def get_play_actor(one_actor, two_actor):
    '''
    Функция возвращает список актеров тех, кто играет с ними в паре больше 2 раз.
    '''

    data = get_all_actor(one_actor, two_actor)
    counter = {}
    result_counter = []
    for actors in data:
        actors['cast'] = actors['cast'].split(", ")
        actors['cast'].remove(one_actor)
        actors['cast'].remove(two_actor)
        for actor in actors['cast']:
            counter.setdefault(actor, 0)
            counter[actor] += 1
    for key, value in counter.items():
        if value > 2:
            result_counter.append(key)

    return result_counter


def get_movie_description(type, release_year, listed_in):
    '''
    Функция возвращает  список названий картин с их описаниями в JSON.
    '''

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        result = []
        query = f"""
                SELECT title, description
                FROM {DB_TABLE}
                WHERE type LIKE '%{type}%'
                and release_year = {release_year}
                and listed_in LIKE '%{listed_in}%'
        
        """
        for i in conn.execute(query).fetchall():
            result.append(dict(i))
    return result

