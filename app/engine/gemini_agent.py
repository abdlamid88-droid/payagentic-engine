import os
import json
from google import genai
from google.genai import types
from app.schemas.pricing_policy import AGENT_CATALOG
from app.engine.negotiator import EscrowNegotiationEngine

# تعريف الأدوات (Tools) التي يملكها الوكيل الذكي
def verify_price_policy(package_id: str, proposed_price: float) -> str:
    """Verifies whether a proposed purchase price complies with deterministic escrow floor rules."""
    result = EscrowNegotiationEngine.evaluate_offer(package_id, proposed_price)
    return json.dumps(result)

def list_available_packages() -> str:
    """Returns the catalog of local AI agent packages and their target hardware specifications."""
    catalog_summary = {
        pkg_id: {
            "target_hardware": policy.target_hardware,
            "base_price": policy.base_price_usd,
            "floor_price": policy.floor_price_usd,
            "max_discount_pct": policy.max_discount_pct
        }
        for pkg_id, policy in AGENT_CATALOG.items()
    }
    return json.dumps(catalog_summary)

class GeminiEscrowAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    async def chat(self, user_message: str, session_id: str) -> dict:
        if not self.client:
            # Fallback محلي نظيف في حال عدم تمرير المفتاح
            return {
                "text": "Gemini API key is not configured. Running in deterministic fallback mode.",
                "tool_used": False
            }

        system_instruction = (
            "You are PayAgentic's autonomous sales broker for local coding agents and Google ADK packages. "
            "You negotiate multi-seat and developer licenses. "
            "CRITICAL RULE: You CANNOT approve prices below the floor price. "
            "You MUST call the verify_price_policy tool whenever the user proposes a price or asks for a discount. "
            "Be professional, technical, and concise."
        )

        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[verify_price_policy, list_available_packages],
                temperature=0.2,
            )
        )
        return {"text": response.text, "candidates": response.candidates}
