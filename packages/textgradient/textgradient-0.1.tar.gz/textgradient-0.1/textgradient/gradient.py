import json
import sys
from colorama import init

init(autoreset=True)

def hex_to_rgb(hex_color):
    """Hex 색상을 RGB로 변환"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_ansi(r, g, b):
    """RGB 값을 ANSI 24bit 컬러 코드로 변환"""
    return f"\033[38;2;{r};{g};{b}m"

def gradient_text(text, start_color, end_color):
    """텍스트를 시작 색상에서 끝 색상으로 점진적 변화"""
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    length = len(text.replace("\n", ""))  # 공백 제외 문자 수

    gradient_text = ""
    index = 0
    for char in text:
        if char == "\n":
            gradient_text += char
            continue

        # 색상 보간 (선형 보간법)
        ratio = index / max(1, length - 1)
        r = int(start_rgb[0] + ratio * (end_rgb[0] - start_rgb[0]))
        g = int(start_rgb[1] + ratio * (end_rgb[1] - start_rgb[1]))
        b = int(start_rgb[2] + ratio * (end_rgb[2] - start_rgb[2]))

        gradient_text += rgb_to_ansi(r, g, b) + char
        index += 1

    gradient_text += "\033[0m"  # ANSI 스타일 리셋
    return gradient_text

def load_config():
    """설정 파일을 불러와서 실행할 코드를 반환"""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        return config.get("startup_code", "print(\"Hello, Gradient!\")")
    except FileNotFoundError:
        return "print(\"Hello, Gradient!\")"

def main():
    """설정된 코드를 실행"""
    code = load_config()
    exec(code)

if __name__ == "__main__":
    main()