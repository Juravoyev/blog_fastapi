from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api import api_router

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

@app.middleware("http")
async def add_version_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Version"] = "1.0.0"
    return response

@app.middleware("http")
async def detect_browser(request: Request, call_next):
    user_agent = request.headers.get("user-agent", "")

    if "Postman" in user_agent:
        print("Diqqat: Dasturchi Postman orqali API ga kirdi!")

    response = await call_next(request)
    return response


# @app.middleware("http")
# async def maintenance_mode(request: Request, call_next):
#     return JSONResponse(
#         status_code=503,
#         content={
#             "message": "Kechirasiz, serverda texnik ishlar olib borilmoqda. 1 soatdan so'ng urinib ko'ring."
#         }
#     )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)