#!/usr/bin/env python3
from whisper_online import *

import sys
import argparse
import os
import logging
import numpy as np
import socketio
from aiohttp import web
import io
import soundfile
import json
from aiohttp import web
from aiohttp.web import static

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()
# 服务器配置选项
parser.add_argument("--host", type=str, default='0.0.0.0',
                    help="服务器监听的IP地址，默认为0.0.0.0表示监听所有网络接口")
parser.add_argument("--port", type=int, default=43007,
                    help="服务器监听的端口号，默认为43007")
parser.add_argument("--warmup-file", type=str,default='samples_jfk.wav', dest="warmup_file",
        help="预热用的音频文件路径，用于加速首次音频处理。可以使用如https://github.com/ggerganov/whisper.cpp/raw/master/samples/jfk.wav的示例文件")

# options from whisper_online
add_shared_args(parser)
args = parser.parse_args()

set_logging(args,logger,other="")

# 设置音频采样率（Hz）
SAMPLING_RATE = 16000

# 获取模型配置
size = args.model  # 模型大小/版本
language = args.lan  # 识别语言
# 创建ASR（自动语音识别）实例和在线处理器
asr, online = asr_factory(args)

asr:OpenaiApiASR = asr

# 获取最小音频块大小设置
min_chunk = args.min_chunk_size

# 预热ASR模型
msg = "Whisper模型未预热，首次音频块处理可能需要较长时间。"
if args.warmup_file:
    if os.path.isfile(args.warmup_file):
        logger.info("Whisper模型开始预热...")
        a = load_audio_chunk(args.warmup_file,0,1)
        asr.transcribe(a)
        logger.info("Whisper模型预热完成。")
    else:
        logger.critical("预热音频文件不可用。"+msg)
        sys.exit(1)
else:
    logger.warning(msg)

# 创建SocketIO服务器
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()

# 添加静态文件服务支持
app.router.add_static('/static', 'static')

sio.attach(app)

class ASRProcessor:
    def __init__(self, sid, online_asr_proc, min_chunk, from_lang=None, to_lang=None):
        self.sid = sid
        self.online_asr_proc: OnlineASRProcessor = online_asr_proc
        self.min_chunk = min_chunk
        self.last_end = None
        self.is_first = True
        self.audio_buffer = []
        self.from_lang = from_lang
        self.to_lang = to_lang
        
        # 初始化音频缓存
        if hasattr(online_asr_proc.asr, 'audio_cache'):
            self.audio_cache = online_asr_proc.asr.audio_cache
        else:
            self.audio_cache = None

    def process_audio_chunk(self, audio_data, user_id=None):
        """处理音频数据块"""
        try:
            # 解析音频数据
            audio_bytes = audio_data.encode() if isinstance(audio_data, str) else audio_data
            
            # 转换音频数据
            sf = soundfile.SoundFile(io.BytesIO(audio_bytes), channels=1,
                                   endian="LITTLE", samplerate=SAMPLING_RATE,
                                   subtype="PCM_16", format="RAW")
            audio, _ = librosa.load(sf, sr=SAMPLING_RATE, dtype=np.float32)
            
            # 如果启用了音频缓存，则存储到对应用户的缓存中
            if self.audio_cache and user_id:
                self.audio_cache.add_audio(user_id, audio)
            
            self.audio_buffer.append(audio)
            
            # 检查是否有足够的数据进行处理
            total_length = sum(len(x) for x in self.audio_buffer)
            if total_length >= self.min_chunk * SAMPLING_RATE:
                # 合并音频数据
                conc = np.concatenate(self.audio_buffer)
                self.audio_buffer = []
                
                if not self.is_first or len(conc) >= self.min_chunk * SAMPLING_RATE:
                    # 设置输入语言
                    if self.from_lang:
                        self.online_asr_proc.asr.original_language = self.from_lang
                    return conc
                
            return None
        except Exception as e:
            logger.error(f"处理音频数据时出错: {str(e)}")
            return None

    def format_output_transcript(self, o, user_id=None, to=None):
        """格式化转录结果输出"""
        if o[0] is not None:
            beg, end = o[0]*1000, o[1]*1000
            if self.last_end is not None:
                beg = max(beg, self.last_end)

            self.last_end = end
            result = {
                "start": beg,
                "end": end,
                "text": o[2],
                "userId": user_id,
                "transl": None
            }
            if to:
                # 设置翻译任务并获取翻译结果
                # self.online_asr_proc.asr.set_translate_task()
                translated = self.online_asr_proc.asr.translate_text(o[2], target_language=to)
                result["transl"] = translated or  None
            print("%1.0f %1.0f %s" % (beg,end,o[2]), flush=True, file=sys.stderr)
            return result
        else:
            logger.debug("此区段中没有文本")
            return None

# 存储所有处理器实例
processors = {}

@sio.event
async def connect(sid, environ):
    logger.info(f'客户端已连接，ID：{sid}')
    # 为新连接创建处理器实例
    processors[sid] = ASRProcessor(sid, online, args.min_chunk_size, None, None)
    online.init()

@sio.event
async def disconnect(sid):
    logger.info(f'客户端断开连接，ID：{sid}')
    if sid in processors:
        del processors[sid]

@sio.event
async def handle_message(sid, data):
    """处理接收到的音频数据"""
    if sid not in processors:
        return

    processor = processors[sid]

    # 解析数据
    user_id = None
    if isinstance(data, str):
        data = json.loads(data)
    audio_content = data.get('data')
    if isinstance(data, dict):
        user_id = data.get('userId')
        audio_content = data.get('data')
        from_lang = data.get('from', 'zh')
        to_lang = data.get('to')

        # 更新处理器的语言设置
        if from_lang:
            processor.from_lang = from_lang
        if to_lang:
            processor.to_lang = to_lang

        if not user_id:
            raise ValueError('Missing userId')

        if not audio_content:
            raise ValueError('Missing audio data')

    # 处理音频数据
    audio_chunk = processor.process_audio_chunk(audio_content, user_id)

    if audio_chunk is not None:
        # 将音频数据插入ASR处理器
        processor.online_asr_proc.insert_audio_chunk(audio_chunk)
        # 获取处理结果
        o = online.process_iter()
        # 格式化并发送结果
        result = processor.format_output_transcript(o, user_id, processor.to_lang)
        if result:
            await sio.emit('response_message', result, room=sid)

# 启动服务器
if __name__ == '__main__':
    web.run_app(app, host=args.host, port=args.port)
    logger.info('服务器已终止运行。')
