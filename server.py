import uvicorn
from fastapi import FastAPI
from bot import bot, dp  # Импортируем бота

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Бот работает!"}

@app.on_event("startup")
async def on_startup():
    import asyncio
    asyncio.create_task(dp.start_polling(bot))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
