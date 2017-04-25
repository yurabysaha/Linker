#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
from datetime import date
from time import strftime

today = date(2013, 11, 1)
c = db.connect(database="../db")
cu = c.cursor()
try:
    cu.executescript("""
          CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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


def create(name):
    con = db.connect(database="../db")
    cur = con.cursor()
    cur.execute("insert into users (name) values (?)",
                (name,))
    con.commit()
    con.close()


def accept(name):

    # :return
    # 1 - Статус змінено на True
    # 2 - Такого користувача не знайдено в базі
    # 3 - У користувача вже є статус True

    con = db.connect(database="../db")
    cur = con.cursor()
    user = cur.execute("SELECT * FROM users WHERE name=?;", (name,)).fetchone()
    if user and not user[2]:
        query = "UPDATE users set accept_connect=1, accept_date=? where name=?"
        cur.execute(query, (date.today(), name,))
        con.commit()
        con.close()
        return 1
    else:
        if not user:
            return 2
        return 3


def send_message(name):
    con = db.connect(database="../db")
    cur = con.cursor()
    query = "UPDATE users set send_message=1, send_date=? where name=?"
    cur.execute(query, (date.today(), name,))
    con.commit()
    con.close()


def get_day_counter():
    con = db.connect(database="../db")
    cur = con.cursor()
    print date.today()
    users = cur.execute("SELECT id FROM users WHERE created_at >=?;", (date.today(),)).fetchall()
    con.close()
    return len(users)


def get_today_connection_results():
    con = db.connect(database="../db")
    cur = con.cursor()
    users = cur.execute("SELECT name, accept_connect, send_message FROM users WHERE updated_at >=?;", (date.today(),)).fetchall()
    con.close()
    return date.today(), users


def get_all_connection_results():
    con = db.connect(database="../db")
    cur = con.cursor()
    users = cur.execute("SELECT strftime('%Y-%m-%d',created_at), name, accept_connect, send_message FROM users "
                        "ORDER BY strftime('%Y-%m-%d', created_at) desc;").fetchall()
    con.close()
    return users


def candidate_for_message():
    con = db.connect(database="../db")
    cur = con.cursor()
    users = cur.execute("SELECT name FROM users WHERE accept_connect=? AND send_message=?;",
                        (True, False,)).fetchall()
    con.close()
    return users


def candidate_for_review():
    con = db.connect(database="../db")
    cur = con.cursor()
    users = cur.execute("SELECT name FROM users WHERE accept_connect=? AND send_message=?;",
                        (False, False,)).fetchall()
    con.close()
    return users


def count_connections():
    con = db.connect(database="../db")
    cur = con.cursor()
    all_count = cur.execute("SELECT COUNT(*) FROM users;").fetchone()
    today_count = cur.execute("SELECT COUNT(*) FROM users WHERE created_at >=DATE('now');").fetchone()
    con.close()
    return today_count, all_count


def count_accepted():
    con = db.connect(database="../db")
    cur = con.cursor()
    all_count = cur.execute("SELECT COUNT(*) FROM users WHERE accept_connect=1;").fetchone()
    today_count = cur.execute("SELECT COUNT(*) FROM users WHERE accept_connect=1 AND created_at >=DATE('now');").fetchone()
    con.close()
    return today_count, all_count


def candidate_for_forward():
    con = db.connect(database="../db")
    cur = con.cursor()
    cand = cur.execute("""SELECT name FROM users WHERE send_message=1 AND second_message=0 AND finished=0 AND send_date < DATE('now', '-7 days');""").fetchall()
   # cand = cur.execute("""SELECT ;""").fetchall()

    con.close()
    return cand


def finish(name):
    con = db.connect(database="../db")
    cur = con.cursor()
    query = "UPDATE users SET finished=1 WHERE name=?;"
    cur.execute(query, (name,))
    con.commit()
    con.close()


def send_second_message(name):
    con = db.connect(database="../db")
    cur = con.cursor()
    query = "UPDATE users SET finished=1, second_message=1, second_message_date=? WHERE name=?;"
    cur.execute(query, (date.today(), name,))
    con.commit()
    con.close()
