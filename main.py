import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Laundry Management System...")
    print("📂 Notice: Architecture has been upgraded. App is now in the 'app/' directory.")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)