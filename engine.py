import cv2
import mediapipe as mp
import numpy as np
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mem_logic as meme 
from jumpscare_logic import JumpscareManager 
from discord_helper import DiscordMemeTracker

def overlay_image(background, overlay_img, face_landmarks):
    """ ฟังก์ชันสำหรับแปะรูปผีลงบนใบหน้าตามพิกัด Landmarks """
    h, w, _ = background.shape
    
    # คำนวณขอบเขตใบหน้าจาก Landmarks
    all_x = [lm.x * w for lm in face_landmarks]
    all_y = [lm.y * h for lm in face_landmarks]
    
    min_x, max_x = int(min(all_x)), int(max(all_x))
    min_y, max_y = int(min(all_y)), int(max(all_y))
    
    face_w = max_x - min_x
    face_h = max_y - min_y

    # ปรับขนาดรูปผี
    padding_w = int(face_w * 0.5)
    padding_h = int(face_h * 0.5)
    new_w = face_w + (padding_w * 2)
    new_h = face_h + (padding_h * 2)
    
    if new_w <= 0 or new_h <= 0: return background
    
    resized_ghost = cv2.resize(overlay_img, (new_w, new_h))

    start_x = min_x - padding_w
    start_y = min_y - padding_h

    # แปะรูปลงบนเฟรม
    for i in range(new_h):
        for j in range(new_w):
            if start_y + i >= h or start_x + j >= w or start_y + i < 0 or start_x + j < 0:
                continue
            
            pixel = resized_ghost[i, j]
            # แปะทับพิกเซลเดิม
            background[start_y + i, start_x + j] = pixel

    return background

class CatoEngine:
    def __init__(self):
        # Setup MediaPipe
        model_path = 'face_landmarker.task'
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)
        
        # Setup Jumpscare Manager 
        self.js_manager = JumpscareManager()
        self.discord_bot = None

    def set_webhook(self, url):
        self.discord_bot = DiscordMemeTracker(url)

    def process_frame(self, frame):
        # เตรียมภาพ
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # สแกนหน้า
        detection_result = self.detector.detect(mp_image)
        
        cat_image_path = "assets/larry.jpeg"
        caption = "นิ่งสงบ"
        js_active = False
        js_opacity = 0

        if detection_result.face_landmarks:
            face_points = detection_result.face_landmarks[0]
            
            # ตรวจจับมีมจากหน้า
            cat_image_path = meme.detect_meme(face_points)
            caption = meme.get_caption(cat_image_path)

            # เช็ค Jumpscare 
            # ส่ง cat_image_path เข้าไปเช็คว่าทำหน้าเดิมค้างไว้นานไหม
            js_active = self.js_manager.check_jumpscare(cat_image_path)
            js_opacity = self.js_manager.get_opacity()

            # 3. ส่ง Discord 
            if js_active:
                ghost_img = cv2.imread(self.js_manager.current_jumpscare_image)
                if ghost_img is not None:
                    # เปลี่ยนจาก RGB กลับเป็น BGR ชั่วคราวเพื่อ OpenCV
                    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                    # แปะผีลงบนใบหน้า
                    bgr_frame = overlay_image(bgr_frame, ghost_img, face_points)
                    # แปลงกลับเป็น RGB เพื่อแสดงผลบน Streamlit
                    rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
                    caption = "WAAAAAAH! 👻"

            # 4. ส่งข้อมูลเข้า Discord
            if self.discord_bot:
                self.discord_bot.check_and_send(cat_image_path)

        return rgb_frame, cat_image_path, caption , js_active