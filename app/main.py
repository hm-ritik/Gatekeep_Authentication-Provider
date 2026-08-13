from fastapi import FastAPI

app=FastAPI(title="Auth Provider")

@app.get("/home")
async def health():
    return{
        "Message" : "Checking system"
    }
