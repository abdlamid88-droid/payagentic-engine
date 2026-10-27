from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, status
from app.core.security import verify_paypal_webhook_signature
from app.integrations.paypal_client import PayPalClient
from app.engine.license_crypto import ADKLicenseVault
from app.engine.adk_verifier import ADKPackageVerifier
from pathlib import Path
import os

router = APIRouter(prefix="/webhooks", tags=["PayPal Webhooks"])

PAYPAL_WEBHOOK_ID = os.getenv("PAYPAL_WEBHOOK_ID", "WH-SANDBOX-VERIFIED-ID")
VAULT_SECRET_SALT = os.getenv("VAULT_SECRET_SALT", "local-agentic-entropy-2026")
PACKAGES_DIR = Path("./storage/packages")
LICENSES_DB = {}

@router.post("/paypal")
async def handle_paypal_webhook(request: Request, background_tasks: BackgroundTasks):
    paypal_client = PayPalClient(
        client_id=os.getenv("PAYPAL_CLIENT_ID", ""),
        client_secret=os.getenv("PAYPAL_CLIENT_SECRET", "")
    )
    access_token = await paypal_client.get_access_token()
    is_valid = await verify_paypal_webhook_signature(
        request=request, webhook_id=PAYPAL_WEBHOOK_ID, access_token=access_token
    )
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signature verification failed.")
    event = await request.json()
    event_type = event.get("event_type")
    resource = event.get("resource", {})
    if event_type == "PAYMENT.AUTHORIZATION.CREATED":
        auth_id = resource.get("id", "MOCK-AUTH-1")
        amount = float(resource.get("amount", {}).get("value", "96.0"))
        currency = resource.get("amount", {}).get("currency_code", "USD")
        custom_id = resource.get("custom_id", "coder-lora-gemma2-9b-swe")
        capture_res = await paypal_client.capture_authorization(auth_id, amount, currency)
        license_key = ADKLicenseVault.generate_license_token(auth_id, custom_id, VAULT_SECRET_SALT)
        LICENSES_DB[custom_id] = {"status": "ISSUED", "license_token": license_key}
    return {"status": "ACK", "event_processed": event_type}
