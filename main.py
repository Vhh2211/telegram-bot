import requests
import time
import random
from datetime import datetime, timedelta

# ================= CONFIG =================
TOKEN = "8687534018:AAEKaa-M0ZV74evpRWCX-6Rb4RPneKqOStE"
CHAT_ID = "6366949018"

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ================= TIME =================
vn_offset = timedelta(hours=7)

def now_vn():
    return datetime.utcnow() + vn_offset

# ================= SEND =================
def send(msg):
    try:
        requests.post(
            BASE_URL,
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
        print("✅ SENT:", msg[:40])
    except Exception as e:
        print("❌ EXCEPTION:", e)

# ================= FOOD SYSTEM (UPGRADED) =================
breakfasts = [
    "Bánh mì trứng + sữa",
    "Xôi gà + cà phê đen",
    "Yến mạch + chuối + sữa chua",
    "Bún bò nhẹ buổi sáng",
    "Trứng ốp la + bánh mì + trái cây"
]

lunches = [
    "Cơm gà + rau luộc + canh",
    "Cơm cá + rau xào + trứng",
    "Bún thịt nướng + rau nhiều",
    "Cơm thịt nạc + canh rau",
    "Phở bò + thêm trứng"
]

dinners = [
    "Cơm cá + rau luộc (ít dầu)",
    "Ức gà + khoai lang + salad",
    "Trứng + rau + cơm ít",
    "Phở nhẹ / bún nhẹ",
    "Cá hồi (hoặc cá thường) + rau xanh"
]

snacks = [
    "Chuối / táo",
    "Sữa chua không đường",
    "Hạt điều / hạnh nhân",
    "Protein nhẹ (trứng)",
]

# ================= GYM SYSTEM (UPGRADED) =================
workouts = ["PUSH", "PULL", "LEGS"]

def get_workout(day):
    w = workouts[day % 3]

    if w == "PUSH":
        return """💪 PUSH DAY
- Bench Press: 4x8-10
- Incline Dumbbell: 3x10
- Shoulder Press: 4x10
- Lateral Raise: 3x15
- Triceps Pushdown: 3x12
🔥 Focus: ngực + vai + tay sau"""

    if w == "PULL":
        return """🧲 PULL DAY
- Lat Pulldown: 4x10
- Barbell Row: 4x8-10
- Seated Row: 3x12
- Biceps Curl: 3x12
- Hammer Curl: 3x12
🔥 Focus: lưng + tay trước"""

    return """🦵 LEGS DAY
- Squat: 4x8-10
- Leg Press: 4x12
- Leg Curl: 3x12
- Calf Raise: 4x15
🔥 Focus: chân + core"""

# ================= LIFESTYLE SYSTEM =================
life_tips = [
    "💧 Uống nước đều mỗi 60–90 phút",
    "🧠 Làm việc 50 phút nghỉ 10 phút (focus mode)",
    "📵 Tránh điện thoại trong deep work",
    "🚶 Đi bộ 5–10 phút sau mỗi bữa ăn",
    "😴 Ngủ đủ 7–8 tiếng"
]

# ================= SCHEDULE =================
schedule = {
    "05:30": "🌞 Dậy + uống nước",
    "05:45": "🍌 Pre-workout",
    "06:00": "🏋️ TẬP NGAY",
    "07:15": "🍳 Ăn sáng",
    "08:30": "🧠 Reset + chuẩn bị đầu óc",
    "09:00": "🔥 Deep Work 1",
    "10:30": "💧 Uống nước + nghỉ ngắn",
    "11:30": "🍵 Nghỉ nhẹ",
    "12:00": "🍱 Ăn trưa",
    "12:16": "🍱 test lần cuối",
    "13:00": "⚙️ Deep Work 2",
    "15:00": "💧 Uống nước",
    "15:15": "🧠 Work nhẹ / edit",
    "17:00": "⛔ Kết thúc công việc",
    "17:30": "🍳 Nấu cơm tối",
    "18:00": "🍽️ Ăn tối",
    "20:00": "📚 Học kiến thức mới",
    "22:30": "💧 Uống nước",
    "23:00": "😴 Ngủ"
}

# ================= STATE =================
sent_today = set()
current_day = now_vn().day

print("🚀 BOT RUNNING")
send("🚀 BOT ONLINE")

# ================= MAIN LOOP =================
while True:
    now_dt = now_vn()
    now = now_dt.strftime("%H:%M")

    if now_dt.day != current_day:
        sent_today.clear()
        current_day = now_dt.day

    for t in schedule:

        if now == t and t not in sent_today:

            msg = schedule[t]

            # ================= FOOD UPGRADE =================
            if t == "07:15":
                msg = "🍳 Ăn sáng\n👉 " + random.choice(breakfasts)

            elif t == "12:00":
                msg = "🍱 Ăn trưa\n👉 " + random.choice(lunches)

            elif t == "18:00":
                msg = "🍽️ Ăn tối\n👉 " + random.choice(dinners)

            elif t == "10:30":
                msg = "💧 Nghỉ + snack\n👉 " + random.choice(snacks)

            elif t == "06:00":
                msg = "💀 Không tập = không có body\n" + get_workout(current_day)

            elif t == "08:30":
                msg = "🧠 RESET MINDSET\n👉 " + random.choice(life_tips)

            elif t == "20:00":
                msg = "📚 HỌC + PHÁT TRIỂN BẢN THÂN\n👉 " + random.choice(life_tips)

            send(msg)
            sent_today.add(t)

    time.sleep(1)
