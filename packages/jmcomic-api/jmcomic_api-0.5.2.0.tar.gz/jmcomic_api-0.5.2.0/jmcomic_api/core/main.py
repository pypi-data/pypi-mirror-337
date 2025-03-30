import asyncio
import gc
import uuid
from contextlib import asynccontextmanager
from typing import Callable, Optional

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRoute

from jmcomic_api._utils.env import dev_mode
from jmcomic_api._utils.exception import (
    add_exception_handler,
)

app = FastAPI(debug=dev_mode)
app = add_exception_handler(app=app)


@asynccontextmanager
async def lifespan():
    gc.enable()


def add_temporary_route(path: str, route_func: Callable, timeout: Optional[int] = 60):
    """
    添加一个临时路由（自动删除且不在文档显示）
    :param path: 路由路径
    :param route_func: 路由处理函数
    :param timeout: 超时时间（秒），超过该时间路由自动关闭
    """
    endpoint_name = f"temporary_route_{uuid.uuid4().hex}"
    temporary_router = APIRouter()
    timeout_task = None  # 用于存储超时任务的引用

    if timeout is not None:

        async def remove_after_timeout():
            await asyncio.sleep(timeout)
            # 查找并删除路由
            routes_to_remove = [
                route
                for route in app.router.routes
                if isinstance(route, APIRoute) and route.name == endpoint_name
            ]
            for route in routes_to_remove:
                try:
                    app.router.routes.remove(route)
                except ValueError:
                    pass  # 路由可能已被删除

        timeout_task = asyncio.create_task(remove_after_timeout())

    @temporary_router.get(path, name=endpoint_name, include_in_schema=False)
    async def temporary_route(request: Request):
        nonlocal timeout_task

        try:
            response = await route_func()
        finally:
            # 无论处理函数是否异常都执行删除
            routes_to_remove = [
                route
                for route in app.router.routes
                if isinstance(route, APIRoute) and route.name == endpoint_name
            ]
            for route in routes_to_remove:
                try:
                    app.router.routes.remove(route)
                except ValueError:
                    pass

            # 取消超时任务
            if timeout_task and not timeout_task.done():
                timeout_task.cancel()

        return response

    app.include_router(temporary_router)
    del temporary_router
    gc.collect()


async def root():
    return RedirectResponse(url="/docs")


app.add_api_route("/", root)
