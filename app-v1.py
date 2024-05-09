import streamlit as st
import random
import time

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def main():
    st.title("Photo Capture Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Persistent state across reruns
    if 'show_camera' not in st.session_state:
        st.session_state.show_camera = False    

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(placeholder="Type 'make photo' to capture an image."):

        # Check if user wants to make a photo
        if "make photo" in prompt.lower():
            st.session_state.show_camera = True
        else:
            st.session_state.show_camera = False
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                response = st.write_stream(response_generator())
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    if st.session_state.show_camera:
        # Camera input widget
        image = st.camera_input("Take a picture")
        if image is not None:
            st.image(image, caption='Captured Image')

if __name__ == "__main__":
    main()
