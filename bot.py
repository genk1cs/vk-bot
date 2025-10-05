import os
import requests
from datetime import datetime

# === Настройки ===
VK_TOKEN = os.getenv("VK_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")  # Например: "-228456366"
POST_NUMBER = (datetime.now().day - 1) % 30 + 1  # 1–30

# Читаем текст поста
with open(f"content/{POST_NUMBER}.txt", "r", encoding="utf-8") as f:
    message = f.read()

# Загружаем фото в ВК
upload_url = requests.get(
    "https://api.vk.com/method/photos.getWallUploadServer",
    params={"access_token": VK_TOKEN, "v": "5.199", "group_id": OWNER_ID.lstrip("-")}
).json()["response"]["upload_url"]

with open(f"images/{POST_NUMBER}.jpg", "rb") as f:
    upload = requests.post(upload_url, files={"photo": f}).json()

photo = requests.post(
    "https://api.vk.com/method/photos.saveWallPhoto",
    data={
        "access_token": VK_TOKEN,
        "v": "5.199",
        "group_id": OWNER_ID.lstrip("-"),
        "photo": upload["photo"],
        "server": upload["server"],
        "hash": upload["hash"]
    }
).json()["response"][0]

attachment = f"photo{photo['owner_id']}_{photo['id']}"

# Публикуем пост
response = requests.post(
    "https://api.vk.com/method/wall.post",
    data={
        "access_token": VK_TOKEN,
        "v": "5.199",
        "owner_id": OWNER_ID,
        "message": message,
        "attachments": attachment
    }
)

print(f"✅ Пост №{POST_NUMBER} опубликован!")