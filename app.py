import streamlit as st
import pandas as pd
import sqlite3
import os

DB_PATH = "backend.db"

# -----------------------------
# Ensure clean DB connection
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  interest TEXT)''')
    conn.commit()
    conn.close()

init_db()  # initialize once

# -----------------------------
# Sample Policies
# -----------------------------
policies = [
    {"title": "Startup India Seed Fund", "sector": "startup"},
    {"title": "PM Kisan Samman Nidhi", "sector": "farmer"},
    {"title": "Digital India Grant", "sector": "tech"},
]
df = pd.DataFrame(policies)

# -----------------------------
# UI
# -----------------------------
st.title("AI Policy Notifier - Day 2 (with DB)")

menu = st.sidebar.radio("Navigate", ["Register", "View Policies", "Registered Users", "Debug DB"])

# -----------------------------
# Register
# -----------------------------
if menu == "Register":
    st.subheader("Register")
    with st.form("register"):
        name = st.text_input("Your Name")
        interest = st.selectbox("Your Interest", ["startup", "farmer", "tech"])
        submitted = st.form_submit_button("Submit")

        if submitted:
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO users (name, interest) VALUES (?, ?)", (name, interest))
            conn.commit()
            conn.close()
            st.success(f"✅ Welcome {name}! Registered for {interest} policies.")

# -----------------------------
# Policies
# -----------------------------
elif menu == "View Policies":
    st.subheader("Available Policies")
    st.dataframe(df)

# -----------------------------
# Registered Users
# -----------------------------
elif menu == "Registered Users":
    st.subheader("Registered Users")
    conn = get_connection()
    users_df = pd.read_sql("SELECT * FROM users", conn)
    conn.close()
    st.dataframe(users_df)

# -----------------------------
# Debug DB (full content)
# -----------------------------
elif menu == "Debug DB":
    st.subheader("📂 Raw Database Content")
    conn = get_connection()
    c = conn.cursor()

    # List tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    st.write("Tables in DB:", tables)

    # For each table, show contents
    for (tname,) in tables:
        st.write(f"### Table: {tname}")
        df_debug = pd.read_sql(f"SELECT * FROM {tname}", conn)
        st.dataframe(df_debug)

    conn.close()