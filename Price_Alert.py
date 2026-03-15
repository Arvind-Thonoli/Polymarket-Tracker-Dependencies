import requests
import time
from datetime import datetime
from ipynb.fs.full.AutoEmail import send_email

CLOB_URL = "https://clob.polymarket.com"
GAMMA_URL = "https://gamma-api.polymarket.com"

def get_token_price(token_id: str) -> float | None:
    """Fetch current mid-market price for a token."""
    try:
        resp = requests.get(f"{CLOB_URL}/midpoint", params={"token_id": token_id}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return float(data["mid"])
    except Exception as e:
        print(f"  [Error fetching price]: {e}")
        return None

def get_event_from_token(token_id: str) -> dict:
    """Look up event/market info from a token ID via Gamma."""
    
    resp = requests.get(
        f"{GAMMA_URL}/markets",
        params={"clob_token_ids": token_id},
        timeout=5
    )
    resp.raise_for_status()
    markets = resp.json()

    if not markets:
        raise ValueError(f"No market found for token_id: {token_id}")

    market = markets[0]
    return market.get("question")

def monitor_price(
    token_id: str,
    target_price: float,
    direction: str = "above",   # "above" or "below"
    poll_interval: int = 5,     # seconds between checks
    on_trigger=None             # optional callback function
):
    """
    Polls a Polymarket token price until it hits the target.

    Args:
        token_id:      The Polymarket token/outcome ID
        target_price:  Price threshold (0.0 to 1.0)
        direction:     Trigger when price goes 'above' or 'below' target
        poll_interval: Seconds between each price check
        on_trigger:    Optional function to call when target is hit
    """
    print(f"Monitoring token: {token_id}")
    print(f"Waiting for price to go {direction} {target_price:.4f}")
    print(f"Polling every {poll_interval}s...\n")

    while True:
        price = get_token_price(token_id)
        now = datetime.now().strftime("%H:%M:%S")

        if price is not None:
            print(f"[{now}] Current price: {price:.4f}", end="")

            triggered = (
                (direction == "above" and price >= target_price) or
                (direction == "below" and price <= target_price)
            )

            if triggered:
                print(f"  ✅ TARGET HIT! Price {price:.4f} is {direction} {target_price:.4f}")
                if on_trigger:
                    on_trigger(token_id, price, target_price)
                return price
            else:
                print(f"  (target: {direction} {target_price:.4f})")
        
        time.sleep(poll_interval)


# --- Example callback when target is hit ---
def on_price_hit(token_id, current_price, target_price):
    print(f"\n🔔 ALERT: Token {token_id}")
    print(f"   Reached {current_price:.4f} (target was {target_price:.4f})")
    send_email(subject="Polymarket Alert", body=f"Token {get_event_from_token(token_id)} hit target price: {current_price:.4f}", to_email="arvindbijulal@gmail.com", to_email2="sarafshaheed78@gmail.com", to_email3="laiyipeng03@gmail.com")
    # e.g. place an order, send a notification, etc.


if __name__ == "__main__":
    TOKEN_ID     = 6628882303864594731548894308977075373030062856864705920016694126013551708713 # paste your token ID
    TARGET_PRICE = 0.6                  # e.g. 75% probability
    DIRECTION    = "above"               # "above" or "below"
    POLL_EVERY   = 60                     # seconds

    monitor_price(
        token_id=TOKEN_ID,
        target_price=TARGET_PRICE,
        direction=DIRECTION,
        poll_interval=POLL_EVERY,
        on_trigger=on_price_hit
    )