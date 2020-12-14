# import mysql.connector
# from game_management import common
# from utilities import security
# from configparser import ConfigParser
#
# turns = []  # arrays of instances of the PlayerMove class
#
#
# class PlayerMove:
#     """
#     Represents a move performed by a Player
#     """
#
#     def __init__(self, sign, turn_n: int, move: int, result=0.0):
#         self.__sign = sign  # sign of the Player which made the move
#         self.__turn_n = turn_n  # turn number
#         self.__move = move  # the move performed by the Player
#         self.__result = result  # the result of the move (1 = win, 0 = loss)
#
#     @property
#     def sign(self):
#         return self.__sign
#
#     @property
#     def turn_n(self):
#         return self.__turn_n
#
#     @property
#     def move(self):
#         return self.__move
#
#     @property
#     def result(self):
#         return self.__result
#
#     @result.setter
#     def result(self, result):
#         self.__result = result
#
#     def __str__(self):
#         return f"turn_n: {self.__turn_n}\tmove: {self.__move}\tresult: {self.__result}"
#
#
# def ai_move():
#     """
#
#     :return:
#     """
#     limit = 0.5
#     cursor, database = db_connection()
#     query_string = "SELECT play FROM turn_{} WHERE probability > {}".format(len(turns) + 1, limit)
#
#     for index, turn in enumerate(turns):
#         query_string += " and turn_{} = {}".format(index + 1, turn.move)
#
#     cursor.execute(query_string)
#     pot_ai_moves = cursor.fetchall()
#
#     cursor.close()
#     database.close()
#
#     if len(pot_ai_moves):
#         definite_play = common.random_number(0, len(pot_ai_moves))
#
#         if (len(turns) + 1) % 2:
#             sign = "O"
#         else:
#             sign = "X"
#
#         turns.append(PlayerMove(sign, len(turns) + 1, pot_ai_moves[definite_play][0]))
#         print(turns[-1])
#         return turns[-1].move
#     else:
#         return "NOT_FOUND"
#
#
# def update_ai_database():
#     """
#
#     :return:
#     """
#     # Connection to the database
#     cursor, database = db_connection()
#
#     for turn in turns:
#         # verify if the moves are already present in the database
#         already_in_database = False
#         condition_query = "SELECT * FROM turn_{}".format(turn.turn_n)
#         where_condition = " WHERE play = {}".format(turn.move)
#
#         for i in range(turn.turn_n - 1):
#             where_condition += " and turn_{0}.turn_{1} = {2}".format(turn.turn_n, i + 1, turns[i].move)
#
#         condition_query += where_condition
#         cursor.execute(condition_query)
#         for (i) in cursor:
#             already_in_database = i
#
#         # Update of the database
#         if already_in_database:
#             # If they are already present in the database, we just update them
#             query_string = "UPDATE turn_{} SET probability = (n_references * probability + {}) / (n_references + 1), n_references = n_references + 1".format(
#                 turn.turn_n, turn.result)
#             query_string += where_condition
#             cursor.execute(query_string)
#         else:
#             # Else, we insert the new values in the database
#             values = [turn.move, turn.result]
#             query_string = "INSERT INTO turn_{}(play, probability, n_references".format(turn.turn_n)
#             value_string = "VALUES (%s, %s, 1"
#
#             for i in range(turn.turn_n - 1):
#                 query_string += ", turn_{}".format(i + 1)
#                 value_string += ", %s"
#                 values.append(turns[i].move)
#
#             query_string += ")"
#             value_string += ")"
#             values = tuple(values)
#
#             entire_query = query_string + value_string
#             cursor.execute(entire_query, values)
#
#         database.commit()
#
#     cursor.close()
#     database.close()
#
#
# def db_connection():
#     """
#
#     :return:
#     """
#     security.decrypt_file("program_files/config.ini")
#     configuration_content = ConfigParser()
#     configuration_content.read("program_files\\config.ini")
#
#     database = mysql.connector.connect(
#         host="localhost",
#         user=configuration_content["database_login"]["username"],
#         password=configuration_content["database_login"]["password"],
#         database="tictactoe"
#     )
#
#     security.encrypt_file("program_files/config.ini")
#     return database.cursor(buffered=True), database
#
#
# if __name__ == "__main__":
#     pass
