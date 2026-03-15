import requests
import time
import json
from pprint import pprint

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, MarketOrderArgs, OrderType, OpenOrderParams, BalanceAllowanceParams, AssetType
from py_clob_client.order_builder.constants import BUY, SELL

GAMMA_API = "https://gamma-api.polymarket.com"
DATA_API = "https://data-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"


def get_token_id(slug):
    response = requests.get(
        f"https://gamma-api.polymarket.com/markets?slug={slug}",
        params={"active": "true", "closed": "false", "limit": 1}
    )
    markets = response.json()
    market = markets[0]
    yes_token_id = json.loads(market['clobTokenIds'])[0]
    return yes_token_id