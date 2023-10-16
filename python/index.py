from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mangum import Mangum
from routes.index import (
    user,
    sales_target,
    auth,
    health_check,
    service_waiting_list,
)

from config.index import Base, engine

app = FastAPI()

# add Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

handler = Mangum(app)

app.include_router(user)
app.include_router(sales_target)
app.include_router(auth)
app.include_router(health_check)
app.include_router(service_waiting_list)
