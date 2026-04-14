import asyncio
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="PG Mock Server", description="PlopVape PG API 시뮬레이션")


class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    method: str = "CARD"


class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    message: str


@app.post("/v1/payments", response_model=PaymentResponse)
async def process_payment(request: PaymentRequest):
    # 실제 PG사 응답 시간 시뮬레이션 (~150ms)
    await asyncio.sleep(0.15)

    transaction_id = f"PG-{uuid.uuid4().hex[:8]}"
    return PaymentResponse(
        transaction_id=transaction_id,
        status="SUCCESS",
        message=f"Payment of {request.amount} for order {request.order_id} processed",
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
