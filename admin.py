import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
client = MongoClient(st.secrets["MONGO_URI"])
db = client["exam_database"]

# Admin credentials
USERNAME = st.secrets.get("USERNAME", "admin")
PASSWORD = st.secrets.get("PASSWORD", "admin")

# Admin Login Function
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        admin = db.admins.find_one({"username": username, "password": password})
        if admin:
            st.session_state["admin_logged_in"] = True
            st.session_state["admin_username"] = username
            st.success(f"Logged in as Admin: {username}")
            st.rerun()
        else:
            st.error("Invalid credentials")

# Admin Panel Function
def admin_panel():
    st.title("Admin Panel")

    # ---------------- Create Exam ----------------
    st.subheader("🛠️Create Exam")
    exam_name = st.text_input("Exam Name")
    exam_duration = st.number_input("Duration (minutes)", min_value=1)
    negative_marking = st.checkbox("Enable Negative Marking (-0.25 per wrong answer)", value=False)
    
    # Add the option for the admin to set the exam start time
    exam_date = st.date_input("Select Exam Start Date", value=datetime.now())
    exam_time = st.time_input("Select Exam Start Time", value=datetime.now().time())
    exam_start_time = datetime.combine(exam_date, exam_time)

    if st.button("Create Exam"):
        try:
            # Insert new exam into database
            db.exams.insert_one({
                "name": exam_name,
                "duration": exam_duration,
                "negative_marking": negative_marking,
                "start_time": exam_start_time,  # Save the start time in the database
            })
            st.success(f"✔️Exam '{exam_name}' created with start time {exam_start_time}.")
        except Exception as e:
            st.error(f"⚠️ Error creating exam: {e}")
    

    # ---------------- Add Question ----------------
    st.subheader("💡Add Question")
    exams = list(db.exams.find())
    exam_options = [exam["name"] for exam in exams]

    if exam_options:
        selected_exam = st.selectbox("Select Exam", exam_options)
        question_text = st.text_area("Question")
    
    options = []
    option_images = []
    for i in range(4):
        col1, col2 = st.columns([2, 1])
        with col1:
            option_text = st.text_input(f"Option {i+1} Text", key=f"text_{i}")
        with col2:
            option_image = st.file_uploader(f"Option {i+1} Image (optional)", type=["jpg", "png", "jpeg"], key=f"img_{i}")
        options.append(option_text)
        option_images.append(option_image.read() if option_image else None)
    
    correct_answer = st.selectbox("Correct Answer", options)
    question_image = st.file_uploader("Upload Question Image (optional)", type=["jpg", "png", "jpeg"])

    if st.button("Add Question"):
        try:
            question_data = {
                "exam": selected_exam,
                "question": question_text,
                "options": options,
                "option_images": option_images,  # Optional images per option
                "answer": correct_answer,
                "image": question_image.read() if question_image else None
            }
            db.questions.insert_one(question_data)
            st.success("✔️Question added successfully.")
        except Exception as e:
            st.error(f"⚠️ Error adding question: {e}")
    
    # ---------------- Upload Solve Sheet via Link ----------------
    st.subheader("📂Add Solve Sheet (PDF Link)")
    pdf_name = st.text_input("Enter a title for the PDF (e.g., 'Math Solve Sheet')")
    pdf_link = st.text_input("Paste Google Drive or PDF Viewer Link")

    if st.button("Add PDF Link"):
        try:
            if pdf_name and pdf_link:
                db.solve_sheets.insert_one({
                    "name": pdf_name,
                    "uploaded_at": datetime.now(),
                    "pdf_link": pdf_link
                })
                st.success("✔️PDF link added successfully.")
            elif not pdf_name:
                st.warning("⚠️Please enter a title for the PDF.")
            else:
                st.warning("⚠️Please paste a valid PDF link.")
        except Exception as e:
            st.error(f"⚠️ Error adding PDF link: {e}")
