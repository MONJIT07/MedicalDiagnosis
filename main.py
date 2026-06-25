from fastapi import FastAPI


app = FastAPI()
@app.get("/health")
def healthcheck():
    return {"message": "ok"}
def main():
    print("Hello from medrag!")


if __name__ == "__main__":
    main()
