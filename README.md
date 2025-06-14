# Webcam Movement Capture

## Description
A Python-based application using OpenCV and Streamlit to capture movement from a webcam. When distinct motion is detected, an image is saved and sent via email.

## Features
- Detects movement using frame comparison
- Captures and stores images when movement is detected
- Sends detected movement snapshots via email
- Displays the processed video stream with timestamps

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your_username/webcam-movement-capture.git
   cd webcam-movement-capture
   
## File Structure
- main.py: Runs the main application logic
- frame_processor.py: Handles frame simplification and movement detection
- send_email.py: Formats and sends email notifications
- requirements.txt: Lists dependencies
- images/: Stores captured movement images
- 
## Practical Applications
This project can be used for various real-world scenarios, such as:
- **Home Security**: Detects movement and sends alerts to monitor unusual activity.
- **Theft Prevention**: Captures images when motion is detected, providing evidence in case of unauthorized entry.
- **Pet Monitoring**: Tracks movement to check on pets while away.
- **Smart Automation**: Can be integrated with IoT devices for automated responses to movement events.