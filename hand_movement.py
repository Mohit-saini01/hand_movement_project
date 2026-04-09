import cv2
import mediapipe as mp
import pyautogui
import os

# Optional: Path to open a folder (you can comment this out if not needed)
custom_folder_path = r"C:\Users\om\Desktop\MyImportantFolder"  # Change this if needed

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Webcam setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

screen_width, screen_height = pyautogui.size()
click_threshold = 30  # Distance between index and thumb to trigger click
clicked = False       # Prevent rapid repeated clicks
folder_opened = False # Prevent folder from opening multiple times

def open_custom_folder():
    if os.path.exists(custom_folder_path):
        os.startfile(custom_folder_path)
    else:
        print("❌ Folder path does not exist:", custom_folder_path)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Index and Thumb Tips
                index_finger = hand_landmarks.landmark[8]
                thumb = hand_landmarks.landmark[4]

                # Cursor Movement
                x = int(index_finger.x * screen_width)
                y = int(index_finger.y * screen_height)
                pyautogui.moveTo(x, y)

                # Gesture Detection (click)
                x_thumb = int(thumb.x * w)
                y_thumb = int(thumb.y * h)
                x_index = int(index_finger.x * w)
                y_index = int(index_finger.y * h)
                distance = ((x_index - x_thumb)**2 + (y_index - y_thumb)**2) ** 0.5

                if distance < click_threshold:
                    if not clicked:
                        print("🖱️ Click Gesture Detected: Performing mouse click!")
                        pyautogui.click()
                        
                        # Optional: Only open folder on first gesture
                        if not folder_opened:
                            open_custom_folder()
                            folder_opened = True
                        clicked = True
                else:
                    clicked = False  # Reset when fingers move apart

        cv2.imshow("Hand Mouse Control + Click", image)

        # Exit on ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
