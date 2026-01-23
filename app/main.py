from fastapi import FastAPI
from app.core.config import APP_NAME
from app.core.config_logging import logger
from app.exceptions import http_exception_handler, general_exception_handler
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.routes import userroutes  # import auth routes

from app.routes import task_routes  ,role_routes, comment_route, actovity_routes



app = FastAPI(title = APP_NAME)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException,http_exception_handler)          
app.add_exception_handler(RequestValidationError,http_exception_handler)  
app.add_exception_handler(Exception, general_exception_handler) 

app.include_router(userroutes.router)
app.include_router(task_routes.router)
app.include_router(role_routes.router)
app.include_router(comment_route.router)
app.include_router(actovity_routes.router)
@app.on_event("startup")
def startup_event():
    logger.info("Application starting up")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("application shutting down")

@app.get("/health")
def health_check():
    logger.info("Health endpoint called")
    return {"status":"ok"}
