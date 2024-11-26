import cv2
import numpy as np
import mediapipe as mp
from pynput.mouse import Controller, Button

# Initialize MediaPipe Hands and mouse controller
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mouse = Controller()

# Define the screen resolution for mapping
SCREEN_WIDTH = 1920  # Update according to your screen resolution
SCREEN_HEIGHT = 1080

# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Frame not captured.")
            break

        # Flip the frame horizontally for natural interaction
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract landmark positions
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Convert normalized landmarks to pixel positions
                index_x, index_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

                # Draw circles on fingertips
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)
                cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255), -1)

                # Map index finger tip to screen coordinates
                screen_x = np.interp(index_x, [0, w], [0, SCREEN_WIDTH])
                screen_y = np.interp(index_y, [0, h], [0, SCREEN_HEIGHT])

                # Move the mouse
                mouse.position = (screen_x, screen_y)

                # Check if thumb and index are close enough for a "click"
                distance = np.linalg.norm(np.array([thumb_x - index_x, thumb_y - index_y]))
                if distance < 20:  # Threshold for a "click"
                    mouse.click(Button.left)

        # Display the frame
        cv2.imshow('AI Virtual Mouse', frame)

        # Exit the program on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
