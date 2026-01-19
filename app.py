import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd

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
with tab2:
    st.markdown(
            "<div class='glow-blue'><h2 style='color:#00bfff;'><U>WasteLess League</U> : <I><U>Save smarter</U> <U>and</U> <U>Level higher</u></I></h2></div>",
            unsafe_allow_html=True
        )
    st.write("")

    if "history" not in st.session_state:
        st.session_state.history = []

    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = {
            "Alder Mess": 0,
            "Oak Mess": 0,
            "Peepal Mess": 0,
            "Pine Mess": 0,
            "Tulsi Mess": 0
        }
    if role == "Staff":
        # Mess Selection
        st.subheader("🏫 Select Mess")
        mess = st.radio(
            "Which Mess are you representing?",
            ["Alder Mess", "Oak Mess", "Peepal Mess", "Pine Mess", "Tulsi Mess"],
            horizontal=True
        )

        # Food Input Section
        st.subheader("🥗 Track Today's Food Waste")

        colA, colB = st.columns(2)

        with colA:
            taken_slider = st.slider("Meals Taken (approx.)", 0, 1000, 300)
            taken_input = st.number_input("Or Enter Exact Meals Taken", min_value=0, value=taken_slider)
            meals_taken = taken_input if taken_input != taken_slider else taken_slider

        with colB:
            wasted_slider = st.slider("Meals Wasted (approx.)", 0, taken_input, 50)
            wasted_input = st.number_input("Or Enter Exact Meals Wasted", min_value=0, value=wasted_slider)
            meals_wasted = wasted_input if wasted_input != wasted_slider else wasted_slider# Calculations
        efficiency = 0 if meals_taken == 0 else max(0, 100 - ((meals_wasted / meals_taken) * 100))
        points = int(efficiency)

        # Display Performance
        st.markdown(f"""
        **Efficiency Score:** `{efficiency:.2f}%`  
        **Points Earned:** `{points}`
        """)

        # Submit Button
        if st.button("Submit Score"):

            # Ensure leaderboard entry exists
            if mess not in st.session_state.leaderboard:
                st.session_state.leaderboard[mess] = 0

            st.session_state.leaderboard[mess] += points

            st.session_state.history.append({
                "Mess": mess,
                "Taken": meals_taken,
                "Wasted": meals_wasted,
                "Efficiency %": round(efficiency, 2),
                "Points": points
            })

            st.success(f"Score submitted for {mess}! 🎉")

    # Nudges
    st.caption("💡 Taking only what you eat maximizes efficiency — waste less to dominate the leaderboard!")

    # Leaderboard Display
    # 🏆 Styled Leaderboard Display
    st.subheader("🏆 Current Leaderboard")

    sorted_board = sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True)

    # Custom CSS for glowing leaderboard cards
    st.markdown("""
    <style>
    .leader-card {
        border: 2px solid rgba(0,255,0,0.8);
        padding: 10px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
        background: rgba(0, 0, 0, 0.65);
        color: #ccffcc;
        font-size: 18px;
        font-weight: 600;
        text-shadow: 0 0 6px #00ff55;
        display: flex;
        justify-content: space-between;
    }
    .rank-box {
        font-size: 20px;
        font-weight: 800;
        color: gold;
        margin-right: 12px;
        text-shadow: 0 0 8px gold;
    }
    </style>
    """, unsafe_allow_html=True)

    for rank, (m, p) in enumerate(sorted_board, 1):
        st.markdown(
            f"""
            <div class="leader-card">
                <div class="rank-box">#{rank}</div>
                <div>{m}</div>
                <div><b>{p} pts</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write(" ")

    # Match History
    st.subheader("📜 Input History")
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("No match history yet — start playing!")

    st.markdown("---")
    st.subheader("🎯 Game Insights")

    # Sustainability nudges
    st.markdown("""
            💬 **Strategic Tips to Win:**
            - Serve smaller portions first
            - Take seconds only if needed
            - Avoid wasting carbs (they score higher penalties)
            - Push for Zero Waste streaks to earn bonus points 🎖️
        """)

    # Motivational random nudge
    import random
    nudges = [
            "Small servings = Big wins!",
            "Waste less. Score more!",
            "Your plate decides your mess' fate!",
            "Nature approves your clean plate 🌱",
            "Zero waste streak coming ???",
            "Other hostels are watching your position too👀"
    ]
    st.markdown(f"🧩 **Not a Nudge (just saying):**  _{random.choice(nudges)}_")

    # End-of-view badge suggestions
    st.markdown("""
        <div style='margin-top:15px; padding:10px; border-radius:10px; background:#111;'>
        🏅 <b>Upcoming Badges</b> <br>
        - Zero Waste Hero<br>
        - Plate Master<br>
        - Eco Elite<br>
        - Hostel Guardian
        </div>
    """, unsafe_allow_html=True)

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

