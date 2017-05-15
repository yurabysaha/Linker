#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
from ConfigParser import RawConfigParser
from datetime import date
from time import strftime

import psycopg2
import psycopg2.extras

today = date(2013, 11, 1)
# c = db.connect(database="../db")
# cu = c.cursor()
# try:
#     cu.executescript("""
#           CREATE TABLE users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             bot_name VARCHAR,
#             name VARCHAR,
#             link VARCHAR,
#             accept_connect BOOLEAN DEFAULT 0,
#             accept_date DATE,
#             send_message BOOLEAN DEFAULT 0,
#             send_date  DATE,
#             second_message BOOLEAN DEFAULT 0,
#             second_message_date DATE,
#             finished BOOLEAN DEFAULT 0
#             ,created_at datetime  NOT NULL  DEFAULT current_timestamp
#             ,updated_at datetime  NOT NULL  DEFAULT current_timestamp
#             );
#
#         -- trigger (updated_at)
#         CREATE TRIGGER tg_users_updated_at
#         AFTER UPDATE
#         ON users FOR EACH ROW
#         BEGIN
#           UPDATE users SET updated_at = current_timestamp
#             WHERE id = old.id;
#         END;""")
#
# except db.DatabaseError, x:
#     print "DB Error: ", x
# c.commit()
# c.close()


# def db_decorator(func):
#     def a_wrapper_accepting_arbitrary_arguments(self, *args, **kwargs):
#         value = None
#         if self.db_type == 1 or self.db_type == 3:
#             self.con = db.connect(database="../db")
#             self.cur = self.con.cursor()
#             value = func(self, *args, **kwargs)
#         if self.db_type == 2 or self.db_type == 3:
#             conn_string = "host='5.9.51.242' port='5432' dbname='db_botnet' user='postgres' password='pomason3'"
#             self.con = psycopg2.connect(conn_string)
#             self.cur = self.con.cursor(cursor_factory = psycopg2.extras.DictCursor)
#             remote = func(self, *args, **kwargs)
#             value = remote
#         return value
#     return a_wrapper_accepting_arbitrary_arguments


class User:
    def __init__(self):
        config = RawConfigParser()
        config.read('../config.ini')
        self.bot_name = config.get('main', 'email')
        self.db_type = config.getint('main', 'db_type')
        conn_string = "host='5.9.51.242' port='5432' dbname='db_botnet' user='postgres' password='pomason3'"
        self.con = psycopg2.connect(conn_string)
        self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

   # @db_decorator
    def create(self, name, link):
        # self.cur.execute("insert into users (bot_name, name, link) values (?, ?, ?);", (self.bot_name, name, link,))
        self.cur.execute("insert into users (bot_name, name, link) values (%s, %s, %s);", (self.bot_name, name, link,))
        self.con.commit()
        self.con.close()

   # @db_decorator
    def accept(self, name):
        # :return
        # 1 - Статус змінено на True
        # 2 - Такого користувача не знайдено в базі
        # 3 - У користувача вже є статус True
        self.cur.execute("SELECT * FROM users WHERE name=%s AND bot_name=%s;", (name, self.bot_name,))
        user = self.cur.fetchone()
        if user and not user[4]:
            query = "UPDATE users set accept_connect= TRUE, accept_date=%s WHERE name=%s AND bot_name=%s"
            self.cur.execute(query, (date.today(), name, self.bot_name,))
            self.con.commit()
            self.con.close()
            return 1
        else:
            if not user:
                return 2
            return 3

   # @db_decorator
    def send_message(self, name):
        self.cur.execute("UPDATE users set send_message=TRUE, send_date=%s where name=%s AND bot_name=%s", (date.today(), name, self.bot_name,))
        self.con.commit()
        self.con.close()

   # @db_decorator
    def get_day_counter(self):
        self.cur.execute("SELECT id FROM users WHERE created_at >=%s AND bot_name=%s;", (date.today(), self.bot_name,))
        users = self.cur.fetchall()
        self.con.close()
        return len(users)

    #@db_decorator
    def get_today_connection_results(self):
         self.cur.execute("SELECT name, accept_connect, send_message, second_message, finished FROM users "
                            "WHERE updated_at >=%s AND bot_name=%s;", (date.today(), self.bot_name,))
         users = self.cur.fetchall()
         self.con.close()
         return date.today(), users

   # @db_decorator
    def get_all_connection_results(self):
        self.cur.execute(
            "SELECT to_char(created_at, 'YYYY-MM-DD'), name, accept_connect, send_message, second_message, finished FROM users WHERE bot_name=%s ORDER BY created_at desc;", (self.bot_name,))
        users = self.cur.fetchall()
        self.con.close()
        return users

   # @db_decorator
    def candidate_for_message(self):
        self.cur.execute("SELECT name FROM users WHERE accept_connect=%s AND send_message=%s AND bot_name=%s AND finished=%s;",
                            (True, False, self.bot_name, False,))
        users = self.cur.fetchall()
        self.con.close()
        return users

   # @db_decorator
    def candidate_for_review(self):
        self.cur.execute("SELECT name FROM users WHERE accept_connect=%s AND send_message=%s  AND bot_name=%s AND finished=%s;",
                            (False, False, self.bot_name, False,))
        users =self.cur.fetchall()
        self.con.close()
        return users

   # @db_decorator
    def count_connections(self):
        self.cur.execute("SELECT COUNT(*) FROM users WHERE bot_name = %s;", (self.bot_name,))
        all_count = self.cur.fetchone()

        self.cur.execute("SELECT COUNT(*) FROM users WHERE created_at >=DATE('now') AND bot_name=%s;", (self.bot_name,))
        today_count = self.cur.fetchone()
        self.con.close()
        return today_count, all_count

   # @db_decorator
    def count_accepted(self):
        self.cur.execute("SELECT COUNT(*) FROM users WHERE accept_connect= TRUE AND bot_name=%s;", (self.bot_name,))
        all_count = self.cur.fetchone()
        self.cur.execute("SELECT COUNT(*) FROM users WHERE accept_connect= TRUE AND accept_date >=DATE('now') AND bot_name=%s;",(self.bot_name,))
        today_count = self.cur.fetchone()
        self.con.close()
        return today_count, all_count

   # @db_decorator
    def candidate_for_forward(self):
        self.cur.execute("""SELECT name FROM users WHERE send_message=TRUE AND second_message= FALSE AND finished= FALSE AND send_date < current_date - interval '5' day AND bot_name=%s;""", (self.bot_name,))
        cand = self.cur.fetchall()
        self.con.close()
        return cand

   # @db_decorator
    def finish(self, name):
        query = "UPDATE users SET finished= TRUE WHERE name=%s AND bot_name=%s;"
        self.cur.execute(query, (name, self.bot_name,))
        self.con.commit()
        self.con.close()

   # @db_decorator
    def send_second_message(self, name):
        query = "UPDATE users SET finished= TRUE, second_message= TRUE, second_message_date=%s WHERE name=%s AND bot_name=%s;"
        self.cur.execute(query, (date.today(), name, self.bot_name,))
        self.con.commit()
        self.con.close()
