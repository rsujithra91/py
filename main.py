```python
import streamlit as st
import sqlite3

# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

conn = sqlite3.connect("dreamfund.db", check_same_thread=False)
cur = conn.cursor()

# -------------------------------------------------
# CREATE TABLE
# -------------------------------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_name TEXT,
    target_amount REAL,
    current_amount REAL DEFAULT 0
)
""")

conn.commit()

# -------------------------------------------------
# BACKGROUND COLOR
# -------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #E8F5E9;
}

h1 {
    color: #1B5E20;
}

h2, h3 {
    color: #2E7D32;
}

[data-testid="stSidebar"] {
    background-color: #C8E6C9;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("💰 DreamFund AI")

# -------------------------------------------------
# MENU
# -------------------------------------------------

menu = st.sidebar.selectbox(
    "Menu",
    ["Create Goal", "Add Savings", "View Goals", "AI Analysis"]
)

# -------------------------------------------------
# CREATE GOAL
# -------------------------------------------------

if menu == "Create Goal":

    st.header("Create Goal")

    goal = st.text_input("Goal Name")

    target = st.number_input(
        "Target Amount",
        min_value=1.0
    )

    if st.button("Create Goal"):

        if goal.strip() == "":
            st.warning("Please enter a goal name.")

        else:
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

# -------------------------------------------------
# ADD SAVINGS
# -------------------------------------------------

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

# -------------------------------------------------
# VIEW GOALS
# -------------------------------------------------

elif menu == "View Goals":

    st.header("All Goals")

    goals = cur.execute(
        """
        SELECT goal_name, target_amount, current_amount
        FROM goals
        """
    ).fetchall()

    if goals:

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

    else:
        st.warning("No goals found. Create a goal first.")

# -------------------------------------------------
# AI ANALYSIS
# -------------------------------------------------

elif menu == "AI Analysis":

    st.header("🤖 DreamFund AI Analysis")

    goals = cur.execute(
        """
        SELECT goal_name, target_amount, current_amount
        FROM goals
        """
    ).fetchall()

    if goals:

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

    else:
        st.warning("No goals available for analysis.")
```

### Important

Your error:

```text
"SELECT id, goal_n_
SyntaxError: unterminated string literal
```

means Python found an opening quote (`"`) but **didn't find the matching closing quote**.

In the corrected code, this section is properly written:

```python
goals = cur.execute(
    "SELECT id, goal_name FROM goals"
).fetchall()
```

So replace **all the existing code in `main.py`** with the code above, save it, and redeploy/re-run your Streamlit a
