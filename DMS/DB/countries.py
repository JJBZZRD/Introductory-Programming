from .config import conn, cursor


def get_all_countries():
    cursor.execute("SELECT * FROM countries")
    list_of_tuples = cursor.fetchall()
    list_of_countries = [x[0] for x in list_of_tuples]
    return list_of_countries


# countries_test = get_all_countries()
# print(countries_test)
