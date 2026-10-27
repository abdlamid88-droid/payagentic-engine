import zipfile
import yaml
from pathlib import Path
from typing import Dict, Any

class ADKPackageVerifier:
    REQUIRED_ROOT_FILE = "agent.yaml"

    @classmethod
    def verify_package_structure(cls, zip_path: Path) -> Dict[str, Any]:
        if not zip_path.exists():
            return {"status": "FAIL", "reason": "Target archive does not exist."}
        try:
            with zipfile.ZipFile(zip_path, 'r') as archive:
                file_list = archive.namelist()
                if cls.REQUIRED_ROOT_FILE not in file_list:
                    return {"status": "FAIL", "reason": "Missing root 'agent.yaml' required by Google ADK."}
                with archive.open(cls.REQUIRED_ROOT_FILE) as config_file:
                    try:
                        agent_config = yaml.safe_load(config_file)
                        if not isinstance(agent_config, dict):
                            return {"status": "FAIL", "reason": "Malformed agent.yaml."}
                    except yaml.YAMLError as exc:
                        return {"status": "FAIL", "reason": f"YAML parse error: {str(exc)}"}
                for file_name in file_list:
                    if ".." in file_name or file_name.startswith("/"):
                        return {"status": "FAIL", "reason": f"Malicious path traversal detected: {file_name}"}
                adapters = [f for f in file_list if f.startswith("adapters/") and f.endswith(".safetensors")]
                return {
                    "status": "PASS",
                    "agent_name": agent_config.get("name", "Local_ADK_Agent"),
                    "version": agent_config.get("version", "1.0.0"),
                    "adapters_count": len(adapters)
                }
        except zipfile.BadZipFile:
            return {"status": "FAIL", "reason": "Invalid or corrupted zip archive."}
