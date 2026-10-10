#!/usr/bin/env python3
"""Add missing bundled Pi models without replacing user configuration."""

import json
import os
from pathlib import Path
import sys
import tempfile


def install_models(template_path, target_path):
    template = json.loads(Path(template_path).read_text(encoding="utf-8"))
    target = Path(target_path)
    existing = target.exists()
    data = json.loads(target.read_text(encoding="utf-8")) if existing else {}
    if not isinstance(data, dict):
        raise ValueError("Pi model configuration must be a JSON object")
    providers = data.setdefault("providers", {})
    if not isinstance(providers, dict):
        raise ValueError("Pi providers must be a JSON object")
    changed = not existing
    for name, defaults in template["providers"].items():
        provider = providers.setdefault(name, {})
        if not isinstance(provider, dict):
            raise ValueError(f"Pi provider {name} must be a JSON object")
        for key, value in defaults.items():
            if key != "models" and key not in provider:
                provider[key] = value
                changed = True
        models = provider.setdefault("models", [])
        if not isinstance(models, list) or any(not isinstance(m, dict) for m in models):
            raise ValueError(f"Pi provider {name} models must be a JSON array of objects")
        model_ids = {model.get("id") for model in models}
        for model in defaults.get("models", []):
            if model["id"] not in model_ids:
                models.append(model)
                model_ids.add(model["id"])
                changed = True
    if not changed:
        return False

    target.parent.mkdir(parents=True, exist_ok=True)
    mode = (target.stat().st_mode & 0o777) if existing else 0o600
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent,
                                         prefix=".models-", delete=False) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(data, temporary, indent=2, ensure_ascii=False)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, target)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: install_pi_model.py TEMPLATE TARGET")
    try:
        changed = install_models(sys.argv[1], sys.argv[2])
    except (OSError, ValueError, TypeError) as error:
        sys.exit(f"Cannot update Pi models: {error}")
    print("Installed missing Pi models." if changed else "Kept existing Pi models.")
