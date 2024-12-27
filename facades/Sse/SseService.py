import time

from flask import Flask, Response, render_template
from flask_cors import CORS
from threading import Lock, Event

app = Flask(__name__)
CORS(app)  # 启用 CORS
# 用于存储 SSE 客户端的连接
clients = {}
clients_lock = Lock()

# 用于触发发送数据的事件
send_event = Event()
data_queue = []

def generate(client_id):
    while True:
        send_event.wait()  # 等待事件触发
        send_event.clear()  # 清除事件

        with clients_lock:
            if client_id not in clients:
                break
        if data_queue:
            data = data_queue.pop(0)
        else:
            data = f"data: {time.strftime("%Y-%m-%d %H:%M:%S")}\n\n"
        yield data

@app.route('/stream')
def stream():
    client_id = id(Response())
    response = Response(generate(client_id), mimetype='text/event-stream')

    with clients_lock:
        clients[client_id] = response
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trigger', methods=['POST'])
def trigger():
    data = f"data: 1223\n\n"
    with clients_lock:
        data_queue.append(data)
    send_event.set()
    return "Data sent!"

if __name__ == '__main__':
    app.run(port=8233)
