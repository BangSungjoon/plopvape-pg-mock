# PlopVape PG Mock Server

PlopVape 쇼핑몰의 외부 PG(Payment Gateway) API를 시뮬레이션하는 모의 서버.

[plopvape-shop](https://github.com/BangSungjoon/plopvape-shop)의 `payment-service`가 실제 HTTP 호출로 결제를 요청하는 대상입니다. 항상 결제 성공을 반환하며, 장애 테스트는 네트워크/인프라 레벨에서 주입합니다.

## 기술 스택

| 항목 | 기술 |
|------|------|
| Language | Python 3.12 |
| Framework | FastAPI |
| ASGI Server | Uvicorn |

## API

### `POST /v1/payments`

결제 요청을 처리합니다. 실제 PG사 응답 시간을 시뮬레이션하기 위해 약 150ms 지연 후 응답합니다.

**Request:**

```json
{
  "order_id": 1,
  "amount": 75000.0,
  "method": "CARD"
}
```

**Response:**

```json
{
  "transaction_id": "PG-a1b2c3d4",
  "status": "SUCCESS",
  "message": "Payment of 75000.0 for order 1 processed"
}
```

### `GET /health`

헬스 체크 엔드포인트.

```json
{
  "status": "ok"
}
```

## 프로젝트 구조

```
plopvape-pg-mock/
├── pg_mock.py          # FastAPI 앱 (메인)
├── requirements.txt    # fastapi, uvicorn
├── Dockerfile          # python:3.12-slim 기반
└── README.md
```

## 시작하기

### 직접 실행

```bash
pip install -r requirements.txt
uvicorn pg_mock:app --host 0.0.0.0 --port 8090
```

### Docker

```bash
docker build -t plopvape-pg-mock .
docker run -d --name pg-mock \
  --cpus=0.5 --memory=128m \
  -p 8090:8090 \
  plopvape-pg-mock
```

### 확인

```bash
# 헬스 체크
curl http://localhost:8090/health

# 결제 테스트
curl -X POST http://localhost:8090/v1/payments \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "amount": 75000, "method": "CARD"}'
```

## 장애 시나리오 활용

이 서버 자체는 항상 정상 응답합니다. 장애 테스트는 외부에서 주입합니다:

| 시나리오 | 방법 | 효과 |
|---------|------|------|
| PG 응답 지연 | `tc netem`으로 네트워크 지연 추가 | payment-service read timeout 발생 |
| PG 장애 | `docker stop pg-mock` | payment-service connection refused → 재고 복구 트리거 |

## 배포 위치

109서버 Docker 컨테이너 (K3s 밖)에서 실행됩니다.

- APM 모니터링 **제외** (Python 기반, Java Agent 미지원)
- KCM 모니터링 **제외** (K3s 밖)
- SMS 프로세스에 `uvicorn`으로 보이나 자원 사용 극소 (CPU~0%, MEM~30MB)

## 관련 프로젝트

| 프로젝트 | 설명 |
|----------|------|
| [plopvape-shop](https://github.com/BangSungjoon/plopvape-shop) | PlopVape 쇼핑몰 마이크로서비스 (Spring Boot 5개 서비스) |

## License

MIT
