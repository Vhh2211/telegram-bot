import requests
import time
import json
from datetime import datetime, timedelta

# ================= CONFIG =================
TOKEN = "8687534018:AAEKaa-M0ZV74evpRWCX-6Rb4RPneKqOStE"
CHAT_ID = "6366949018"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ================= TIME =================
vn_offset = timedelta(hours=7)

def now():
    return datetime.utcnow() + vn_offset

# ================= SEND =================
def send(msg):
    try:
        requests.post(BASE_URL, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        print("✅", msg[:40])
    except Exception as e:
        print("❌", e)

# ================= STORAGE =================
FILE = "stats.json"

def load():
    try:
        return json.load(open(FILE, "r"))
    except:
        return {
            "xp": 0,
            "level": 1,
            "streak": 0,
            "miss": {},
            "done": {},
            "hard": 0
        }

def save(data):
    json.dump(data, open(FILE, "w"))

data = load()

# ================= SCHEDULE =================
schedule = {
    "05:30": "🌞 Dậy + uống nước",
    "05:45": "🍌 Pre-workout",
    "06:00": "🏋️ TẬP NGAY",
    "07:15": "🍳 Ăn sáng",
    "09:00": "🔥 Deep Work",
    "12:00": "🍱 Ăn trưa",
    "12:10": "🍱 cc è",
    "18:00": "🍽️ Ăn tối",
    "23:00": "😴 Ngủ"
}

# ================= AI (RULE-BASED) =================
def brain():
    miss_total = sum(data["miss"].values())

    if miss_total >= 3:
        data["hard"] = 1
    else:
        data["hard"] = 0

# ================= XP SYSTEM =================
def reward(ok):
    if ok:
        data["xp"] += 10
        data["streak"] += 1
    else:
        data["xp"] -= 5
        data["streak"] = 0

    if data["xp"] < 0:
        data["xp"] = 0

    data["level"] = data["xp"] // 100 + 1

# ================= STATE =================
last_sent = {}
last_alert = {}
current_day = now().day

print("👑 GOD SYSTEM STARTED")
send("👑 GOD SYSTEM ONLINE")

# ================= LOOP =================
while True:
    try:
        t = now()
        hm = t.strftime("%H:%M")

        # reset ngày
        if t.day != current_day:
            data = load()
            current_day = t.day

        brain()

        for time_key, task in schedule.items():

            key = f"{current_day}_{time_key}"

            # ================= TASK EXEC =================
            if hm == time_key and last_sent.get(key) != hm:

                msg = f"📌 {task}"

                if data["hard"]:
                    msg = "🔥 HARD MODE\n" + msg

                send(msg)

                last_sent[key] = hm
                reward(True)

        # ================= MISS CHECK =================
        for time_key in schedule:

            key = f"{current_day}_{time_key}"

            if hm > time_key and last_sent.get(key) != time_key:

                if not last_alert.get(key):

                    send(f"🔔 MISS TASK: {time_key}")
                    data["miss"][str(current_day)] = data["miss"].get(str(current_day), 0) + 1
                    last_alert[key] = True

                    reward(False)

        save(data)

        time.sleep(2)

    except Exception as e:
        print("🔥 ERROR:", e)
        time.sleep(5)
