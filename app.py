import streamlit as st

st.set_page_config(page_title="Career Guidance System")

st.title("🔥 Student Career Guidance System")
st.write("Welcome nanba 😎")

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
        st.success("Login Successful ✅")

elif choice == "Register":
    st.header("📝 Register Page")
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    if st.button("Register"):
        st.success("Account Created ✅")
