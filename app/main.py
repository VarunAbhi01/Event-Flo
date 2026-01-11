# this is to build application main file

# fastapi is a modern, fast (high-performance) web framework for building APIs and setting communication btwn them, basically an application. 
from fastapi import FastAPI

# Importing the router defined in events module to include its endpoints in the main application, we set it as events_router to avoid confusion when we also import routers for other domains like users,payments etc in future.
from app.api.events import router as events_router

# Creating an instance of FastAPI as our main web application
app = FastAPI(title="EventFlo")

# attaches all routes defined in events_router to the main FastAPI app with the "/events" prefix to path.
app.include_router(events_router, prefix="/events")