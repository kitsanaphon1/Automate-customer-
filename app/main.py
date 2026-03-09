from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets
from . import models, schemas, database

# 1. เพิ่มระบบ Security
security = HTTPBasic()

# 2. ฟังก์ชันสำหรับเช็ค Username & Password
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    # เปลี่ยน username และ password เป็นค่าที่คุณต้องการที่นี่
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "password123")
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# สร้าง Table อัตโนมัติ
models.Base.metadata.create_all(bind=database.engine)

# 3. ใส่ dependencies=[Depends(authenticate)] เพื่อล็อกทั้ง API
app = FastAPI(
    title="ERP Customer Service API",
    description="API สำหรับจัดการข้อมูลลูกค้าในระบบ ERP (เชื่อมต่อ Postgres 15)",
    version="1.0.1",
    contact={
        "name": "Chosy",
        "url": "http://192.168.2.180",
    },
    dependencies=[Depends(authenticate)] 
)

# POST: สร้างลูกค้าใหม่
@app.post("/customers", 
          response_model=schemas.CustomerResponse,
          tags=["Customer Management"],
          summary="สร้างลูกค้าใหม่ลงในระบบ")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    """
    ใช้สำหรับเพิ่มข้อมูลลูกค้าใหม่:
    - **customer_code**: รหัสลูกค้า (ต้องไม่ซ้ำ)
    - **name**: ชื่อลูกค้า
    - **email**: อีเมล (ไม่บังคับ)
    """
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# GET: ดึงข้อมูลลูกค้าทั้งหมด
@app.get("/customers", 
         response_model=list[schemas.CustomerResponse],
         tags=["Customer Management"],
         summary="ดึงรายการลูกค้าทั้งหมด")
def read_customers(db: Session = Depends(database.get_db)):
    return db.query(models.Customer).all()