import streamlit as st

st.set_page_config(page_title="Career Guidance System")

# session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🔥 Student Career Guidance System")

# IF LOGGED IN → DASHBOARD
if st.session_state.logged_in:
    st.sidebar.success("Logged in ✅")

    st.header("📊 Dashboard")
    st.write("Welcome nanba 😎🔥")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

else:
    menu = ["Home", "Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.header("🏠 Home Page")
        st.write("This is your final year project")

    elif choice == "Login":
        st.header("🔐 Login Page")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "saravanan_1437" and password == "1234":
                st.session_state.logged_in = True
                st.success("Login Successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

    elif choice == "Register":
        st.header("📝 Register Page")
        st.text_input("Create Username")
        st.text_input("Create Password", type="password")
        st.button("Register")
