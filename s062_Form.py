import json
import os
import streamlit as st
import pandas as pd
import plotly.express as px

user_data_file = "users.json"

def load_users():
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            return json.load(file)
    return {}

def save_user(user_data):
    users = load_users()
    users[user_data['email']] = user_data
    with open(user_data_file, 'w') as file:
        json.dump(users, file)

def user_exists(email):
    users = load_users()
    return email in users

def register_user():
    st.title("Welcome to the Sign-Up Page")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    dob = st.date_input("Date of Birth")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if user_exists(email):
            st.error("User with this email already exists!")
        else:
            save_user({"name": name, "phone": phone, "dob": str(dob), "email": email, "password": password})
            os.makedirs(email)  # Create a directory for the user
            st.success("User registered successfully!")
            st.info("Go to the login page to sign in.")

def login_user(email, password):
    users = load_users()
    if email in users and users[email]['password'] == password:
        return True
    return False

def login_page():
    st.title("Welcome to the Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(email, password):
            st.success(f"Welcome {email}!")
            return email
        else:
            st.error("Invalid email or password!")
    return None

def input_marks(email):
    st.title(f"Welcome {email}")
    subjects = ["Math", "English", "Science", "History", "Geography", "Physics", "Chemistry"]
    marks = {}

    for subject in subjects:
        marks[subject] = st.slider(f"Choose your marks for {subject}", 0, 100, 50)

    if st.button("Submit"):
        df = pd.DataFrame(marks.items(), columns=["Subject", "Marks"])
        df.to_csv(f"{email}/marks.csv", index=False)
        st.success("Marks saved successfully!")

def save_marks(email, marks):
    user_folder = os.path.join(USER_DATA_DIR, email)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    marks_file = os.path.join(user_folder, 'marks.csv')
    df = pd.DataFrame(marks.items(), columns=['Subject', 'Marks'])
    df.to_csv(marks_file, index=False)

def generate_report(email):
    st.title("Your Reports are Ready!")
    df = pd.read_csv(f"{email}/marks.csv")

    st.subheader("Average Marks - Bar Graph")
    bar_fig = px.bar(df, x="Subject", y="Marks", title="Marks per Subject")
    st.plotly_chart(bar_fig)

    st.subheader("Marks per Subject - Line Graph")
    line_fig = px.line(df, x="Subject", y="Marks", title="Marks Trend")
    st.plotly_chart(line_fig)

    st.subheader("Marks per Subject - Pie Chart")
    pie_fig = px.pie(df, values="Marks", names="Subject", title="Marks Distribution")
    st.plotly_chart(pie_fig)

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ["Sign Up", "Log In", "Input Marks", "Generate Reports"])

    if choice == "Sign Up":
        register_user()
    elif choice == "Log In":
        logged_in_user = login_page()
        if logged_in_user:
            st.session_state["user"] = logged_in_user
    elif choice == "Input Marks":
        if "user" in st.session_state:
            input_marks(st.session_state["user"])
        else:
            st.error("Please log in first!")
    elif choice == "Generate Reports":
        if "user" in st.session_state:
            generate_report(st.session_state["user"])
        else:
            st.error("Please log in first!")

if __name__ == "__main__":
    main()
