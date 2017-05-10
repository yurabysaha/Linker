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


def db_decorator(func):
    def a_wrapper_accepting_arbitrary_arguments(self, *args, **kwargs):
        db_type = 1
        value = None
        if db_type == 1 or db_type == 3:
            self.con = db.connect(database="../db")
            self.cur = self.con.cursor()
            value = func(self, *args, **kwargs)
        if db_type == 2 or db_type == 3:
            pass
            # self.con = db.connect(database="../db")
            # self.cur = self.con.cursor()
            # remote = func(self, *args, **kwargs)
            # if value is None:
            #     value = remote
        return value
    return a_wrapper_accepting_arbitrary_arguments


class User:
    def __init__(self):
        config = RawConfigParser()
        config.read('../config.ini')
        self.bot_name = config.get('main', 'email')

    @db_decorator
    def create(self, name):
        self.cur.execute("insert into users (bot_name, name) values (?)", (self.bot_name, name,))
        self.con.commit()
        self.con.close()

    @db_decorator
    def accept(self, name):
        # :return
        # 1 - Статус змінено на True
        # 2 - Такого користувача не знайдено в базі
        # 3 - У користувача вже є статус True
        user = self.cur.execute("SELECT * FROM users WHERE name=? AND bot_name=?;", (name, self.bot_name,)).fetchone()
        if user and not user[2]:
            query = "UPDATE users set accept_connect=1, accept_date=? WHERE name=? AND bot_name=?"
            self.cur.execute(query, (date.today(), name, self.bot_name,))
            self.con.commit()
            self.con.close()
            return 1
        else:
            if not user:
                return 2
            return 3

    @db_decorator
    def send_message(self, name):
        query = "UPDATE users set send_message=1, send_date=? where name=? AND bot_name=?"
        self.cur.execute(query, (date.today(), name, self.bot_name,))
        self.con.commit()
        self.con.close()

    @db_decorator
    def get_day_counter(self):
        users = self.cur.execute("SELECT id FROM users WHERE created_at >=? AND bot_name=?;", (date.today(), self.bot_name,)).fetchall()
        self.con.close()
        return len(users)

    @db_decorator
    def get_today_connection_results(self):
        users = self.cur.execute("SELECT name, accept_connect, send_message, second_message, finished FROM users "
                            "WHERE updated_at >=? AND bot_name=?;", (date.today(), self.bot_name,)).fetchall()
        self.con.close()
        return date.today(), users

    @db_decorator
    def get_all_connection_results(self):
        users = self.cur.execute(
            "SELECT strftime('%Y-%m-%d',created_at), name, accept_connect, send_message, second_message, "
            "finished FROM users WHERE bot_name=?"
            "ORDER BY strftime('%Y-%m-%d', created_at) desc;", (self.bot_name,)).fetchall()
        self.con.close()
        return users

    @db_decorator
    def candidate_for_message(self):
        users = self.cur.execute("SELECT name FROM users WHERE accept_connect=? AND send_message=? AND bot_name=?;",
                            (True, False, self.bot_name,)).fetchall()
        self.con.close()
        return users

    @db_decorator
    def candidate_for_review(self):
        users = self.cur.execute("SELECT name FROM users WHERE accept_connect=? AND send_message=?  AND bot_name=?;",
                            (False, False, self.bot_name,)).fetchall()
        self.con.close()
        return users

    @db_decorator
    def count_connections(self):
        all_count = self.cur.execute("SELECT COUNT(*) FROM users WHERE bot_name=?;", (self.bot_name,)).fetchone()
        today_count = self.cur.execute("SELECT COUNT(*) FROM users WHERE created_at >=DATE('now') AND bot_name=?;", (self.bot_name,)).fetchone()
        self.con.close()
        return today_count, all_count

    @db_decorator
    def count_accepted(self):
        all_count = self.cur.execute("SELECT COUNT(*) FROM users WHERE accept_connect=1 AND bot_name=?;", (self.bot_name,)).fetchone()
        today_count = self.cur.execute("SELECT COUNT(*) FROM users WHERE accept_connect=1 AND accept_date >=DATE('now') AND bot_name=?;",(self.bot_name,)).fetchone()
        self.con.close()
        return today_count, all_count

    @db_decorator
    def candidate_for_forward(self):
        cand = self.cur.execute("""SELECT name FROM users WHERE send_message=1 AND second_message=0 AND finished=0 AND send_date < DATE('now', '-4 days') AND bot_name=?;""", (self.bot_name,)).fetchall()
       # cand = cur.execute("""SELECT ;""").fetchall()
        self.con.close()
        return cand

    @db_decorator
    def finish(self, name):
        query = "UPDATE users SET finished=1 WHERE name=? AND bot_name=?;"
        self.cur.execute(query, (name, self.bot_name,))
        self.con.commit()
        self.con.close()

    @db_decorator
    def send_second_message(self, name):
        query = "UPDATE users SET finished=1, second_message=1, second_message_date=? WHERE name=? AND bot_name=?;"
        self.cur.execute(query, (date.today(), name, self.bot_name,))
        self.con.commit()
        self.con.close()
