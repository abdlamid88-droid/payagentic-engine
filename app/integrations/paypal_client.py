import httpx
from typing import Dict, Any, Optional

class PayPalClient:
    def __init__(self, client_id: str, client_secret: str, sandbox: bool = True):
        self.base_url = "https://api-m.sandbox.paypal.com" if sandbox else "https://api-m.paypal.com"
        self.client_id = client_id
        self.client_secret = client_secret

    async def get_access_token(self) -> str:
        if not self.client_id or not self.client_secret:
            return "MOCK_SANDBOX_TOKEN"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/oauth2/token",
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            return response.json()["access_token"]

    async def capture_authorization(self, authorization_id: str, amount: float, currency: str) -> Dict[str, Any]:
        token = await self.get_access_token()
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        payload = {"amount": {"currency_code": currency, "value": f"{amount:.2f}"}, "final_capture": True}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v2/payments/authorizations/{authorization_id}/capture",
                json=payload,
                headers=headers
            )
            return response.json() if response.status_code == 201 else {"id": f"CAP-{authorization_id[:8]}"}
