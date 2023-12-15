# from config import conn, cursor
# from camp import Camp
# from plan import Plan
#
#
# def get_by_planID(planID):
#     query = []
#     params = []
#     camps = Camp.get_camp(planID=planID)
#     campIDs = [camps[i][0] for i in range(len(camps))]
#     print(campIDs)
#     for campID in campIDs:
#         query.append("campID = ?")
#         params.append(campID)
#     cursor.execute(f"""SELECT * FROM volunteers WHERE {' OR '.join(query)}""", params)
#     return cursor.fetchall()
#
# print(get_by_planID(1))
