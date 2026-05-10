import cv2
import mediapipe as mp
import numpy as np
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from discord_helper import DiscordMemeTracker
import winsound
import mem_logic as meme

model_path = 'face_landmarker.task'

# ตรวจสอบว่ามีไฟล์โมเดลไหม ถ้าไม่มีจะแจ้งเตือน
if not os.path.exists(model_path):
    print(f"Error: ไม่พบไฟล์ {model_path} กรุณาดาวน์โหลดมาวางในโฟลเดอร์ก่อนรัน")
    exit()

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True, # แก้ชื่อตัวแปรตรงนี้ครับ
    num_faces=1
)

# สร้างตัวตรวจจับ (Detector)
detector = vision.FaceLandmarker.create_from_options(options)

def main():
    cam = cv2.VideoCapture(0)
    webhook_url = "ใส่ webhook discord"
    discord_bot = DiscordMemeTracker(webhook_url)
    prev_image_path = "assets/larry.jpeg"

    while cam.isOpened():
        ret, frame = cam.read()

        if not ret:
            break
        frame = cv2.flip(frame, 1)
        # ค่า default
        cat_image_path = "assets/larry.jpeg"
        # =========================
        # MediaPipe Detection
        # =========================
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )
        detection_result = detector.detect(mp_image)
        # Meme Detection
        if detection_result.face_landmarks:
            face_points = detection_result.face_landmarks[0]
            cat_image_path = meme.detect_meme(face_points)
            caption = meme.get_caption(cat_image_path)

            # เล่นเสียงเมื่อ meme เปลี่ยน
            if (
                cat_image_path != prev_image_path and
                cat_image_path != "assets/larry.jpeg"
            ):
                winsound.PlaySound(
                    "assets/meow.wav",
                    winsound.SND_FILENAME |
                    winsound.SND_ASYNC
                )
            prev_image_path = cat_image_path
        else:
            caption = ""

        discord_bot.check_and_send(cat_image_path)
        # Caption Overlay
        cv2.putText(
            frame,
            caption,
            (30, 50),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (255,255,255),
            2
        )
        # Webcam Display
        cv2.imshow(
            'Face Detection (Original)',
            frame
        )
        cat_img = cv2.imread(cat_image_path)
        if cat_img is not None:
            cat_img = cv2.resize(
                cat_img,
                (640, 480)
            )
            cv2.imshow(
                "Meme Display",
                cat_img
            )
        else:
            blank = np.zeros(
                (480, 640, 3),
                dtype=np.uint8
            )
            cv2.putText(
                blank,
                f"File Missing: {cat_image_path}",
                (50, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )
            cv2.imshow(
                "Meme Display",
                blank
            )
        # ESC เพื่อปิดโปรแกรม
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # =========================
    # Cleanup
    # =========================
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        print("\n[!] ปิดโปรแกรมโดยผู้ใช้งาน")

        try:
            cv2.destroyAllWindows()

        except:
            pass