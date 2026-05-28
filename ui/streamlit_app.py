import json
import os
from datetime import datetime

import streamlit as st

from bot.client import get_binance_client
from bot.logging_config import logger
from bot.validators import validate_inputs


def _project_root() -> str:
    return os.path.dirname(os.path.dirname(__file__))


def _log_path() -> str:
    return os.path.join(_project_root(), "logs", "trading_bot.log")


def _read_log_tail(max_bytes: int = 50_000) -> str:
    path = _log_path()
    if not os.path.exists(path):
        return "(log file not found yet)"

    size = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(max(0, size - max_bytes))
        data = f.read()
    return data.decode("utf-8", errors="replace")


def _place_order(symbol: str, side: str, order_type: str, quantity: float, price: float | None):
    symbol, side, order_type, quantity, price = validate_inputs(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )
    params: dict[str, str] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": str(quantity),
    }
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Missing limit price.")
        params["price"] = str(price)
        params["timeInForce"] = "GTC"

    logger.info(
        "UI ORDER -> Asset: %s | Side: %s | Type: %s | Qty: %s | Price: %s",
        symbol,
        side,
        order_type,
        quantity,
        price,
    )
    client = get_binance_client()
    return client.send_futures_order(params)


st.set_page_config(page_title="Trading Bot UI", page_icon="📈", layout="wide")
st.title("Trading Bot UI")
st.caption("Local UI for the existing bot modules (mock Binance testnet client).")

with st.sidebar:
    st.subheader("Order parameters")
    symbol = st.text_input("Symbol", value="BTCUSDT").strip().upper()
    side = st.selectbox("Side", options=["BUY", "SELL"], index=0)
    order_type = st.selectbox("Order type", options=["MARKET", "LIMIT"], index=0)
    quantity = st.number_input("Quantity", min_value=0.0, value=0.01, step=0.01, format="%.6f")
    price = None
    if order_type == "LIMIT":
        price = st.number_input("Limit price", min_value=0.0, value=75000.0, step=10.0, format="%.2f")

    submitted = st.button("Place order", type="primary", use_container_width=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Response")
    if submitted:
        try:
            resp = _place_order(symbol, side, order_type, float(quantity), float(price) if price is not None else None)
            st.success("Order sent.")
            st.json(resp)
        except Exception as e:
            logger.exception("UI error while placing order")
            st.error(str(e))
    else:
        st.info("Fill order parameters and click **Place order**.")

with col2:
    st.subheader("Logs (tail)")
    st.caption(f"File: `{_log_path()}`")
    refresh = st.button("Refresh logs", use_container_width=True)
    _ = refresh  # Streamlit reruns on click
    st.text_area(
        "log_tail",
        value=_read_log_tail(),
        height=520,
        label_visibility="collapsed",
    )

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
