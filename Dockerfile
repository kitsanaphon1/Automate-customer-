# 1. ใช้ Python 3.11 แบบ slim เพื่อให้ Image มีขนาดเล็ก
FROM python:3.11-slim

# 2. ตั้งค่า Environment Variables เพื่อไม่ให้ Python สร้างไฟล์ .pyc และให้แสดง Log ทันที
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. กำหนดโฟลเดอร์ทำงานใน Container
WORKDIR /app

# 4. ติดตั้ง Dependencies สำหรับระบบที่จำเป็นในการรัน PostgreSQL Driver
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. ติดตั้ง Python Library
# Copy เฉพาะ requirements.txt มาก่อนเพื่อใช้ประโยชน์จาก Docker Cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Code ทั้งหมดในโฟลเดอร์ app เข้าไปที่ /app/app
COPY ./app ./app

# 7. เปิด Port 8000 สำหรับ FastAPI
EXPOSE 8000

# 8. สั่งรัน uvicorn โดยกำหนด host เป็น 0.0.0.0 เพื่อให้เข้าถึงจากภายนอก Container ได้
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]