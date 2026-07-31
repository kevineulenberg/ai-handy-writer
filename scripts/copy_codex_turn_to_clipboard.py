#!/usr/bin/env python3

import json
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2:
        return 0

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        return 0

    message = payload.get("last-assistant-message")
    if not isinstance(message, str) or not message:
        return 0

    subprocess.run(
        ["/usr/bin/pbcopy"],
        input=message.encode("utf-8"),
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
