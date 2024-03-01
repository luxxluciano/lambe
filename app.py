import streamlit as st
from streamlit_webrtc import VideoTransformerBase, WebRtcMode, webrtc_streamer
import requests

# Define FastAPI endpoint
FASTAPI_ENDPOINT = "http://localhost:8000"  # Update with your FastAPI endpoint

# Function to send image to WordPress CMS via FastAPI
def send_to_wordpress(image):
    response = requests.post(f"{FASTAPI_ENDPOINT}/send_to_wordpress", files={"image": image})
    if response.status_code == 200:
        return True
    else:
        return False

# Define video transformer class
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Display the captured frame
        st.image(frame, channels="BGR")

        # Check if user approves the captured image
        if st.button("Approve"):
            return frame
        else:
            return None

# Main function for Streamlit app
def main():
    # Streamlit app configuration
    st.set_page_config(
        page_title="Camera App",
        page_icon="📷",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Title and instructions
    st.title("Camera App")
    st.write("Touch the screen to take a photo.")

    # WebRTC streamer to access camera
    webrtc_ctx = webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=VideoTransformer,
        async_transform=True,
    )

    # Check if photo is approved and send to WordPress
    if webrtc_ctx.video_transformer:
        image = webrtc_ctx.video_transformer.get_image()
        if image is not None:
            if send_to_wordpress(image):
                st.success("Photo sent to WordPress successfully!")
            else:
                st.error("Failed to send photo to WordPress.")

if __name__ == "__main__":
    main()
