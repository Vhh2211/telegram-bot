import requests
import time
from datetime import datetime

# ================= CONFIG =================
TOKEN = "8687534018:AAEKaa-M0ZV74evpRWCX-6Rb4RPneKqOStE"
CHAT_ID = "6366949018"

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ================= SEND =================
def send(msg):
    try:
        res = requests.post(
            BASE_URL,
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )

        if res.status_code == 200:
            print("✅ SENT:", msg[:40])
        else:
            print("⚠️ ERROR:", res.text)

    except Exception as e:
        print("❌ EXCEPTION:", e)


# ================= DATA =================
breakfasts = ["Bánh mì trứng", "Xôi gà", "Cháo thịt", "Bánh mì pate"]
lunches = ["Cơm gà", "Cơm cá", "Bún thịt nướng", "Cơm thịt trứng"]
dinners = ["Cơm cá", "Phở bò", "Bún bò", "Cơm trứng"]

workouts = ["PUSH", "PULL", "LEGS"]


def get_workout(day):
    w = workouts[day % 3]

    if w == "PUSH":
        return "💪 PUSH\nBench 4x10\nShoulder 4x10\nTricep 3x12"

    if w == "PULL":
        return "🧲 PULL\nLat 4x10\nRow 4x10\nBicep 3x12"

    return "🦵 LEGS\nSquat 4x10\nLeg 4x12\nCalf 4x15"


# ================= SCHEDULE =================
schedule = {
    "05:30": "🌞 Dậy + uống nước",
    "05:45": "🍌 Pre-workout",
    "06:00": "🏋️ TẬP NGAY",
    "07:15": "🍳 Ăn sáng",
    "08:30": "🧠 Chuẩn bị + reset đầu óc",
    "09:00": "🔥 Deep Work 1",
    "10:30": "💧 Uống nước",
    "11:30": "🍵 Nghỉ nhẹ",
    "11:52": "tao nè",
    "12:00": "🍱 Ăn trưa",
    "13:00": "⚙️ Deep Work 2",
    "15:00": "💧 Uống nước",
    "15:15": "🧠 Work nhẹ",
    "17:00": "⛔ Kết thúc công việc",
    "17:30": "🍳 Nấu cơm tối",
    "18:00": "🍽️ Ăn tối",
    "20:00": "📚 Học kiến thức mới",
    "22:30": "💧 Uống nước",
    "23:00": "😴 Ngủ"
}

# chống spam
sent_today = set()
current_day = datetime.now().day

print("🚀 BOT RUNNING")
send("🚀 BOT ONLINE")

# ================= MAIN LOOP =================
while True:
    now_dt = datetime.now()
    now = now_dt.strftime("%H:%M")

    # reset ngày mới
    if now_dt.day != current_day:
        sent_today.clear()
        current_day = now_dt.day
        print("🔄 RESET DAY")

    for t in schedule:

        if now == t and t not in sent_today:

            msg = schedule[t]

            # custom meal/workout
            if t == "07:15":
                msg = "🍳 Ăn sáng\n👉 " + breakfasts[current_day % len(breakfasts)]

            elif t == "12:00":
                msg = "🍱 Ăn trưa\n👉 " + lunches[current_day % len(lunches)]

            elif t == "18:00":
                msg = "🍽️ Ăn tối\n👉 " + dinners[current_day % len(dinners)]

            elif t == "06:00":
                msg = "💀 Không tập = không có body\n" + get_workout(current_day)

            send(msg)
            sent_today.add(t)

    time.sleep(1)
