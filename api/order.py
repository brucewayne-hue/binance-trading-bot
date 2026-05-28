import json
from json import JSONDecodeError
from http.server import BaseHTTPRequestHandler

from bot.logging_config import logger
from bot.service import execute_order


MAX_BODY_BYTES = 10_000


def _read_json_body(req: BaseHTTPRequestHandler) -> dict:
    length = int(req.headers.get("content-length", "0") or "0")
    if length <= 0:
        return {}
    if length > MAX_BODY_BYTES:
        raise ValueError(f"Request too large (max {MAX_BODY_BYTES} bytes).")
    raw = req.rfile.read(length)
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except JSONDecodeError:
        raise ValueError("Invalid JSON body.")


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict, extra_headers: dict | None = None):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        # Basic CORS for browser UI on Vercel
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self._send_json(
            200,
            {
                "ok": True,
                "usage": {
                    "POST": {
                        "path": "/api/order",
                        "json": {
                            "symbol": "BTCUSDT",
                            "side": "BUY",
                            "type": "MARKET",
                            "quantity": 0.01,
                            "price": 75000.0,
                        },
                    }
                },
            },
        )

    def do_POST(self):
        try:
            content_type = (self.headers.get("content-type") or "").lower()
            if content_type and "application/json" not in content_type:
                raise ValueError("Content-Type must be application/json.")

            data = _read_json_body(self)
            symbol = str(data.get("symbol", "BTCUSDT"))
            side = str(data.get("side", "BUY"))
            order_type = str(data.get("type", "MARKET"))
            quantity = float(data.get("quantity", 0.01))
            price = data.get("price", None)
            price_f = float(price) if price is not None else None

            resp = execute_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price_f,
            )

            self._send_json(200, {"ok": True, "order": resp})
        except Exception as e:
            logger.exception("API error while placing order")
            self._send_json(400, {"ok": False, "error": str(e)})

    def do_PUT(self):
        self._send_json(405, {"ok": False, "error": "Method not allowed."})

    def do_DELETE(self):
        self._send_json(405, {"ok": False, "error": "Method not allowed."})
