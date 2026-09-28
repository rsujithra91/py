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
CREATE TABLE IF NOT EXISTS goals(
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

/* Title */
h1 {
    color: #1B5E20;
}

/* Headers */
h2, h3 {
    color: #2E7D32;
}

/* Sidebar */
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
        "SELECT id, goal_n_
```
