from fastapi import FastAPI

app = FastAPI()

# This is a default endpoint
@app.get("/")
def hello():
    return {"message": "Hello World"}

# These are called endpoints
@app.get("/about")
def about():
    return {"message":"This is why I love learning, so many things to learn."}

#Using /docs in the opened link will open an interactive version of all the endpoints you have created. 