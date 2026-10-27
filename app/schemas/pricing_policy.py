from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional

class LicensePolicy(BaseModel):
    package_id: str
    target_hardware: str
    base_price_usd: float = Field(gt=0)
    max_discount_pct: float = Field(ge=0.0, le=0.40)
    floor_price_usd: float = Field(gt=0)

    @field_validator("floor_price_usd")
    @classmethod
    def validate_floor(cls, v, info):
        base = info.data.get("base_price_usd")
        max_disc = info.data.get("max_discount_pct", 0.0)
        if base and v < base * (1 - max_disc):
            raise ValueError("Floor price violates maximum allowable discount threshold.")
        return v

AGENT_CATALOG: Dict[str, LicensePolicy] = {
    "coder-lora-gemma2-9b-swe": LicensePolicy(
        package_id="coder-lora-gemma2-9b-swe",
        target_hardware="RTX_3060_12GB",
        base_price_usd=120.0,
        max_discount_pct=0.25,
        floor_price_usd=90.0
    ),
    "adk-full-repo-navigator-qwen": LicensePolicy(
        package_id="adk-full-repo-navigator-qwen",
        target_hardware="Apple_Silicon_16GB",
        base_price_usd=250.0,
        max_discount_pct=0.20,
        floor_price_usd=200.0
    ),
    "enterprise-offline-audit-bundle": LicensePolicy(
        package_id="enterprise-offline-audit-bundle",
        target_hardware="Local_Workstation_64GB",
        base_price_usd=600.0,
        max_discount_pct=0.30,
        floor_price_usd=420.0
    )
}
