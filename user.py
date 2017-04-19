#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
from datetime import date
from time import strftime

today = date(2013, 11, 1)
c = db.connect(database="../linker")
cu = c.cursor()
try:
    cu.executescript("""
          CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            accept_connect BOOLEAN DEFAULT 0,
            accept_date DATE,
            send_message BOOLEAN DEFAULT 0,
            send_date  DATE
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
    con = db.connect(database="../linker")
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

    con = db.connect(database="../linker")
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
    con = db.connect(database="../linker")
    cur = con.cursor()
    query = "UPDATE users set send_message=1, send_date=? where name=?"
    cur.execute(query, (date.today(), name,))
    con.commit()
    con.close()


def get_day_counter():
    con = db.connect(database="../linker")
    cur = con.cursor()
    print date.today()
    users = cur.execute("SELECT id FROM users WHERE created_at >=?;", (date.today(),)).fetchall()
    con.close()
    return len(users)


def get_today_connection_results():
    con = db.connect(database="../linker")
    cur = con.cursor()
    users = cur.execute("SELECT name FROM users WHERE created_at >=?;", (date.today(),)).fetchall()
    con.close()
    return date.today(), users


def get_all_connection_results():
    con = db.connect(database="../linker")
    cur = con.cursor()
    users = cur.execute("SELECT name,strftime('%Y-%m-%d',created_at) FROM users "
                        "ORDER BY strftime('%Y-%m-%d', created_at) desc;" ) .fetchall()
    con.close()
    return users