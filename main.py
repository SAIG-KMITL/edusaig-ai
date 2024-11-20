if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", port=8000, reload=True, host="127.0.0.1")