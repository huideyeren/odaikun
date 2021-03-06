import uvicorn
from fastapi import Depends, FastAPI
from starlette.requests import Request

from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.topics import topics_router
from app.api.api_v1.routers.users import users_router
from app.core import config
from app.core.auth import get_current_active_user
from app.core.celery_app import celery_app
from app.db.session import SessionLocal

app = FastAPI(title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    db_session_middleware DB接続を生成する

    Args:
        request (Request): リクエスト
        call_next (Any): 次のリクエストを呼ぶ

    Returns:
        Any: レスポンス
    """
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root():
    """
    root APIのルートにアクセスしたときの処理

    Returns:
        dict: 「Hello World」というメッセージ
    """
    return {"message": "Hello World"}


@app.get("/api/v1/task")
async def example_task():
    """
    example_task サンプルタスク

    Returns:
        dict: 成功を表すメッセージ
    """
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])

    return {"message": "success"}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(
    topics_router,
    prefix="/api/v1",
    tags=["topics"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
