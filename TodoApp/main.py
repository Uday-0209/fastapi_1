from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

#routers are created for scalability and maintainability
app.include_router(auth.router)

app.include_router(todos.router)


