if [ -f "installed.txt" ]; then
    echo "installed.txt 存在：已安装 requirements.txt"

    python main.py
    exit 1
else
    echo "installed.txt 不存在：未检测到安装记录" >&2
    python -m pip install --upgrade pip
    pip install paddleocr
    pip install paddlepaddle
    pip install -r requirements.txt
    pip install -e .
    pip freeze > installed.txt
    python main.py

    exit 1
fi