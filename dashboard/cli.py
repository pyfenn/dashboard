from __future__ import annotations

import argparse
import os

from .app import app


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="dashboard")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run the dashboard server")
    run_cmd.add_argument("--host", default="0.0.0.0", help="Bind host")
    run_cmd.add_argument("--port", default=5000, type=int, help="Bind port")
    run_cmd.add_argument("--debug", action="store_true", help="Enable debug mode")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if args.command == "run":
        if args.debug:
            os.environ["FLASK_DEBUG"] = "1"
        app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
