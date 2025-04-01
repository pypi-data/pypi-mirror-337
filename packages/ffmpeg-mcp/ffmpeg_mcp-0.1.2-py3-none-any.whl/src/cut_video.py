import src.ffmpeg as ffmpeg
import os
def convert_to_seconds(time_input):
    """
    将不同格式的时间表示转换为秒数。

    参数:
        time_input: 可以是以下格式之一：
            - str: 格式为 'HH:MM:SS', 'MM:SS' 或 'SS'.
            - tuple: 格式为 (HH, MM, SS).
            - int or float: 直接表示秒数.

    返回:
        float: 转换后的秒数表示。

    异常:
        ValueError: 如果输入格式不被识别。
    """
    if isinstance(time_input, (int, float)):
        return float(time_input)

    if isinstance(time_input, str):
        parts = time_input.split(':')
        parts = [float(p) for p in parts]
        if len(parts) == 3:
            hours, minutes, seconds = parts
        elif len(parts) == 2:
            hours = 0
            minutes, seconds = parts
        elif len(parts) == 1:
            hours = 0
            minutes = 0
            seconds = parts[0]
        else:
            raise ValueError(f"Unrecognized time string format: {time_input}")
        return hours * 3600 + minutes * 60 + seconds

    if isinstance(time_input, tuple):
        if len(time_input) == 3:
            hours, minutes, seconds = time_input
        elif len(time_input) == 2:
            hours = 0
            minutes, seconds = time_input
        elif len(time_input) == 1:
            hours = 0
            minutes = 0
            seconds = time_input[0]
        else:
            raise ValueError(f"Unrecognized time tuple format: {time_input}")
        return hours * 3600 + minutes * 60 + seconds

    raise ValueError(f"Unrecognized time input type: {type(time_input)}")

def clip_video_ffmpeg(video_path, start = None, end = None, duration=None, output_path = None, time_out = 30):
    """
    智能视频剪辑函数
    
    参数：
    video_path : str - 源视频文件路径
    start : int/float/str - 开始时间（支持秒数、MM:SS、HH:MM:SS格式,默认为视频开头）
    end : int/float/str - 结束时间（同上，默认为视频结尾）
    duration:  int/float/str - 裁剪时长，end和duration必须有一个
    output_path: str - 裁剪后视频输出路径，如果不传入，会有一个默认的输出路径
    time_out: int - 命令行执行超时时间，默认为30s
    返回：
    error - 错误码
    str - ffmpeg执行过程中所有日志
    str - 生成的剪辑文件路径
    示例：
    clip_video("input.mp4", "00:01:30", "02:30")
    """
    try:
        base, ext = os.path.splitext(video_path)
        if (output_path == None):
            output_path = f"{base}_clip{ext}"
        cmd = f"-i {video_path} "
        if (start != None):
            start_sec = convert_to_seconds(start)
            cmd = f"{cmd} -ss {start_sec}"
        if (end == None and duration is not None):
            end = start_sec + convert_to_seconds(duration)
        if (end != None):
            end_sec = convert_to_seconds(end) 
            cmd = f"{cmd} -to {end_sec}"
        cmd = f"{cmd} -y {output_path}"
        print(cmd)
        status_code, log = ffmpeg.run_ffmpeg(cmd, timeout=time_out)
        print(log)
        return {status_code, log, output_path}
    except Exception as e:
        print(f"剪辑失败: {str(e)}")
        return {-1, str(e), ""}