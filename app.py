import streamlit as st
import sqlite3

DB_NAME = "backend.db"  # path to your DB

def create_user(name, email, age, income, state):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, age, income, state)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, age, income, state))
        conn.commit()
        st.success("✅ User registered successfully!")
    except sqlite3.IntegrityError:
        st.error("❌ Email already exists!")
    conn.close()

# Streamlit UI
st.title("AI Notifier MVP")
st.subheader("🚀 Government Policy Notifier")

menu = ["Home", "Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.write("Welcome to AI Notifier MVP!")
    st.write("Get notified about schemes you are eligible for.")

elif choice == "Register":
    st.write("📝 User Registration Form")
    
    # Registration form
    with st.form(key="registration_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        age = st.number_input("Age", min_value=1, max_value=120)
        income = st.number_input("Annual Income (₹)", min_value=0)
        state = st.text_input("State")
        
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if name and email and age and state:
                create_user(name, email, age, income, state)
            else:
                st.error("❌ Please fill all required fields")

elif choice == "Login":
    st.write("🔑 Login Page (coming soon...)")