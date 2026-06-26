from fastapi import FastAPI
from routes.summarize import router as summarize_router
from database import engine , Base
import models

from fastapi.responses import JSONResponse #exception handling
from fastapi import Request

from slowapi import Limiter, _rate_limit_exceeded_handler #to add limits a user can use this
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="YouTube Summarizer API",
    description="Summarizes YouTube videos using AI",
    version="1.0.0"
)

app.state.limiter = limiter #connecting limiter to your app
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



app.include_router(summarize_router)




@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": f"Something went wrong: {str(exc)}"
        }
    )

    
    