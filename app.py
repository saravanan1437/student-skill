elif choice == "Register":
    st.header("📝 Register Page")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if new_user and new_pass:
            st.success("Account Created ✅")

            # 🔥 AUTO LOGIN
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Fill all fields ❌")
