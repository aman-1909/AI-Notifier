import streamlit as st
from database import SCHEMES
from brain import is_eligible

st.set_page_config(page_title="Bihar Student Scheme Finder")

st.title("🎓 Bihar Student Scheme Finder")
st.write("Find government schemes you are eligible for.")

income = st.number_input("Annual Family Income (₹)", min_value=0, step=1000)
category = st.selectbox("Category", ["SC", "ST", "OBC", "GENERAL"])
gender = st.selectbox("Gender", ["Male", "Female"])
student = st.checkbox("I am currently a student")

user = {
    "income": income,
    "category": category,
    "gender": gender,
    "student": student
}

st.subheader("Eligible Schemes")

matched = False
for scheme in SCHEMES:
    if is_eligible(user, scheme):
        st.success(scheme["name"])
        st.write(scheme["description"])
        st.markdown(f"[More Info]({scheme['link']})")
        matched = True

if not matched:
    st.warning("No schemes matched your profile.")