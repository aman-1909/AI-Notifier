import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "backend.db"

# -----------------------------
# Database helper functions
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  interest TEXT)''')
    # Policies table
    c.execute('''CREATE TABLE IF NOT EXISTS policies
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  sector TEXT,
                  description TEXT)''')
    conn.commit()
    conn.close()

init_db()  # initialize DB

# -----------------------------
# UI
# -----------------------------
st.title("🤖 AI Policy Notifier - Day 3")

menu = st.sidebar.radio("Navigate", ["Register", "Admin Panel", "View Policies", "My Notifications", "Debug DB"])

# -----------------------------
# Register
# -----------------------------
if menu == "Register":
    st.subheader("Register")
    with st.form("register"):
        name = st.text_input("Your Name")
        interest = st.selectbox("Your Interest", ["startup", "farmer", "tech", "msme"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO users (name, interest) VALUES (?, ?)", (name, interest))
            conn.commit()
            conn.close()
            st.success(f"✅ Welcome {name}! Registered for {interest} policies.")

# -----------------------------
# Admin Panel
# -----------------------------
elif menu == "Admin Panel":
    st.subheader("Add a New Policy")
    with st.form("add_policy"):
        title = st.text_input("Policy Title")
        sector = st.selectbox("Sector", ["startup", "farmer", "tech", "msme"])
        description = st.text_area("Description")
        submit_policy = st.form_submit_button("Add Policy")
        if submit_policy:
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO policies (title, sector, description) VALUES (?, ?, ?)", (title, sector, description))
            conn.commit()
            conn.close()
            st.success(f"✅ Policy '{title}' added successfully!")

# -----------------------------
# View Policies
# -----------------------------
elif menu == "View Policies":
    st.subheader("All Policies")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM policies", conn)
    conn.close()
    st.dataframe(df)

# -----------------------------
# My Notifications (Eligible Policies)
# -----------------------------
elif menu == "My Notifications":
    st.subheader("Your Eligible Policies")
    conn = get_connection()
    users_df = pd.read_sql("SELECT * FROM users", conn)
    policies_df = pd.read_sql("SELECT * FROM policies", conn)
    conn.close()

    if users_df.empty:
        st.warning("⚠️ Please register first.")
    else:
        # For simplicity, show last registered user
        user = users_df.iloc[-1]
        st.info(f"Showing notifications for {user['name']} (interest: {user['interest']})")

        eligible = policies_df[policies_df["sector"] == user["interest"]]
        if eligible.empty:
            st.info("No matching policies at the moment.")
        else:
            st.success(f"✅ Found {len(eligible)} eligible policies:")
            st.dataframe(eligible)

# -----------------------------
# Debug DB
# -----------------------------
elif menu == "Debug DB":
    st.subheader("📂 Raw Database Content")
    conn = get_connection()
    c = conn.cursor()

    # List tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    st.write("Tables in DB:", tables)

    # Show contents of each table
    for (tname,) in tables:
        st.write(f"### Table: {tname}")
        df_debug = pd.read_sql(f"SELECT * FROM {tname}", conn)
        st.dataframe(df_debug)
    conn.close()