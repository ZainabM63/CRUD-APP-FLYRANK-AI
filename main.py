from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def read_root():
    return {"name": " TASK API",
            "version":"1.0.0",
            "endpoints":["/tasks","/health","/docs"]}

@app.get("/health")
def health_check():
    return{"status":"ok"}
