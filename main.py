from fastapi import FastAPI

"""
uvicorn main:app --reload 启动



"""
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}