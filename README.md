# 🎮 Gesture Controlled Tic Tac Toe AI

A computer vision based Tic Tac Toe game where the player uses **hand gestures** to control the game.  
The system detects the **index finger using MediaPipe** and allows the user to play against an **AI opponent powered by the Minimax algorithm**.

This project combines **Computer Vision, AI, and Game Development** in one interactive application.

---

# 🚀 Features

✔ Hand gesture controlled cursor  
✔ Hover based interaction (no mouse or keyboard required)  
✔ AI opponent using **Minimax algorithm**  
✔ Multiple difficulty levels  
✔ Animated neon UI grid  
✔ Hover progress indicator  
✔ Win detection and animated win line  
✔ Restart gesture system  
✔ Menu system with difficulty selection  

---

# 🧠 How It Works

The system uses **MediaPipe Hand Tracking** to detect the user's hand and identify the position of the index finger.

Workflow:

1. Webcam captures the live video feed
2. MediaPipe detects hand landmarks
3. The **index finger tip coordinates** are extracted
4. The finger acts as a **cursor on the game board**
5. Hovering on a grid cell for **1 second confirms the move**
6. The player places **X**
7. The computer responds with **O using Minimax AI**

---

# 🕹 Game Controls (Gesture Based)

### Start Menu
Hover over options to select.

Options:
- Start Game
- Change Difficulty
- Exit

### During Gameplay

Move your index finger over a cell and hold for **1 second** to place a move.

### After Game Ends

Gesture actions:

| Gesture | Action |
|------|------|
Hold **center cell** | Restart game |
Hold **bottom-right cell** | Return to menu |

---

# 🤖 AI System

The computer opponent uses the **Minimax algorithm** to determine the best move.

Difficulty levels:

| Difficulty | Behaviour |
|------|------|
Easy | Random moves |
Medium | 50% Random + 50% Minimax |
Hard | 90% Minimax + 10% Random |

This makes the AI **challenging but still beatable**.

---

# 🧰 Tech Stack

| Technology | Purpose |
|------|------|
Python | Core programming language |
MediaPipe | Hand tracking |
OpenCV | Webcam processing |
Pygame | Game interface and animations |
Minimax Algorithm | AI opponent logic |

---

# ▶️ Running the Project

1. Clone the repository

git clone https://github.com/VaruniJyn/gesture-tic-tac-toe-mediapipe.git

2. Navigate into the project directory

cd gesture-tic-tac-toe-mediapipe

3. Install required dependencies

pip install -r requirements.txt

4. Run the application

python main.py

⚠️ Note:
Make sure your webcam is connected because the game uses hand gestures detected through the camera.
