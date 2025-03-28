import torch

# 这段代码复制自silero-vad的vad_utils.py：
# https://github.com/snakers4/silero-vad/blob/f6b1294cb27590fb2452899df98fb234dfef1134/utils_vad.py#L340
# （除了修改了默认值）

# 他们使用MIT许可证，与我们的许可证相同：https://github.com/snakers4/silero-vad/blob/f6b1294cb27590fb2452899df98fb234dfef1134/LICENSE

class VADIterator:
    def __init__(self,
                 model,
                 threshold: float = 0.5,
                 sampling_rate: int = 16000,
                 min_silence_duration_ms: int = 500,  # makes sense on one recording that I checked
                 speech_pad_ms: int = 100             # same 
                 ):

        """
        用于模拟音频流的类

        参数
        ----------
        model: 预加载的.jit silero VAD模型

        threshold: float (默认值 - 0.5)
            语音阈值。Silero VAD为每个音频块输出语音概率，高于此值的概率被视为语音。
            最好针对每个数据集单独调整此参数，但"懒惰"的0.5对大多数数据集都有不错的效果。

        sampling_rate: int (默认值 - 16000)
            目前silero VAD模型支持8000和16000采样率

        min_silence_duration_ms: int (默认值 - 100毫秒)
            在每个语音块结束时，等待min_silence_duration_ms后再进行分割

        speech_pad_ms: int (默认值 - 30毫秒)
            最终的语音块在两端各填充speech_pad_ms
        """

        self.model = model
        self.threshold = threshold
        self.sampling_rate = sampling_rate

        if sampling_rate not in [8000, 16000]:
            raise ValueError('VADIterator仅支持[8000, 16000]采样率')

        self.min_silence_samples = sampling_rate * min_silence_duration_ms / 1000
        self.speech_pad_samples = sampling_rate * speech_pad_ms / 1000
        self.reset_states()

    def reset_states(self):

        self.model.reset_states()
        self.triggered = False
        self.temp_end = 0
        self.current_sample = 0

    def __call__(self, x, return_seconds=False):
        """
        x: torch.Tensor
            音频块（参见仓库中的示例）

        return_seconds: bool (默认值 - False)
            是否以秒为单位返回时间戳（默认为采样点数）
        """

        if not torch.is_tensor(x):
            try:
                x = torch.Tensor(x)
            except:
                raise TypeError("音频无法转换为张量，请手动进行转换")

        window_size_samples = len(x[0]) if x.dim() == 2 else len(x)
        self.current_sample += window_size_samples

        speech_prob = self.model(x, self.sampling_rate).item()

        if (speech_prob >= self.threshold) and self.temp_end:
            self.temp_end = 0

        if (speech_prob >= self.threshold) and not self.triggered:
            self.triggered = True
            speech_start = self.current_sample - self.speech_pad_samples
            return {'start': int(speech_start) if not return_seconds else round(speech_start / self.sampling_rate, 1)}

        if (speech_prob < self.threshold - 0.15) and self.triggered:
            if not self.temp_end:
                self.temp_end = self.current_sample
            if self.current_sample - self.temp_end < self.min_silence_samples:
                return None
            else:
                speech_end = self.temp_end + self.speech_pad_samples
                self.temp_end = 0
                self.triggered = False
                return {'end': int(speech_end) if not return_seconds else round(speech_end / self.sampling_rate, 1)}

        return None

#######################
# 因为Silero现在要求音频块大小必须恰好为512 

import numpy as np
class FixedVADIterator(VADIterator):
    '''修复VADIterator，使其能够处理任意长度的音频，而不仅限于恰好512帧。
    如果一次处理的音频较长且检测到多个语音段，
    则__call__返回第一个语音段的开始时间，以及最后一个语音段的结束时间（或中间时间，表示尚未结束）。
    '''

    def reset_states(self):
        super().reset_states()
        self.buffer = np.array([],dtype=np.float32)

    def __call__(self, x, return_seconds=False):
        self.buffer = np.append(self.buffer, x) 
        ret = None
        while len(self.buffer) >= 512:
            r = super().__call__(self.buffer[:512], return_seconds=return_seconds)
            self.buffer = self.buffer[512:]
            if ret is None:
                ret = r
            elif r is not None:
                if 'end' in r:
                    ret['end'] = r['end']  # the latter end
                if 'start' in r and 'end' in ret:  # there is an earlier start.
                    # Remove end, merging this segment with the previous one.
                    del ret['end']
        return ret if ret != {} else None

if __name__ == "__main__":
    # 测试/演示使用FixedVADIterator的必要性：

    import torch
    model, _ = torch.hub.load(
        repo_or_dir='snakers4/silero-vad',
        model='silero_vad'
    )
    vac = FixedVADIterator(model)
#   vac = VADIterator(model)  # 第二种情况会导致崩溃

    # 这种方式对两种情况都有效
    audio_buffer = np.array([0]*(512),dtype=np.float32)
    vac(audio_buffer)

    # 这种方式在非FixedVADIterator上会崩溃，错误信息：
    # ops.prim.RaiseException("输入的音频块太短", "builtins.ValueError")
    audio_buffer = np.array([0]*(512-1),dtype=np.float32)
    vac(audio_buffer)
