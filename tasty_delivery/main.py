import uvicorn

if __name__ == '__main__':
    print("MAIN")
    uvicorn.run("server:app", reload=True, port=8000)
