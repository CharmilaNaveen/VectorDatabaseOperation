from vectordb_routes import app

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn as the ASGI server
    uvicorn.run(app, host="localhost", port=8000)
