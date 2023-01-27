from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """Main function of the web application
    
    Returns:
        List -- Hello World
    """
    return {"Hello": "World"}

@app.get("/tyler")
def tylers_route():
    return "Tyler was here"