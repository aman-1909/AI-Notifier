import streamlit as st

st.title("AI Notifier MVP")
st.subheader("🚀 Government Policy Notifier")

menu = ["Home", "Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.write("Welcome to AI Notifier MVP!")
    st.write("Get notified about schemes you are eligible for.")
elif choice == "Register":
    st.write("📝 User Registration Form (coming soon...)")
elif choice == "Login":
    st.write("🔑 Login Page (coming soon...)")