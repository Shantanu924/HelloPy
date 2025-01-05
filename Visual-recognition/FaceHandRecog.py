import cv2
import face_recognition as face
import mediapipe as mp
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

class Recognition:
   def __init__(self,root):
        self.root = root
        self.root.title("Facial and hand recognition")
        self.root.geometry("1000x800")

        self.video_label = Label(root)
        self.video_label.pack()
        
        self.start_btn = Button(root,text="Start", command=self.start_recog)
        self.start_btn.pack()
        self.stop_btn = Button(root,text="Stop", command=self.stop_recog)
        self.stop_btn.pack()

        self.cap = None
        self.runnimg = False
    
    def start_recog(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.recog()
    
    def stop_recog(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image='')

    def recog(self):
        if not self.running:
            return
        _,frame = self.cap.read()
        if frame is not None:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_locat = face.face_locations(frame_rgb)
            for top, right, bottom, left in face_locat:
                cv2.rectangle(frame, (left,top),(right,bottom),(0,255,0),2)
            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(10,self.recog)

if __name__ == "__main__":
    root = tk.Tk()
    app = Recogition(root)
    root.mainloop()