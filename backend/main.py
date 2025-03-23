from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from index_wrecker import generate_dummy_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/information")
async def get_information():
    return generate_dummy_data()
