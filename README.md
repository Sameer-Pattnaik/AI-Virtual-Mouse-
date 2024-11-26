# **AI Virtual Mouse Using OpenCV - Documentation**

## **Introduction**
The AI Virtual Mouse is a Python program that enables users to control the mouse pointer and perform click actions using hand gestures detected via a webcam. This program leverages OpenCV for real-time video capture, MediaPipe for hand tracking, and the `pynput` library to control mouse actions.

---

## **Features**
1. **Hand Gesture Recognition**: Tracks the position of your hand and fingers.
2. **Mouse Pointer Movement**: Maps the index finger's movement to screen coordinates.
3. **Click Action**: Simulates a left-click when the thumb and index finger tips are brought close together.
4. **Real-Time Processing**: Processes hand gestures in real-time for a seamless experience.

---

## **Prerequisites**
### **Hardware**
- A computer with a webcam.
- A screen resolution (e.g., 1920x1080) that you can configure in the program.

### **Software**
1. Python 3.6+
2. Libraries:
   - OpenCV
   - MediaPipe
   - pynput
   - NumPy

Install the required libraries using the following command:
```bash
pip install opencv-python mediapipe pynput numpy
```

---

## **How It Works**
1. The webcam captures video frames in real-time.
2. MediaPipe detects hand landmarks and identifies the positions of the index finger and thumb.
3. The index finger's tip is used to control the mouse pointer, mapped to the screen resolution.
4. When the thumb and index finger tips come close enough, a left-click is simulated using `pynput`.

---

## **Code Overview**

### **1. Import Required Libraries**
The program imports the following:
- `cv2` (OpenCV) for video capture and processing.
- `mediapipe` for hand tracking.
- `pynput.mouse` to control mouse actions.
- `numpy` for numerical computations.

### **2. Initialize Components**
- Initialize MediaPipe's `Hands` solution for hand detection.
- Create a `pynput.mouse.Controller` object to control the mouse.

### **3. Webcam Input**
The webcam is accessed using OpenCV:
```python
cap = cv2.VideoCapture(0)
```

### **4. Hand Detection**
MediaPipe processes the webcam frames to detect hand landmarks:
```python
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:
    results = hands.process(rgb_frame)
```

### **5. Mouse Pointer Mapping**
The index finger tip's position is normalized and mapped to the screen resolution:
```python
screen_x = np.interp(index_x, [0, w], [0, SCREEN_WIDTH])
screen_y = np.interp(index_y, [0, h], [0, SCREEN_HEIGHT])
mouse.position = (screen_x, screen_y)
```

### **6. Click Action**
When the distance between the thumb and index finger tips is below a threshold, a left-click is simulated:
```python
distance = np.linalg.norm(np.array([thumb_x - index_x, thumb_y - index_y]))
if distance < 20:
    mouse.click(Button.left)
```

### **7. Exit Mechanism**
Press `q` to quit the program.

---

## **Usage Instructions**
1. **Run the Program**:
   - Save the code as a `.py` file and run it in a Python environment:
     ```bash
     python ai_virtual_mouse.py
     ```

2. **Control the Mouse**:
   - Move your index finger to control the cursor position.
   - Bring your thumb and index finger tips close together to simulate a left-click.

3. **Exit the Program**:
   - Press `q` on your keyboard to stop the program.

---

## **Configuration**
### **Screen Resolution**
Update the `SCREEN_WIDTH` and `SCREEN_HEIGHT` variables to match your monitor's resolution:
```python
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
```

### **Click Sensitivity**
Adjust the `distance` threshold to make the click action more or less sensitive:
```python
if distance < 20:  # Lower values make it more sensitive
```

---

## **Troubleshooting**
1. **Cursor Doesn't Move**:
   - Ensure your webcam is properly connected and functional.
   - Keep your hand visible and steady in the camera's frame.

2. **Unintended Clicks**:
   - Increase the click sensitivity threshold:
     ```python
     if distance < 30:
     ```

3. **Performance Issues**:
   - Use a well-lit environment for better hand detection.
   - Close other programs that might be using the webcam.

---

## **Limitations**
- Requires good lighting for accurate hand detection.
- Gesture recognition may vary with different hand sizes and positions.
- May not work smoothly on lower-resolution webcams.

---

## **Future Enhancements**
1. Add **right-click functionality** using a different gesture.
2. Implement **scrolling** using hand gestures.
3. Support for **multi-hand tracking**.
4. Enhance **accuracy** using advanced hand tracking algorithms.

---

## **Conclusion**
The AI Virtual Mouse program provides an innovative way to interact with your computer using natural hand gestures. With further optimization, it can serve as an effective touchless control system for various applications.
