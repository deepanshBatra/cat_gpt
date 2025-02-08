import streamlit as st

# Set up Streamlit page
st.set_page_config(page_title="Choose Your AI Avatar", page_icon="🤖", initial_sidebar_state="collapsed")

st.title("Welcome to CatGPT 🐱")
st.write("Select your expert to begin chatting:")

col1, col2 = st.columns(2)

with col1:
    st.image("namoosh.webp", width=150)  # Placeholder image for Zen
    st.subheader("Namoosh, the Wise Scientist")
    st.write("Do anything but don't sneeze!!!")
    if st.button("Choose Namshi"):
        st.session_state.selected_avatar = "Namshi"
        st.switch_page("pages/namoosh.py")  # Redirect to chat page

with col2:
    st.image("dandon.webp", width=150)  # Placeholder image for Bolt
    st.subheader("Dandon, the Queen")
    st.write("The queen demands more dry food")
    if st.button("Choose Malkti"):
        st.session_state.selected_avatar = "Malkti"
        st.switch_page("pages/dandon.py")  # Redirect to chat page
