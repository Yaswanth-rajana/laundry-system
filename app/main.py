from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.orders import router

app = FastAPI(title="Laundry Management System", description="AI-First Development")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Laundry Management System API",
        "docs": "/docs",
        "endpoints": ["/orders", "/dashboard", "/orders/{id}/status", "/orders/{id}/history"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
