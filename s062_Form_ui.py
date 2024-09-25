import streamlit as st
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Create users directory
USER_DATA_DIR = 'user_data'
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

# JSON file to store login details for each user
def load_user_data():
    user_file = os.path.join(USER_DATA_DIR, 'users.json')
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_user_data(user_data):
    user_file = os.path.join(USER_DATA_DIR, 'users.json')
    with open(user_file, 'w') as f:
        json.dump(user_data, f)

# Load and save marks
def save_marks(email, marks):
    user_folder = os.path.join(USER_DATA_DIR, email)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    marks_file = os.path.join(user_folder, 'marks.csv')
    df = pd.DataFrame(marks.items(), columns=['Subject', 'Marks'])
    df.to_csv(marks_file, index=False)

def load_marks(email):
    marks_file = os.path.join(USER_DATA_DIR, email, 'marks.csv')
    if os.path.exists(marks_file):
        return pd.read_csv(marks_file)
    return None

# Signout function
def signout():
    if 'user' in st.session_state:
        del st.session_state['user']

# Login function
def handle_login(email, password):
    user_data = load_user_data()
    if email in user_data:
        if user_data[email]['password'] == password:
            st.session_state['user'] = email
            st.success(f"Welcome, {user_data[email]['name']}!")
        else:
            st.error("Incorrect password.")
    else:
        st.error("User does not exist. Please sign up first.")

# Signup function
def handle_signup(name, phone, dob, email, password):
    user_data = load_user_data()
    if email in user_data:
        st.error("Email already exists! Please use a different email.")
    else:
        user_data[email] = {'name': name, 'phone': phone, 'dob': str(dob), 'password': password}
        save_user_data(user_data)
        os.makedirs(os.path.join(USER_DATA_DIR, email), exist_ok=True)
        st.success("Signup successful! Please login.")

# Main Application
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Signup", "Login", "Signout"])

    if page == "Signup":
        st.title("Welcome to the Signup Page")
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        dob = st.date_input("Date of Birth")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            handle_signup(name, phone, dob, email, password)

    elif page == "Login":
        st.title("Login Page")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            handle_login(email, password)

    elif page == "Signout":
        signout()
        st.success("Signed out successfully!")
        st.experimental_rerun()

    # After login: Get the username and proceed to the next steps
    if 'user' in st.session_state:
        email = st.session_state['user']
        user_data = load_user_data()
        username = user_data[email]['name']

        # Step 2: Welcome page after sign in
        st.title(f"Welcome {username}!")
        subjects = ["Maths", "Science", "English", "Hindi", "History", "Civics", "Geography"]
        marks = {}

        for subject in subjects:
            marks[subject] = st.slider(f"Choose your marks for {subject}", 0, 100)

        if st.button("Submit Marks"):
            save_marks(email, marks)
            st.success("Marks submitted successfully!")

        # Provide option to download the marks CSV
        user_folder = os.path.join(USER_DATA_DIR, email)
        marks_file = os.path.join(user_folder, 'marks.csv')

        if os.path.exists(marks_file):
            with open(marks_file, 'rb') as f:
                st.download_button(label="Download Marks CSV", data=f, file_name='marks.csv', mime='text/csv')

        # Step 3: Reports page
        st.title("Your Reports are Ready!")
        marks_data = load_marks(email)
        if marks_data is not None:
            # Average marks
            avg_marks = marks_data['Marks'].mean()

            # Bar chart - Average marks
            st.subheader("Average Marks (Bar Chart)")
            st.bar_chart(marks_data.set_index('Subject'))

            # Line chart - Marks per subject
            st.subheader("Marks per Subject (Line Chart)")
            st.line_chart(marks_data.set_index('Subject'))

            # Pie chart - Marks per subject
            st.subheader("Marks per Subject (Pie Chart)")
            fig, ax = plt.subplots()
            ax.pie(marks_data['Marks'], labels=marks_data['Subject'], autopct='%1.1f%%')
            st.pyplot(fig)

# Run the app
if __name__ == "__main__":
    main()
