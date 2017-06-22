#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
from ConfigParser import RawConfigParser
from datetime import date
from time import strftime

today = date(2013, 11, 1)
c = db.connect(database="../db")
cu = c.cursor()
try:
    cu.executescript("""
          CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_name VARCHAR,
            name VARCHAR,
            link VARCHAR,
            accept_connect BOOLEAN DEFAULT 0,
            accept_date DATE,
            send_message BOOLEAN DEFAULT 0,
            send_date  DATE,
            second_message BOOLEAN DEFAULT 0,
            second_message_date DATE,
            finished BOOLEAN DEFAULT 0
            ,created_at datetime  NOT NULL  DEFAULT current_timestamp
            ,updated_at datetime  NOT NULL  DEFAULT current_timestamp
            );

        -- trigger (updated_at)
        CREATE TRIGGER tg_users_updated_at
        AFTER UPDATE
        ON users FOR EACH ROW
        BEGIN
          UPDATE users SET updated_at = current_timestamp
            WHERE id = old.id;
        END;""")

except db.DatabaseError, x:
    print "DB Error: ", x
c.commit()
c.close()

DB_TABLE = 'users'


class User:
    def __init__(self):
        config = RawConfigParser()
        config.read('../config.ini')
        self.bot_name = (config.get('main', 'email')).lower()
        self.con = db.connect(database="../db")
        self.cur = self.con.cursor()

    def create(self, name, link):
        # return 0 - if user already in database (added)
        # return 1 - if we add new user success
        # self.cur.execute("insert into users (bot_name, name, link) values (?, ?, ?);", (self.bot_name, name, link,))
        self.cur.execute("SELECT * FROM "+DB_TABLE+" WHERE bot_name=? AND name=? AND link=?;", (self.bot_name, name, link,))
        data = self.cur.fetchall()
        if data:
            resp = 0
        else:
            self.cur.execute("insert into "+DB_TABLE+" (bot_name, name, link) values (?, ?, ?);", (self.bot_name, name, link,))
            self.con.commit()
            resp = 1
        self.con.close()
        return resp

    def accept(self, name):
        # :return
        # 1 - Статус змінено на True
        # 2 - Такого користувача не знайдено в базі
        # 3 - У користувача вже є статус True
        self.cur.execute("SELECT * FROM "+DB_TABLE+" WHERE name=? AND bot_name=?;", (name, self.bot_name,))
        user = self.cur.fetchone()
        if user and not user[4]:
            query = "UPDATE "+DB_TABLE+" set accept_connect=1, accept_date=? WHERE name=? AND bot_name=?"
            self.cur.execute(query, (date.today(), name, self.bot_name,))
            self.con.commit()
            self.con.close()
            return 1
        else:
            if not user:
                return 2
            return 3

    def send_message(self, name):
        self.cur.execute("UPDATE "+DB_TABLE+" set send_message=1, send_date=? where name=? AND bot_name=?", (date.today(), name, self.bot_name,))
        self.con.commit()
        self.con.close()

    def get_day_counter(self):
        self.cur.execute("SELECT id FROM "+DB_TABLE+" WHERE created_at >=? AND bot_name=?;", (date.today(), self.bot_name,))
        users = self.cur.fetchall()
        self.con.close()
        return len(users)

    def get_today_connection_results(self):
         self.cur.execute("SELECT name, accept_connect, send_message, second_message, finished FROM "+DB_TABLE+" "
                            "WHERE updated_at >=? AND bot_name=?;", (date.today(), self.bot_name,))
         users = self.cur.fetchall()
         self.con.close()
         return date.today(), users

    def get_all_connection_results(self):
        self.cur.execute(
            "SELECT to_char(created_at, 'YYYY-MM-DD'), name, accept_connect, send_message, second_message, finished FROM "+DB_TABLE+" WHERE bot_name=? ORDER BY created_at desc;", (self.bot_name,))
        users = self.cur.fetchall()
        self.con.close()
        return users

    def candidate_for_message(self):
        self.cur.execute("SELECT name FROM "+DB_TABLE+" WHERE accept_connect=? AND send_message=? AND bot_name=? AND finished=?;",
                            (True, False, self.bot_name, False,))
        users = self.cur.fetchall()
        self.con.close()
        return users

    def candidate_for_review(self):
        self.cur.execute("SELECT name FROM "+DB_TABLE+" WHERE accept_connect=? AND send_message=? AND bot_name=? AND finished=?;",
                            (False, False, self.bot_name, False,))
        users = self.cur.fetchall()
        self.con.close()
        return users

    def count_connections(self):
        self.cur.execute("SELECT COUNT(*) FROM "+DB_TABLE+" WHERE bot_name=?;", (self.bot_name,))
        all_count = self.cur.fetchone()

        self.cur.execute("SELECT COUNT(*) FROM "+DB_TABLE+" WHERE created_at >=DATE('now') AND bot_name=?;", (self.bot_name,))
        today_count = self.cur.fetchone()
        self.con.close()
        return today_count, all_count

    def count_accepted(self):
        self.cur.execute("SELECT COUNT(*) FROM "+DB_TABLE+" WHERE accept_connect=1 AND bot_name=?;", (self.bot_name,))
        all_count = self.cur.fetchone()
        self.cur.execute("SELECT COUNT(*) FROM "+DB_TABLE+" WHERE accept_connect=1 AND accept_date >=DATE('now') AND bot_name=?;", (self.bot_name,))
        today_count = self.cur.fetchone()
        self.con.close()
        return today_count, all_count

    def candidate_for_forward(self):
        self.cur.execute("SELECT name FROM "+DB_TABLE+" WHERE send_message=1 AND second_message=0 AND finished=0 AND send_date < current_date - interval '5' day AND bot_name=?;", (self.bot_name,))
        cand = self.cur.fetchall()
        self.con.close()
        return cand

    def finish(self, name):
        query = "UPDATE "+DB_TABLE+" SET finished=1 WHERE name=? AND bot_name=?;"
        self.cur.execute(query, (name, self.bot_name,))
        self.con.commit()
        self.con.close()

    def send_second_message(self, name):
        query = "UPDATE "+DB_TABLE+" SET finished=1, second_message=1, second_message_date=? WHERE name=? AND bot_name=?;"
        self.cur.execute(query, (date.today(), name, self.bot_name,))
        self.con.commit()
        self.con.close()
