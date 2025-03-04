import os.path
import sys

from elements.enums import OutputType

sys.path.insert(0, os.path.join(os.path.abspath(".")))

import base64
import datetime
import io
import threading
import time

import numpy as np
import uvicorn
from PIL import Image
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

lock = threading.Lock()


class ImageData(BaseModel):
    image: str


class Webserver:
    def __init__(self, model_manager, output_type: OutputType):
        self.app = FastAPI()
        self.model_manager = model_manager
        self.stop_time = None
        self.tracking_started = False
        self.output_type = output_type

        origins = ["*"]

        # Add CORSMiddleware to the application
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["GET", "POST"],  # Specify allowed methods
            allow_headers=["Content-Type"],  # Specify allowed headers
        )

        @self.app.post("/predict/")
        async def predict(data: ImageData):
            try:
                lock.acquire()
                self.tracking_started = True
                self.stop_time = datetime.datetime.now() + datetime.timedelta(seconds=10)

                incoming_image_bytes = base64.b64decode(data.image.split(",")[1])
                image = Image.open(io.BytesIO(incoming_image_bytes))
                image_array = np.asarray(image)[:, :, :3]

                generated_image = self.model_manager.predict([image_array])
                if generated_image is None:
                    self.model_manager.logger.info("Something went wrong, couldn´t process image")
                    if self.model_manager.locker.lock.locked():
                        self.model_manager.locker.lock.release()
                    lock.release()
                    return JSONResponse(content={"image": data.image.split(",")[1]}, status_code=200)

                # In case the output is JSON
                if isinstance(generated_image, str):
                    lock.release()
                    if self.model_manager.locker.lock.locked():
                        self.model_manager.locker.lock.release()
                    return JSONResponse(content={"data": generated_image}, status_code=200)

                pil_img = Image.fromarray(generated_image)
                buff = io.BytesIO()
                pil_img.save(buff, format="JPEG")
                img_str = base64.b64encode(np.ascontiguousarray(buff.getvalue()))
                lock.release()
                if self.model_manager.locker.lock.locked():
                    self.model_manager.locker.lock.release()
                return JSONResponse(content={"image": "data:image/jpeg;base64," + str(img_str).replace("b'", "")[:-1]})
            except Exception as e:
                if lock.locked():
                    lock.release()
                if self.model_manager.locker.lock.locked():
                    self.model_manager.locker.lock.release()
                print(e)
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.post("/predict_binary/")
        async def predict(image: UploadFile = File(...)):
            try:
                lock.acquire()
                self.tracking_started = True
                self.stop_time = datetime.datetime.now() + datetime.timedelta(seconds=10)

                image_contents = await image.read()
                image = Image.open(io.BytesIO(image_contents))
                image_array = np.asarray(image)[:, :, :3]

                generated_image = self.model_manager.predict([image_array])

                pil_img = Image.fromarray(generated_image)
                buff = io.BytesIO()
                pil_img.save(buff, format="JPEG")
                img_str = base64.b64encode(np.ascontiguousarray(buff.getvalue()))
                lock.release()
                if self.model_manager.locker.lock.locked():
                    self.model_manager.locker.lock.release()
                return JSONResponse(content={"image": "data:image/jpeg;base64," + str(img_str).replace("b'", "")[:-1]})
            except Exception as e:
                if lock.locked():
                    lock.release()
                if self.model_manager.locker.lock.locked():
                    self.model_manager.locker.lock.release()
                print(e)
                raise HTTPException(status_code=400, detail=str(e))

    def monitor_tracker(self):
        while True:
            if self.stop_time is None:
                time.sleep(1)
                continue

            while datetime.datetime.now() < self.stop_time and self.tracking_started:
                time.sleep(1)

            self.model_manager.reset_tracker()
            self.tracking_started = False
            time.sleep(1)

    def run(self):
        t = threading.Thread(target=self.monitor_tracker)
        t.start()
        uvicorn.run(self.app, host="0.0.0.0", port=2456)
