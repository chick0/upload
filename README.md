# Upload

파일 공유를 위한 웹 사이트

모든 파일은 45분 뒤에 삭제됩니다.

## 주의사항

파일 정보를 Redis 서버에 저장합니다.

따라서 Redis 접속 정보가 설정 되어 있지 않다면 파일 업로드가 불가능합니다.

## 실행하기

1. 의존성 설치하기

    ```bash
    pip install -r requirements.txt
    ```

2. 서버 실행하기

    ```bash
    gunicorn -c gunicorn.py
    ```

3. 워커 실행하기

    ```bash
    python worker.py
    ```

    - 워커는 업로드된 지 45분이 지난 파일을 삭제하는 작업을 합니다.

    - 워커가 실행되고 있지 않다면 만료된 파일이 삭제되지 않습니다.

## 서버 설정하기

### 업로드 용량 제한하기

1. `upload.ini` 파일을 열고

2. `max_size` 옵션을 원하는 용량으로 변경한다.
    - ex) 8mb 이면 8
    - ex) 16mb 이면 16

### Redis 접속 정보 설정하기

1. `upload.ini` 파일을 열고

2. `redis_url` 옵션을 원하는 용량으로 변경한다.
    - ex) 8mb 이면 8
    - ex) 16mb 이면 16

## 콘솔에서 업로드 하기

```bash
curl -F 'file=@./fileName' https://upload.ch1ck.xyz/
```

`User-Agent` 값에 `curl`이 포함되어있다면, 파일 다운로드 링크만 전달 받을 수 있습니다.
