import os
from datetime import datetime

import streamlit as st

from bot.logging_config import logger
from bot.service import execute_order


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
    return execute_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )


st.set_page_config(page_title="Trading Bot UI", page_icon="📈", layout="wide")
st.title("Trading Bot UI")
st.caption("Local UI for the existing bot modules (mock Binance testnet client).")

if "last_order" not in st.session_state:
    st.session_state["last_order"] = None

with st.sidebar:
    st.subheader("Order parameters")
    symbol = st.text_input("Symbol", value="BTCUSDT").strip().upper()
    side = st.selectbox("Side", options=["BUY", "SELL"], index=0)
    order_type = st.selectbox("Order type", options=["MARKET", "LIMIT"], index=0)
    quantity = st.number_input("Quantity", min_value=0.0, value=0.01, step=0.01, format="%.6f")
    price = None
    if order_type == "LIMIT":
        price = st.number_input("Limit price", min_value=0.0, value=75000.0, step=10.0, format="%.2f")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        submitted = st.button("Place order", type="primary", use_container_width=True)
    with col_b:
        if st.button("Load example", use_container_width=True):
            st.session_state["example_loaded_at"] = datetime.now().isoformat()
            st.rerun()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Response")
    if submitted:
        try:
            resp = _place_order(symbol, side, order_type, float(quantity), float(price) if price is not None else None)
            st.session_state["last_order"] = resp
            st.success("Order sent.")
            st.json(resp)
        except Exception as e:
            logger.exception("UI error while placing order")
            st.error(str(e))
    else:
        if st.session_state["last_order"] is not None:
            st.info("Last order response:")
            st.json(st.session_state["last_order"])
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
