# -*- coding: utf-8 -*-
# @Time: 2024/6/5 下午5:27
# @Author: dyz
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from edge_tts import Communicate
from fastapi.responses import Response
from fastapi.responses import StreamingResponse


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# 允许所有来源的跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],   # 允许所有HTTP方法
    allow_headers=["*"]    # 允许所有请求头
)



class Item(BaseModel):
    text: str
    voice: str = 'zh-CN-XiaoxiaoNeural'


@app.post("/tts/")
async def text_to_speech(data: Item):
    # 检查输入是否为空
    if not data.text:
        raise HTTPException(status_code=400, detail="文本不能为空")
    # 使用edge_tts将文本转换为语音
    communicate = Communicate(data.text, data.voice)

    async def generate_audio():
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    return StreamingResponse(generate_audio(), media_type="audio/mp3")


@app.post("/tts2/")
async def text_to_speech(data: Item):
    # 检查输入是否为空
    if not data.text:
        raise HTTPException(status_code=400, detail="文本不能为空")

    # 初始化TTS引擎（此处使用您自定义的MyCommunicate）
    communicate = Communicate(data.text, data.voice)
    import io
    # 创建字节缓冲区
    audio_buffer = io.BytesIO()

    # 收集音频数据
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])

    # 一次性返回完整音频数据
    return Response(
        content=audio_buffer.getvalue(),
        media_type="audio/mpeg",  # 更标准的MIME类型
        headers={
            "Content-Disposition": "attachment; filename=tts_audio.mp3"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8200)
