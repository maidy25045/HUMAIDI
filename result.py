import streamlit as st
import json
from datetime import datetime

def view_result_by_roll():
    with open("data/result.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    st.markdown("<h2 style='text-align:center; color:#1b5e20;'>📋রোল নম্বর দিয়ে ফলাফল দেখো</h2>", unsafe_allow_html=True)

    # Custom CSS for design
    st.markdown("""
        <style>
        .result-card {
            background-color: white;
            border-radius: 15px;
            padding: 25px;
            margin-top: 30px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            font-family: 'Segoe UI', sans-serif;
            color: #212121;
        }
        .result-card h2 {
            color: #2e7d32;
            text-align: center;
            margin-bottom: 20px;
        }
        .info-row {
            font-size: 18px;
            margin: 8px 0;
            color: #212121;
        }
        .info-row span {
            font-weight: bold;
            color: #212121;
        }
        </style>
    """, unsafe_allow_html=True)

    roll = st.text_input("🔍 রোল নম্বর")

    if st.button("ফলাফল দেখো"):
        student = next((s for s in results if s["roll"] == roll), None)

        if student:
            st.markdown(f"""
            <div class='result-card'>
                <h2>📊 ফলাফল সংক্ষিপ্ত বিবরণ</h2>
                <div class='info-row'>👤 <span>নাম:</span> {student['name']}</div>
                <div class='info-row'>🎓 <span>রোল নম্বর:</span> {student['roll']}</div>
                <div class='info-row'>🧪 <span>পরীক্ষা:</span> {student['exam']}</div>
                <div class='info-row'>✅ <span>স্কোর:</span> <span style='color:green; font-weight:bold;'>{student['score']} নম্বর</span></div>
                <div class='info-row'>✔️ <span>সঠিক উত্তর:</span> {student['correct']} টি</div>
                <div class='info-row'>❌ <span>ভুল উত্তর:</span> {student['wrong']} টি</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❗ এই রোল নম্বরের জন্য কোনো ফলাফল পাওয়া যায়নি। অথবা, তুমি পরীক্ষা দাওনি")
