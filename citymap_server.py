"""City 24i Map - local launcher.

Serves the map from this folder on your own PC (127.0.0.1 only, nothing is
reachable from other machines), opens it in your browser, and writes your
district edits to districts.json next to this file.

    python citymap_server.py            (or double-click "Run City Map.bat")
    python citymap_server.py --port 9000 --no-browser
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "districts.json"
MAX_BODY = 2 * 1024 * 1024


def valid(data) -> bool:
    if not isinstance(data, dict) or not isinstance(data.get("districts"), list):
        return False
    for d in data["districts"]:
        if not isinstance(d, dict) or not isinstance(d.get("points"), list) or len(d["points"]) < 3:
            return False
        if not all(isinstance(p, list) and len(p) >= 2 and all(isinstance(v, (int, float)) for v in p[:2])
                   for p in d["points"]):
            return False
    return True


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):      # keep the console quiet apart from saves
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, code: int, payload) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/districts":
            try:
                self._json(200, json.loads(DATA.read_text(encoding="utf-8")))
            except FileNotFoundError:
                self._json(200, {"version": 1, "districts": []})
            except json.JSONDecodeError as e:
                self._json(500, {"error": f"districts.json is not valid JSON: {e}"})
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/districts":
            self._json(404, {"error": "not found"})
            return
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BODY:
            self._json(413, {"error": "bad size"})
            return
        try:
            data = json.loads(self.rfile.read(n).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"error": "not JSON"})
            return
        if not valid(data):
            self._json(400, {"error": "not a district file"})
            return
        if DATA.exists():
            shutil.copyfile(DATA, DATA.with_suffix(".json.bak"))     # one step of undo
        tmp = DATA.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, DATA)
        print(f"  saved {len(data['districts'])} districts to {DATA.name}")
        self._json(200, {"ok": True})


def main() -> int:
    ap = argparse.ArgumentParser(description="Open the City 24i map in your browser.")
    ap.add_argument("--port", type=int, default=8724)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    handler = partial(Handler, directory=str(HERE))
    server = None
    for port in range(args.port, args.port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), handler)
            break
        except OSError:
            continue
    if server is None:
        print(f"Couldn't find a free port between {args.port} and {args.port + 19}.")
        return 1
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"City 24i Map is running at {url}")
    print("Leave this window open while you use the map. Close it (or press Ctrl+C) to stop.")
    if not args.no_browser:
        threading.Timer(0.6, webbrowser.open, (url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
