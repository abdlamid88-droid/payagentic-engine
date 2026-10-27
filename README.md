# PayAgentic: ADK Escrow Engine

> **Autonomous Agentic Commerce Engine for Local Coding Agents, Google ADK Bundles, and Fine-Tuned LoRA Adapters powered by PayPal Two-Phase Settlement.**

## 💡 Overview
PayAgentic bridges autonomous AI negotiations with deterministic policy verification and two-phase conditional escrow via PayPal (`AUTHORIZE` & `CAPTURE`).

## 🛠️ Stack
- Python 3.12, FastAPI
- PayPal Orders API v2 & Cryptographic Webhooks
- Google ADK Package Verification & AES-256 License Vault
- AG Grid Enterprise/Community Dark Dashboard
- Render Cloud Deployment (`render.yaml`)

## 🚀 Running Locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
Access Dashboard at: http://localhost:8000
