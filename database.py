import re
import datetime
import motor.motor_asyncio
from configs import DATABASE_URL, DATABASE_NAME

# ---------- MongoDB Setup ----------
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]
tmv_collection = db["Tamilmv"]

# ---------- TamilMV Entry Helper ----------
async def add_tmv(file_name: str, file_url: str, magnet: str, size_mb: float = 0, category: str = "Movies"):
    """
    Store processed TamilMV torrent entry into MongoDB with Category.
    """
    try:
        exists = await tmv_collection.find_one({"file_url": file_url})
        
        if not exists:
            await tmv_collection.insert_one({
                "file_name": file_name,
                "file_url": file_url,
                "magnet": magnet,
                "size_mb": size_mb,
                "category": category, 
                "upload_date": datetime.date.today().isoformat()
            })
            print(f"💾 Added to DB [{category}]: {file_name}")
        else:
            print(f"⏩ Already exists in DB: {file_name}")
    except Exception as e:
        print(f"⚠️ DB insert failed for {file_name}: {e}")

async def is_tmv_exist(file_url: str):
    """Check if the torrent already processed."""
    result = await tmv_collection.find_one({"file_url": file_url})
    return True if result else False
