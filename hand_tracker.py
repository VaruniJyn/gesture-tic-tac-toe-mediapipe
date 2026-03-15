import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

    def get_index_finger(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        h, w, _ = frame.shape
        index_position = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # Landmark 8 = index finger tip
                index_tip = hand_landmarks.landmark[8]

                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                index_position = (x, y)

                # draw landmarks
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame, index_position