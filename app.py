import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Dummy Policy Database ---
policies = [
    {
        "title": "Farmer Subsidy Scheme",
        "eligibility": {"occupation": "Farmer", "max_income": 200000},
        "benefit": "Direct subsidy for organic fertilizers."
    },
    {
        "title": "Student Scholarship 2025",
        "eligibility": {"occupation": "Student", "max_income": 500000},
        "benefit": "Free scholarships for higher education."
    },
    {
        "title": "Senior Citizen Health Scheme",
        "eligibility": {"min_age": 60},
        "benefit": "Free health checkups and medicines."
    }
]

# --- Email Notification Function ---
def send_email(receiver_email, subject, body):
    sender_email = "yourgmail@gmail.com"
    password = "your-app-password"  # Use App Password if 2FA enabled

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)

# --- Streamlit UI ---
st.set_page_config(page_title="Policy Notifier", layout="wide")

st.title("📢 Government Policy Notifier")
st.write("Find policies you are eligible for & get notified instantly!")

# --- User Input ---
with st.form("user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    occupation = st.selectbox("Occupation", ["Farmer", "Student", "Worker", "Other"])
    income = st.number_input("Annual Income (₹)", min_value=0, step=1000)
    submitted = st.form_submit_button("Check Eligibility")

if submitted:
    eligible_policies = []
    for policy in policies:
        rules = policy["eligibility"]
        ok = True

        if "min_age" in rules and age < rules["min_age"]:
            ok = False
        if "max_age" in rules and age > rules["max_age"]:
            ok = False
        if "occupation" in rules and occupation != rules["occupation"]:
            ok = False
        if "max_income" in rules and income > rules["max_income"]:
            ok = False

        if ok:
            eligible_policies.append(policy)

    if eligible_policies:
        st.success(f"✅ {name}, you are eligible for the following policies:")
        message = ""
        for p in eligible_policies:
            st.write(f"**{p['title']}** – {p['benefit']}")
            message += f"{p['title']}: {p['benefit']}\n"

        if email:
            result = send_email(email, "Policy Eligibility Notification", message)
            if result == True:
                st.info("📧 Notification email sent successfully!")
            else:
                st.error(f"Email failed: {result}")

    else:
        st.error("❌ Sorry, no policies match your profile right now.")