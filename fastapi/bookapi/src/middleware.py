from  fastapi import  FastAPI
from fastapi.requests import Request
import time
import logging

def register_middleware(app:FastAPI):

    @app.middleware('http')
    async def custom_logging(request:Request,call_next):
        start_time = time.time()
        print("Before",start_time)
        response = await  call_next(request)
        processing_time = time.time()
        print("After", processing_time)

        return  response


