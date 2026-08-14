"""Root entrypoint to launch the LET local web application."""

import sys
from pathlib import Path

# Ensure src/ is on sys.path even if not installed in editable mode
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from let.config import get_config
from let.web.app import create_app


def main():
    config = get_config()
    app = create_app(config)

    print("\n=======================================================")
    print(" Les Enfants Terribles (LET) — Capture Station")
    print(f" Local Data Root : {config.data_dir}")
    print(f" SQLite Database  : {config.db_path}")
    print(f" Server URL       : http://{config.host}:{config.port}")
    print("=======================================================\n")

    app.run(host=config.host, port=config.port, debug=config.debug)


if __name__ == "__main__":
    main()
