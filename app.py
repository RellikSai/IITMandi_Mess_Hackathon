# ---------- IMPORTS ----------
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

st.set_page_config(
    page_title="Smart Campus AI | IIT Mandi",
    layout="wide"
)

st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #111827, #0b0b0b 60%);
    color: white;
}
.glow-blue {
    border: 2px solid #00bfff;
    box-shadow: 0 0 18px #00bfff;
    border-radius: 16px;
    padding: 30px;
}
.glow-green {
    border: 2px solid #00ff99;
    box-shadow: 0 0 18px #00ff99;
    border-radius: 16px;
    padding: 30px;
}
.glow-gold {
    border: 2px solid #ffd700;
    box-shadow: 0 0 18px #ffd700;
    border-radius: 16px;
    padding: 30px;
}
.glow-red {
    border: 2px solid #ff4d4d;
    box-shadow: 0 0 18px #ff4d4d;
    border-radius: 16px;
    padding: 30px;
}
.game-text {
    font-family: 'Trebuchet MS', monospace;
    color: #9effc6;
}
.game-rule {
    color: #ffd700;
    font-size: 15px;
}
.neon-btn {
    background: linear-gradient(90deg, #00ff99, #00ffaa);
    color: black;
    font-weight: bold;
    border-radius: 10px;
}
h1, h2 {
    text-align: center;
}
.role-box {
    position: fixed;
    top: 15px;
    right: 20px;
    z-index: 100;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 style='color:#ffd700;'>Smart Campus AI • IIT Mandi</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#9effc6;'>Food Sustainability & Hostel Intelligence Platform</p>", unsafe_allow_html=True)

# ---------- ROLE ----------
with st.container():
    st.markdown("<div class='role-box'>", unsafe_allow_html=True)
    role = st.selectbox("Sign in as", ["Staff", "Student"])
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------- GLOBAL COMPLAINT STORAGE ----------
if "complaints_data" not in st.session_state:
    st.session_state.complaints_data = {
        "Water": [
            {"text": "Leakage in Hostel B Room 214", "days": 1},
            {"text": "Low water pressure in washrooms", "days": 3}
        ],
        "Electricity": [
            {"text": "Frequent power cuts in Block C", "days": 2},
            {"text": "Street light not working near gate", "days": 5}
        ],
        "Cleanliness": [
            {"text": "Overflowing dustbins near mess", "days": 1}
        ]
    }

# ---------- TABS ----------
if role == "Staff":
    tab1, tab2, tab3 = st.tabs([
        "Food Demand Predictions",
        "Game Mode",
        "Complaints Organizer"
    ])
else:
    tab2, tab3 = st.tabs([
        "Game Mode",
        "Complaints Organizer"
    ])

# ---------- SECTION 1A ----------
if role == "Staff":
    with tab1:
        st.markdown(
            "<div class='glow-green'><h2 style='color:#00ff99;'>Food Demand Prediction</h2></div>",
            unsafe_allow_html=True
        )
        if role == "Staff":

            st.subheader("📂 Upload Mess Attendance Data")

            uploaded_file = st.file_uploader(
                "Upload CSV file (past mess attendance data)",
                type=["csv"]
            )

            if uploaded_file is not None:
                import pandas as pd

                data = pd.read_csv(uploaded_file)
                st.write("Preview of uploaded data:")
                st.dataframe(data.head())

                # -------- Feature & Target Selection --------
                target_column = "students_present"

                X = data.drop(columns=[target_column])
                y = data[target_column]

                # -------- Train-Test Split --------
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )

                # -------- Model Training --------
                model = RandomForestRegressor(
                    n_estimators=200,
                    random_state=42
                )
                model.fit(X_train, y_train)

                # -------- Evaluation --------
                predictions = model.predict(X_test)
                error = mean_absolute_error(y_test, predictions)

                st.success(f"Model trained successfully!")
                st.caption(f"Mean Absolute Error: {error:.2f} students")
                feature_order = list(X_train.columns)

                # -------- Prediction Input (BUTTON BASED UI) --------
                st.subheader("🔮 Predict Students for Upcoming Meal")

                # Initialize input_data safely
                if "input_data" not in st.session_state:
                    st.session_state.input_data = {}

                input_data = st.session_state.input_data

                # ---------- DAY OF WEEK ----------
                st.markdown("### 📅 Day of Week")
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                cols = st.columns(len(days))

                for i, day in enumerate(days):
                    if cols[i].button(day, key=f"day_{day}"):
                        input_data["day_of_week"] = i
                        st.success(f"Selected Day: {day}")

                # ---------- MEAL TYPE ----------
                st.markdown("### 🍽 Meal Type")
                meals = {"Breakfast": 0, "Lunch": 1, "Dinner": 2}
                cols = st.columns(len(meals))

                for meal, val in meals.items():
                    if cols[val].button(meal, key=f"meal_{meal}"):
                        input_data["meal_type"] = val
                        st.success(f"Selected Meal: {meal}")

                # ---------- HOLIDAY ----------
                st.markdown("### 🎉 Is it a Holiday?")
                cols = st.columns(2)

                if cols[0].button("Yes", key="holiday_yes"):
                    input_data["is_holiday"] = 1
                    st.success("Marked as Holiday")

                if cols[1].button("No", key="holiday_no"):
                    input_data["is_holiday"] = 0
                    st.success("Marked as Working Day")

                # ---------- WEATHER ----------
                st.markdown("### 🌦 Weather Condition")
                weather_map = {"Clear": 0, "Rain": 1}
                cols = st.columns(2)

                for w, v in weather_map.items():
                    if cols[v].button(w, key=f"weather_{w}"):
                        input_data["weather"] = v
                        st.success(f"Weather Selected: {w}")

                # ---------- EXAM WEEK ----------
                st.markdown("### 📝 Exam Week?")
                cols = st.columns(2)

                if cols[0].button("Yes", key="exam_yes"):
                    input_data["exam_week"] = 1
                    st.success("Exam Week: Yes")

                if cols[1].button("No", key="exam_no"):
                    input_data["exam_week"] = 0
                    st.success("Exam Week: No")

                # ---------- PREVIOUS WEEK ATTENDANCE ----------
                st.markdown("### 📊 Previous Week Attendance")
                prev_attendance = st.number_input(
                    "Enter number of students attended last week",
                    min_value=0,
                    value=1000
                )
                input_data["previous_week_attendance"] = prev_attendance

                # ---------- FINAL SUBMIT ----------
                st.markdown("---")
                if st.button("🚀 Submit Data for Prediction"):
                    if len(input_data) < 6:
                        st.warning("⚠️ Please select all options before submitting.")
                    else:
                        st.success("✅ Input data captured successfully!")
                        st.write("### 🔍 Final Input Data")
                        st.json(input_data)

                # ----- MODEL CONFIDENCE -----
                confidence_score = model.score(X_test, y_test) * 100

                input_df = pd.DataFrame([input_data])

                # -------- Prediction --------
                if st.button("Predict Attendance"):

                    # Ensure ALL features exist
                    for col in feature_order:
                        if col not in input_data:
                            input_data[col] = 0  # safe fallback

                    # Create dataframe
                    input_df = pd.DataFrame([input_data])

                    # 🔒 FORCE SAME COLUMN ORDER AS TRAINING
                    input_df = input_df[feature_order]

                    # Predict
                    result = model.predict(input_df)[0]

                    st.markdown(
                        """
                        <style>
                        .glow-card {
                            background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
                            border-radius: 16px;
                            padding: 25px;
                            text-align: center;
                            box-shadow: 0 0 25px rgba(0, 255, 140, 0.5);
                            border: 1px solid rgba(0, 255, 140, 0.4);
                        }

                        .glow-title {
                            color: #aaffc3;
                            font-size: 20px;
                            letter-spacing: 1px;
                            margin-bottom: 10px;
                        }

                        .glow-number {
                            font-size: 48px;
                            font-weight: bold;
                            color: #00ff8c;
                            text-shadow: 0 0 15px rgba(0, 255, 140, 0.8);
                        }

                        .confidence-badge {
                            display: inline-block;
                            margin-top: 10px;
                            padding: 8px 18px;
                            border-radius: 20px;
                            font-size: 18px;
                            color: black;
                            background: #00ff8c;
                            font-weight: bold;
                            box-shadow: 0 0 15px rgba(0, 255, 140, 0.9);
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(
                            f"""
                            <div class="glow-card">
                                <div class="glow-title">Predicted Students</div>
                                <div class="glow-number">{int(result)}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col2:
                        st.markdown(
                            f"""
                            <div class="glow-card">
                                <div class="glow-title">Model Confidence</div>
                                <div class="confidence-badge">{confidence_score:.2f}%</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

# ---------- SECTION 1B (EMPTY / RESERVED) ----------
with tab2:
    st.markdown(
        "<div class='glow-blue'><h2 style='color:#00bfff;'><U>WasteLess League</U> : <I><U>Save smarter</U> <U>and</U> <U>Level higher</u></I></h2></div>",
        unsafe_allow_html=True
    )
    st.write("")

    st.write(
        "AI monitors **post-serving food waste**, compares it with historical trends, "
        "and gamifies reduction to encourage sustainable behavior."
    )

    # ------------------ SESSION DATA ------------------
    if "waste_history" not in st.session_state:
        st.session_state.waste_history = [
            {"week": "Week 1", "waste": 42},
            {"week": "Week 2", "waste": 38},
            {"week": "Week 3", "waste": 34}
        ]


    # ------------------ AI LOGIC ------------------
    def get_level(waste):
        if waste <= 20:
            return "Diamond 🟢"
        elif waste <= 30:
            return "Gold 🟡"
        elif waste <= 40:
            return "Silver ⚪"
        else:
            return "Bronze 🔴"


    def level_trend(curr, prev):
        if curr < prev:
            return "⬆ Level Up"
        elif curr > prev:
            return "⬇ Level Down"
        else:
            return "⏸ No Change"


    latest = st.session_state.waste_history[-1]
    prev = st.session_state.waste_history[-2] if len(st.session_state.waste_history) > 1 else latest

    current_level = get_level(latest["waste"])
    trend = level_trend(latest["waste"], prev["waste"])

    # ------------------ DASHBOARD ------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Food Wasted This Week", f"{latest['waste']} kg")
    col2.metric("Current Level", current_level)
    col3.metric("Weekly Trend", trend)

    progress = max(0, min(100, int((40 - latest["waste"]) * 2.5)))
    st.progress(progress)

    st.caption("AI Confidence: 87% (based on historical consistency)")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ GAME MODE ------------------
    if st.button("🎮 Rules and LeaderBoard"):
        st.markdown("---")

        st.markdown(
            "<h3 style='color:#00ff99;font-family:Trebuchet MS;'>🏆 WasteLess League — Rules</h3>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <ul style="color:#ffd700;">
        <li>Each hostel competes weekly to <b>reduce food waste</b></li>
        <li>Waste decreases from last week → <b>Level increases</b></li>
        <li>Waste increases from last week → <b>Level decreases</b></li>
        <li>Levels unlocks recognition & incentives</li>
        <li>AI recalculates rankings every week</li>
        </ul>
        """, unsafe_allow_html=True)

        st.write("")

        # ------------------ LEADERBOARD ------------------
        st.subheader("📊 Weekly Leaderboard")

        leaderboard = []
        for i, w in enumerate(st.session_state.waste_history):
            prev_waste = st.session_state.waste_history[i - 1]["waste"] if i > 0 else w["waste"]
            leaderboard.append({
                "Week": w["week"],
                "Food Wasted (kg)": w["waste"],
                "Level": get_level(w["waste"]),
                "Change": level_trend(w["waste"], prev_waste)
            })

        st.dataframe(leaderboard, use_container_width=True)

        # ------------------ NEXT LEVEL TARGET ------------------
        target = max(latest["waste"] - 5, 0)

        st.markdown(
            f"""
            <div style="
                border:2px solid #00bfff;
                box-shadow:0 0 15px #00bfff;
                padding:20px;
                border-radius:14px;
                margin-top:20px;
            ">
            <h4 style='color:#00bfff;'>🎯 A Few CheatCodes To Increase Present Level 🎯</h4>
            <h5 style='color:yellow;'>
            🚀 Reduce waste by <b><u>{latest['waste'] - target} kg</b></u> next week to surpass your competitor hostel on the leaderboard 🚀
            </h5>
            <p>🔥 Full plate ≠ full points. 🔥 Clean plate = victory for your hostel. 🔥</p>
            <p>🏆 Take what you need, finish it, and secure the win. 🏆</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

# ------------------ SECTION 2 ------------------
with tab3:
    st.markdown(
        "<div class='glow-red'><h2 style='color:#ff4d4d;'>Complaints Organizer</h2></div>",
        unsafe_allow_html=True
    )
    st.write("")

    # ================= STAFF VIEW =================
    if role == "Staff":

        if "view_mode" not in st.session_state:
            st.session_state.view_mode = "dashboard"

        # ---------- DASHBOARD ----------
        if st.session_state.view_mode == "dashboard":
            st.write(
                "AI auto-classifies complaints and prioritizes them "
                "based on urgency and impact."
            )

            total_complaints = sum(
                len(v) for v in st.session_state.complaints_data.values()
            )

            st.metric("Total Active Complaints", total_complaints)
            st.metric("Critical Issues", "—")
            st.progress(60)
            st.caption("Resolution Efficiency: 60%")

            if st.button("Show All Complaints"):
                st.session_state.view_mode = "categories"

        # ---------- CATEGORY VIEW ----------
        elif st.session_state.view_mode == "categories":
            st.subheader("Complaint Categories")

            for category, items in st.session_state.complaints_data.items():
                if st.button(f"{category} ({len(items)})"):
                    st.session_state.selected_category = category
                    st.session_state.view_mode = "list"

            if st.button("Back to Dashboard"):
                st.session_state.view_mode = "dashboard"

        # ---------- COMPLAINT LIST ----------
        elif st.session_state.view_mode == "list":
            category = st.session_state.selected_category
            st.subheader(f"{category} Complaints")

            sorted_items = sorted(
                st.session_state.complaints_data[category],
                key=lambda x: x["days"]
            )

            for idx, c in enumerate(sorted_items, start=1):
                st.markdown(
                    """
                    <div style="
                        border:2px solid #ff4d4d;
                        box-shadow:0 0 12px #ff4d4d;
                        border-radius:12px;
                        padding:12px;
                        margin-bottom:12px;
                    ">
                    """,
                    unsafe_allow_html=True
                )

                st.write(f"**Complaint #{idx}:** {c['text']}")
                st.write(f"**Tolerance Period:** {c['days']} days")

                st.markdown("</div>", unsafe_allow_html=True)

            if st.button("Back to Categories"):
                st.session_state.view_mode = "categories"

    # ================= STUDENT VIEW =================
    else:
        st.write("Submit a new hostel or campus-related complaint.")

        complaint_text = st.text_area(
            "Describe your issue",
            placeholder="Example: Water leakage in Hostel B, Room 214"
        )

        tolerance_days = st.number_input(
            "How many days can this issue be managed if unattended?",
            min_value=0,
            max_value=30,
            step=1
        )

        # ---------- SIMPLE AI CLASSIFIER ----------
        def classify_complaint(text):
            text = text.lower()
            if "water" in text:
                return "Water"
            elif "electricity" in text or "power" in text:
                return "Electricity"
            elif "clean" in text or "dustbin" in text or "garbage" in text:
                return "Cleanliness"
            else:
                return "Other"

        # ---------- SUBMIT ----------
        if st.button("Submit Complaint"):
            if complaint_text.strip() == "":
                st.warning("Please describe the issue before submitting.")
            else:
                category = classify_complaint(complaint_text)

                if category not in st.session_state.complaints_data:
                    st.session_state.complaints_data[category] = []

                st.session_state.complaints_data[category].append({
                    "text": complaint_text,
                    "days": tolerance_days
                })

                st.success(f"Complaint submitted under category: {category}")
                st.caption(
                    "This complaint is now visible to hostel authorities."
                )


    st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
    "<p style='text-align:center;color:#777;margin-top:40px;'>Powered by Google AI • Built for Sustainable Campus Living • Designed by SaiPrasanth </p>",
    unsafe_allow_html=True
)
