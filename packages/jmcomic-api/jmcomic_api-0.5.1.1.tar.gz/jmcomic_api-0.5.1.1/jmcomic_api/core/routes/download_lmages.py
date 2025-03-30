from fastapi import Query
from fastapi.responses import JSONResponse
from jmcomic_api._libs import jm_api
from jmcomic_api._utils.env import IMG_FORMAT
from jmcomic_api.models.core.route import Route
from jmcomic_api._utils.file import GetCacheFilePath
import os
import shutil
import asyncio
from jmcomic import create_option_by_str, JmImageDetail

class DownloadImages(Route):
    def __init__(self):
        self.method = ["GET"]
        self.path = "/download/image"

    def config(self, output_dir: str, jm_config: dict):
        self.output_dir = output_dir
        self.client = create_option_by_str(str(jm_config)).build_jm_client()

    async def download_image_concurrently(self, image_data:JmImageDetail, chapter_dir):
        img_save_path = os.path.join(
            chapter_dir, f"{image_data.img_file_name}.{IMG_FORMAT.lower()}"
        )
        await asyncio.to_thread(
            self.client.download_by_image_detail,
            image_data,
            img_save_path,
            decode_image=True,
        )

    async def route_def(
        self,
        jm_id: int = Query(..., title="本子ID", description="本子ID"),
        no_cache: bool = Query(
            False,
            title="是否绕过缓存",
            description="是否绕过缓存",
        ),
    ) -> JSONResponse:
        get_cache_path = GetCacheFilePath(self.output_dir, jm_id).get
        output_dir = get_cache_path(IMG_FORMAT.lower())

        if os.path.exists(output_dir) and not no_cache:
            image_files = []
            for root, _, files in os.walk(output_dir):
                for file in files:
                    if file.lower().endswith(f".{IMG_FORMAT.lower()}"):
                        image_files.append(os.path.join(root, file))
            if image_files:
                return JSONResponse(content={"code": 200, "status": "OK", "data": {}})
            else:
                shutil.rmtree(output_dir, ignore_errors=True)

        os.makedirs(output_dir, exist_ok=True)

        album, image_data_list = jm_api.get_album_images(jm_id, self.client)

        tasks = []
        for chapter_index, photo_data_list in enumerate(image_data_list):
            chapter_dir = os.path.join(output_dir, f"{chapter_index + 1}")
            os.makedirs(chapter_dir, exist_ok=True)

            for image_data in photo_data_list:
                tasks.append(self.download_image_concurrently(image_data, chapter_dir))
        
        await asyncio.gather(*tasks)
        
        return JSONResponse(content={"code": 200, "status": "OK", "data": {}})
