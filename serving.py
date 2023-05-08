"""
__project__ = 'holoinsight-ai'
__file_name__ = 'serving'
__author__ = 'LuYuan'
__time__ = '2023/4/7 15:44'
__info__ =
"""
from flask import Flask, request

from handlers.run_main import run_main

app = Flask(__name__)


@app.route('/anomaly_detect', methods=['POST'])
def anomaly_detect():
    body = request.json
    result = run_main(body)
    trace_id = body.get("traceId")
    detect_time = body.get("detectTime")
    result["traceId"] = trace_id
    result["detectTime"] = detect_time
    result["errorCode"] = {}
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    pass
