import threading
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import user, hero, occurrence
from app.socket.handler import start_socket
from app.allocator import allocator
from app.core.settings import settings

app = FastAPI(
    # dependencies=[Depends(start_socket)]
)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

socket_handler_thread = threading.Thread(target=start_socket)
socket_handler_thread.daemon = True

allocator_thread = threading.Thread(target=allocator.main)
allocator_thread.daemon = True

socket_handler_thread.start()
allocator_thread.start()

app.include_router(user.router)
app.include_router(hero.router)
app.include_router(occurrence.router)

# if __name__ == "__main__":
    
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    

# @app.post("/importfile/", status_code=status.HTTP_201_CREATED)
