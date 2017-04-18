#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db

from datetime import date, datetime

today = date(2013, 11, 1)
c = db.connect(database="linker")
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
    con = db.connect(database="linker")
    cur = con.cursor()
    cur.execute("insert into users (name) values (?)",
                (name,))
    con.commit()
    con.close()


def accept(name):
    con = db.connect(database="linker")
    cur = con.cursor()
    query = "UPDATE users set accept_connect=1, accept_date=? where name=?"
    cur.execute(query, (date.today(), name,))
    con.commit()
    con.close()


def send_message(name):
    con = db.connect(database="linker")
    cur = con.cursor()
    query = "UPDATE users set send_message=1, send_date=? where name=?"
    cur.execute(query, (date.today(), name,))
    con.commit()
    con.close()
