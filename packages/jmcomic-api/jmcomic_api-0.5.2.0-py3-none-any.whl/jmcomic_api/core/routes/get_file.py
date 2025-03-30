import base64
import os
from io import BytesIO
from typing import Dict, Literal

from fastapi import Query, Request
from fastapi.responses import (
    JSONResponse,
    StreamingResponse,
)

from jmcomic_api._utils.env import IMG_FORMAT
from jmcomic_api._utils.file import (
    GetCacheFilePath,
    encrypt_file,
    merge_images_to_file,
)
from jmcomic_api.core.main import add_temporary_route
from jmcomic_api.models.core.route import Route


class GetFile(Route):
    def __init__(self):
        self.method = ["GET"]
        self.path = "/get/file"
        self.time_out = 30

    def config(self, output_dir: str, time_out: int):
        self.output_dir = output_dir
        self.time_out = time_out

    async def route_def(
        self,
        request: Request,
        jm_id: int = Query(..., title="本子ID", description="本子ID"),
        file_type: Literal["pdf", "zip"] = Query(
            ..., title="文件格式", description="文件格式"
        ),
        file_pwd: str = Query(None, title="文件密码", description="文件密码"),
        return_method: Literal["from-data", "base64", "url"] = Query(
            "base64",
            title="返回方式",
            description="返回方式",
        ),
    ) -> JSONResponse:
        get_cache_path = GetCacheFilePath(self.output_dir, jm_id).get
        file_name = f"{jm_id}.{file_type}"
        return_data: Dict = {
            "code": 200,
            "status": "OK",
            "data": {
                "jm_id": jm_id,
                "file_name": file_name,
                "file_type": file_type,
                "file_pwd": file_pwd,
                "file": None,
            },
        }

        img_dir = get_cache_path(IMG_FORMAT.lower())
        if not os.path.exists(img_dir) or not os.listdir(img_dir):
            return JSONResponse(
                content={
                    "code": 400,
                    "status": "error",
                    "data": {
                        "msg": "图片未下载",
                        "log": "图片未下载",
                    },
                },
                status_code=400,
            )

        # 构建缓存文件路径
        file_dir = os.path.join(get_cache_path(file_type))
        file_path = os.path.join(file_dir, file_name)
        os.makedirs(file_dir, exist_ok=True)

        # 优先使用缓存文件
        if os.path.exists(file_path):
            # 从缓存文件读取
            with open(file_path, "rb") as f:
                file = BytesIO(f.read())
        else:
            # 收集需要合并的图片路径
            out_img_paths = []
            for chapter_data in os.listdir(img_dir):
                chapter_path = os.path.join(img_dir, chapter_data)
                if os.path.isdir(chapter_path):
                    for f in os.listdir(chapter_path):
                        if f.endswith(f".{IMG_FORMAT.lower()}"):
                            full_path = os.path.join(chapter_path, f)
                            out_img_paths.append(full_path)

            # 生成文件并写入缓存
            file = merge_images_to_file(out_img_paths, file_type)
            with open(file_path, "wb") as f:
                f.write(file.getvalue())
            file.seek(0)  # 重置指针以便后续读取

        # 文件加密处理
        if file_pwd is not None:
            file = encrypt_file(
                input_file=file,
                password=file_pwd,
                file_type=file_type,
            )

        # 处理返回方式
        async def return_streaming(file_name, file_type):
            def file_iterator():
                while chunk := file.read(1024 * 1024):
                    yield chunk
                file.close()

            return StreamingResponse(
                file_iterator(),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f"attachment; filename={file_name}",
                    "X-File-Type": file_type,
                },
            )

        if return_method == "base64":
            return_data["data"]["file"] = base64.b64encode(file.read()).decode("utf-8")
        elif return_method == "from-data":
            return await return_streaming(file_name=file_name, file_type=file_type)
        elif return_method == "url":
            time_out = 30
            base_url = str(request.base_url._url).rstrip("/")
            url_path = f"/temp/{file_name}"

            def call_back():
                return return_streaming(file_name=file_name, file_type=file_type)

            add_temporary_route(url_path, call_back)
            return_data["data"]["file"] = f"{base_url}{url_path}"
            return_data["data"]["file_time_out"] = time_out

        return JSONResponse(content=return_data)
