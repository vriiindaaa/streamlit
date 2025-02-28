import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

def connectdb():
    conn = sqlite3.connect("mydb.db")
    return conn

def createTable():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name TEXT, password TEXT, roll INTEGER PRIMARY KEY, branch TEXT)")
        conn.commit()

def addRecord(data):
    with connectdb() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO student (name, password, roll, branch) VALUES (?, ?, ?, ?)", data)
            conn.commit()
        except sqlite3.IntegrityError:
            st.error("Student already registered...")

def display(branch_filter=None):
    with connectdb() as conn:
        cur = conn.cursor()
        if branch_filter and branch_filter != "All":
            cur.execute("SELECT * FROM student WHERE branch = ?", (branch_filter,))
        else:
            cur.execute("SELECT * FROM student")
        return cur.fetchall()

def search_by_roll(roll):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE roll = ?", (roll,))
        return cur.fetchone()

def reset_password(roll, new_password):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE student SET password = ? WHERE roll = ?", (new_password, roll))
        conn.commit()
        st.success("Password updated successfully!")

def delete_student(roll):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE roll = ?", (roll,))
        conn.commit()
        st.success("Student deleted successfully!")

def signup():
    st.title("Registration Page")
    name = st.text_input("Enter your username")
    password = st.text_input("Enter the Password", type='password')
    repassword = st.text_input("Retype your password", type='password')
    roll = st.number_input("Enter the Roll Number")
    branch = st.selectbox("Branch", options=["CSE", "AIML", "ECE", "RA"])
    
    if st.button('Sign Up'):
        if password != repassword:
            st.warning("Password Mismatch")
        elif not name or not password or not roll or not branch:
            st.warning("All fields are required!")
        else:
            addRecord((name, password, int(roll), branch))
            st.success("Student Registered Successfully!")

def reset_password_page():
    st.title("Reset Password")
    roll = st.number_input("Enter Roll Number")
    new_password = st.text_input("Enter New Password", type='password')
    
    if st.button("Update Password"):
        student = search_by_roll(int(roll))
        if student:
            reset_password(int(roll), new_password)
        else:
            st.error("Roll number not found!")

def delete_student_page():
    st.title("Delete Student")
    roll = st.number_input("Enter Roll Number")
    
    if st.button("Delete Student"):
        student = search_by_roll(int(roll))
        if student:
            delete_student(int(roll))
        else:
            st.error("Roll number not found!")

def search_student_page():
    st.title("Search Student by Roll Number")
    roll = st.number_input("Enter Roll Number")
    
    if st.button("Search"):
        student = search_by_roll(int(roll))
        if student:
            st.write(f"*Name:* {student[0]}")
            st.write(f"*Roll Number:* {student[2]}")
            st.write(f"*Branch:* {student[3]}")
        else:
            st.error("Student not found!")

def display_students():
    st.title("Student Records")
    branch_filter = st.selectbox("Filter by Branch", ["All", "CSE", "AIML", "ECE", "RA"])
    data = display(branch_filter)
    
    if data:
        st.table(data)
    else:
        st.info("No records found.")

with st.sidebar:
    selected = option_menu("My App", ['Signup', 'Display Students', 'Search Student', 'Reset Password', 'Delete Student'])

createTable()

if selected == "Signup":
    signup()
elif selected == "Display Students":
    display_students()
elif selected == "Search Student":
    search_student_page()
elif selected == "Reset Password":
    reset_password_page()
elif selected == "Delete Student":
    delete_student_page()
