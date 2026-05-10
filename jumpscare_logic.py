import time
import random

JUMPSCARE_TRIGGER_TIME = 5.0  # ทำหน้าค้างไว้นานกี่วินาทีถึงจะโดน
JUMPSCARE_DISPLAY_DURATION = 2.0  # รูปผีจะโชว์ค้างไว้นานแค่ไหน

class JumpscareManager:
    def __init__(self):
        self.last_expression = None
        self.start_time = 0
        self.is_active = False
        self.jumpscare_start_time = 0
        self.current_jumpscare_image = "assets\jumscea.jpg" # รูปที่ใช้แกล้ง

    def check_jumpscare(self, current_expression):
        now = time.time()

        # ถ้าหน้าเปลี่ยน ให้รีเซ็ตเวลาใหม่
        if current_expression != self.last_expression:
            self.last_expression = current_expression
            self.start_time = now
            return False

        # ถ้าทำหน้าเดิมค้างไว้เกินเวลา และยังไม่ได้เข้าสู่สถานะ Jumpscare
        if not self.is_active and (now - self.start_time) > JUMPSCARE_TRIGGER_TIME:
            if random.random() < 0.3: 
                self.is_active = True
                self.jumpscare_start_time = now
                return True

        # เช็คว่าหมดเวลาโชว์รูป Jumpscare หรือยัง
        if self.is_active:
            if (now - self.jumpscare_start_time) > JUMPSCARE_DISPLAY_DURATION:
                self.is_active = False
            return True # ยังคงแสดงผล Jumpscare อยู่

        return False

    def get_opacity(self):
        """ คำนวณความโปร่งใสให้ค่อยๆ หายไป (Fade out) """
        if not self.is_active:
            return 0
        
        elapsed = time.time() - self.jumpscare_start_time
        # คำนวณค่าจาก 1.0 -> 0.0
        opacity = max(0, 1.0 - (elapsed / JUMPSCARE_DISPLAY_DURATION))
        return opacity