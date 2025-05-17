import streamlit as st
import json
import os

def load_routine():
    path = os.path.join("data", "routine.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: The file '{path}' was not found. Please ensure it exists in the 'data' folder.")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON from '{path}': {e}")
        return None

def routine_view():
    st.title("⏳Exam Routine")

    routine_data = load_routine()

    if routine_data is None:
        return

    st.markdown("""
    <style>
        .routine-box {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .routine-title {
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .exam-row {
            padding: 8px;
            background-color: #ffffff;
            border-radius: 5px;
            margin-bottom: 5px;
            border-left: 5px solid #3498db;
            color : black;
        }
    </style>
    """, unsafe_allow_html=True)

    if not routine_data:
        st.info("No exam routine data available.")
        return

    for day_schedule in routine_data:
        day = day_schedule.get("day")
        exams = day_schedule.get("exam", [])

        if day:
            st.markdown(f"""
            <div class="routine-box">
                <div class="routine-title">🌤️ {day}</div>
            """, unsafe_allow_html=True)

            if exams:
                for exam in exams:
                    time = exam.get("time")
                    subject = exam.get("subject")
                    topic = exam.get("topic")

                    if time and subject:
                        topic_display = f"🏷️ <i>{topic}</i>" if topic else ""
                        st.markdown(f"""
                        <div class="exam-row">
                            🕒 <b>{time}</b><br>
                            📚 <b>{subject}</b><br>
                            {topic_display}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning(f"Incomplete exam information for {day}.")
            else:
                st.info(f"No exams scheduled for {day}.")

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Missing 'day' information in the routine data.")

if __name__ == "__main__":
    routine_view()
