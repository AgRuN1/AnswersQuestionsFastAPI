from datetime import datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class LoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        print(f'New request {request.method} {request.url} {datetime.now()}')
        response = await call_next(request)
        return response