import streamlit as st
import sqlite3

# Database Connection
conn = sqlite3.connect("dreamfund.db", check_same_thread=False)
cur = conn.cursor()

# Create Table
cur.execute("""
CREATE TABLE IF NOT EXISTS goals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_name TEXT,
    target_amount REAL,
    current_amount REAL DEFAULT 0
)
""")
conn.commit()

st.title("💰 DreamFund AI")

menu = st.sidebar.selectbox(
    "Menu",
    ["Create Goal", "Add Savings", "View Goals", "AI Analysis"]
)

# CREATE GOAL
if menu == "Create Goal":

    st.header("Create Goal")

    goal = st.text_input("Goal Name")

    target = st.number_input(
        "Target Amount",
        min_value=1.0
    )

    if st.button("Create Goal"):

        cur.execute(
            """
            INSERT INTO goals
            (goal_name, target_amount, current_amount)
            VALUES (?, ?, 0)
            """,
            (goal, target)
        )

        conn.commit()

        st.success("Goal Created Successfully!")

# ADD SAVINGS
elif menu == "Add Savings":

    st.header("Add Savings")

    goals = cur.execute(
        "SELECT id, goal_name FROM goals"
    ).fetchall()

    if goals:

        selected_goal = st.selectbox(
            "Select Goal",
            goals,
            format_func=lambda x: x[1]
        )

        amount = st.number_input(
            "Amount to Add",
            min_value=1.0
        )

        if st.button("Add Savings"):

            cur.execute(
                """
                UPDATE goals
                SET current_amount = current_amount + ?
                WHERE id = ?
                """,
                (amount, selected_goal[0])
            )

            conn.commit()

            st.success("Savings Added!")

    else:

        st.warning("No goals found.")

# VIEW GOALS
elif menu == "View Goals":

    st.header("All Goals")

    goals = cur.execute(
        """
        SELECT goal_name,
               target_amount,
               current_amount
        FROM goals
        """
    ).fetchall()

    for goal, target, current in goals:

        st.subheader(goal)

        progress = min(current / target, 1.0)

        st.progress(progress)

        st.write(
            f"₹{current:,.0f} / ₹{target:,.0f}"
        )

        st.write(
            f"{progress * 100:.1f}% Completed"
        )

# AI ANALYSIS
elif menu == "AI Analysis":

    st.header("🤖 DreamFund AI Analysis")

    goals = cur.execute(
        """
        SELECT goal_name,
               target_amount,
               current_amount
        FROM goals
        """
    ).fetchall()

    for goal, target, current in goals:

        progress = (current / target) * 100

        if progress < 30:

            advice = (
                "⚠️ Behind Schedule. "
                "Try increasing monthly savings."
            )

        elif progress < 70:

            advice = (
                "✅ On Track. "
                "Keep saving consistently."
            )

        else:

            advice = (
                "🚀 Excellent Progress! "
                "Goal is within reach."
            )

        st.subheader(goal)

        st.write(
            f"Progress: {progress:.1f}%"
        )

        st.info(advice)

