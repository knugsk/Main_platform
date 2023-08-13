
# gunicorn.conf.py
import sys
import os

chdir = "/app"
sys.path.append(os.path.join(chdir, "Main_platform"))  # 프로젝트 루트를 Python 경로에 추가

bind = "0.0.0.0:8080"  # Gunicorn이 수신할 호스트와 포트 설정
workers = 4            # 동시에 처리할 worker 프로세스 수 (적절한 수로 조정)
timeout = 120          # 워커 프로세스가 처리하는 최대 시간 (초)