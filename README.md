# Upload

파일 공유를 위한 웹 사이트

모든 파일은 45분 뒤에 삭제됩니다.

## 주의사항

1. 파일과 파일 정보를 메모리에 저장합니다. 따라서 서버가 중간에 꺼질 경우 모든 파일 정보가 삭제됩니다.

2. 메모리를 최대 `3GB`까지 사용합니다.

## 실행하기

1. 의존성 설치하기

    ```bash
    pip install -r requirements.txt
    ```

2. 서버 실행하기

    ```bash
    uvicorn --host 127.0.0.1 --port 16482 --loop uvloop --factory app:create_app
    ```
