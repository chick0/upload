# upload

단순 파일 업로드 사이트

## 설치 및 실행

1. 의존성 설치
   - `pip install -r requirements.txt`
2. 설정 수정
   - `.env.example` 파일을 `.env` 파일로 복사해주세요.
   - `.env` 파일을 수정해주세요.
   - `MAX_SIZE` 는 업로드 할 수 있는 파일의 최대 용량입니다. (단위:MB)
   - `REDIS_URL` 은 redis 서버 접속 정보 입니다.
3. 서버 시작
   - `gunicorn -c gunicorn.py`
   - 윈도우에서는 gunicorn을 사용 할 수 없습니다.
4. 워커 실행
   - `worker.py`
   - 해당 스크립트는 redis 서버에서 삭제된 파일을 삭제하는 일을 하고 있습니다.
   - 해당 스크립트가 실행중이 아니라면 삭제 되어야하는 파일이 삭제되지 않습니다.
