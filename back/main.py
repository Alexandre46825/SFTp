from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, files, shares, friends, admin, users

app = FastAPI(title="SFTP Cloud", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,    prefix="/auth",    tags=["Auth"])
app.include_router(files.router,   prefix="/files",   tags=["Files"])
app.include_router(shares.router,  prefix="/shares",  tags=["Shares"])
app.include_router(friends.router, prefix="/friends", tags=["Friends"])
app.include_router(admin.router,   prefix="/admin",   tags=["Admin"])
app.include_router(users.router,   prefix="/users",   tags=["Users"])

@app.get("/")
def root():
    return {"message": "SFTP Cloud API is running"}