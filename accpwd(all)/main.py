from fastapi import FastAPI
from accpwd.accpwdController import router as accpwdControllerRouter


app = FastAPI()
app.include_router(accpwdControllerRouter, prefix="/user")



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}