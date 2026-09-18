import os
import asyncio
from pyrogram import Client, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# তথ্যগুলো এনভায়রনমেন্ট ভেরিয়েবল থেকে আসবে (Koyeb-এ সেট করবো)
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PRIVATE_CHANNEL = int(os.environ.get("PRIVATE_CHANNEL"))
PUBLIC_CHANNEL = int(os.environ.get("PUBLIC_CHANNEL"))
POST_TIME = os.environ.get("POST_TIME", "10:00") # ডিফল্ট সকাল ১০টা

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def post_video():
    async with app:
        print("🔍 ভিডিও খোঁজা হচ্ছে...")
        # প্রাইভেট চ্যানেল থেকে মেসেজগুলো দেখা (পুরানো থেকে নতুন)
        async for message in app.get_chat_history(PRIVATE_CHANNEL, limit=100, reverse=True):
            if message.video or message.document:
                # পাবলিক চ্যানেলে ভিডিও পাঠানো
                await message.copy(chat_id=PUBLIC_CHANNEL)
                print(f"✅ ভিডিও পোস্ট হয়েছে: {message.id}")
                
                # প্রাইভেট চ্যানেল থেকে ডিলিট করে দেওয়া যাতে পরে আর না পাঠায়
                await message.delete()
                break # একটা পাঠানো হয়ে গেলে লুপ বন্ধ

async def main():
    scheduler = AsyncIOScheduler(timezone="Asia/Dhaka")
    hour, minute = POST_TIME.split(":")
    
    # প্রতিদিন নির্দিষ্ট সময়ে রান হবে
    scheduler.add_job(post_video, "cron", hour=int(hour), minute=int(minute))
    scheduler.start()
    
    print(f"🤖 বট চালু হয়েছে! প্রতিদিন {POST_TIME} টায় পোস্ট হবে।")
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(main())
