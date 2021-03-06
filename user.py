#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
from ConfigParser import RawConfigParser
from datetime import date
from time import strftime

import psycopg2
import psycopg2.extras

today = date(2013, 11, 1)

# 1q2w!@QW
# alexandervojak@gmail.com

DB_TABLE = 'tb_eq_users'
# DB_TABLE = 'users'
class User:
    def __init__(self):
        config = RawConfigParser()
        config.read('../config.ini')
        self.bot_name = (config.get('main', 'email')).lower()
        self.db_type = config.getint('main', 'db_type')
        conn_string = "host='5.9.51.242' port='5432' dbname='db_botnet' user='postgres' password='pomason3'"
        self.con = psycopg2.connect(conn_string)
        self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def create(self, name, link):
        # return 0 - if user already in database (added)
        # return 1 - if we add new user success
        # self.cur.execute("insert into users (bot_name, name, link) values (?, ?, ?);", (self.bot_name, name, link,))
        self.cur.execute("SELECT * FROM "+DB_TABLE+" WHERE bot_name=%s AND name=%s AND link=%s;", (self.bot_name, name, link,))
        data = self.cur.fetchall()
        if data:
            resp = 0
        else:
            self.cur.execute("insert into "+DB_TABLE+" (bot_name, name, link) values (%s, %s, %s);", (self.bot_name, name, link,))
            self.con.commit()
            resp = 1
        self.con.close()
        return resp

    def accept(self, name):
        # :return
        # 1 - Статус змінено на True
        # 2 - Такого користувача не знайдено в базі
        # 3 - У користувача вже є статус True
        self.cur.execute("SELECT * FROM "+DB_TABLE+" WHERE name=%s AND bot_name=%s;", (name, self.bot_name,))
        user = self.cur.fetchone()
        if user and not user[4]:
            query = "UPDATE "+DB_TABLE+" set accept_connect= TRUE, accept_date=%s WHERE name=%s AND bot_name=%s"
            self.cur.execute(query, (date.today(), name, self.bot_name,))
            self.con.commit()
            self.con.close()
            return 1
        else:
            if not user:
                return 2
            return 3

    def send_message(self, name):
        self.cur.execute("UPDATE "+DB_TABLE+" set send_message=TRUE, send_date=%s where name=%s AND bot_name=%s", (date.today(), name, self.bot_name,))
        self.con.commit()
        self.con.close()

    def get_day_counter(self):
        self.cur.execute("SELECT id FROM "+DB_TABLE+" WHERE created_at >=%s AND bot_name=%s;", (date.today(), self.bot_name,))
        users = self.cur.fetchall()
        self.con.close()
        return len(users)

    def get_today_connection_results(self):
         self.cur.execute("SELECT name, accept_connect, send_message, second_message, finished FROM "+DB_TABLE+" "
                            "WHERE updated_at >=%s AND bot_name=%s;", (date.today(), self.bot_name,))
         users = self.cur.fetchall()
         self.con.close()
         return date.today(), users

    def get_all_connection_results(self):
        self.cur.execute(
            "SELECT to_char(created_at, 'YYYY-MM-DD'), name, accept_connect, send_message, second_message, finished FROM "+DB_TABLE+" WHERE bot_name=%s ORDER BY created_at desc;", (self.bot_name,))
        users = self.cur.fetchall()
        self.con.close()
        return users

    def candidate_for_message(self):
        self.cur.execute("SELECT name FROM "+DB_TABLE+" WHERE accept_connect=%s AND send_message=%s AND bot_name=%s AND finished=%s;",
                            (True, False, self.bot_name, False,))
        users = self.cur.fetchall()
        self.con.close()
        return users

    def candidate_for_review(self):
        self.cur.execute("SELECT name FROM "+DB_TABLE+" WHERE accept_connect=%s AND send_message=%s  AND bot_name=%s AND finished=%s;",
                            (False, False, self.bot_name, False,))
        users =self.cur.fetchall()
        self.con.close()
        return users

    def count_connections(self):
        self.cur.execute("SELECT COUNT(*) FROM "+DB_TABLE+" WHERE bot_name = %s;", (self.bot_name,))
        all_count = self.cur.fetchone()

        self.cur.execute("SELECT COUNT(*) FROM "+DB_TABLE+" WHERE created_at >=DATE('now') AND bot_name=%s;", (self.bot_name,))
        today_count = self.cur.fetchone()
        self.con.close()
        return today_count, all_count

    def count_accepted(self):
        self.cur.execute("SELECT COUNT(*) FROM "+DB_TABLE+" WHERE accept_connect= TRUE AND bot_name=%s;", (self.bot_name,))
        all_count = self.cur.fetchone()
        self.cur.execute("SELECT COUNT(*) FROM "+DB_TABLE+" WHERE accept_connect= TRUE AND accept_date >=DATE('now') AND bot_name=%s;",(self.bot_name,))
        today_count = self.cur.fetchone()
        self.con.close()
        return today_count, all_count

    def candidate_for_forward(self):
        self.cur.execute("SELECT name FROM "+DB_TABLE+" WHERE send_message=TRUE AND second_message= FALSE AND finished= FALSE AND send_date < current_date - interval '5' day AND bot_name=%s;", (self.bot_name,))
        cand = self.cur.fetchall()
        self.con.close()
        return cand

    def finish(self, name):
        query = "UPDATE "+DB_TABLE+" SET finished= TRUE WHERE name=%s AND bot_name=%s;"
        self.cur.execute(query, (name, self.bot_name,))
        self.con.commit()
        self.con.close()

    def send_second_message(self, name):
        query = "UPDATE "+DB_TABLE+" SET finished= TRUE, second_message= TRUE, second_message_date=%s WHERE name=%s AND bot_name=%s;"
        self.cur.execute(query, (date.today(), name, self.bot_name,))
        self.con.commit()
        self.con.close()
