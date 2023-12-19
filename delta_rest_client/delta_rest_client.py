import requests
import urllib.parse
import time
import datetime
import hashlib
import hmac
import base64
import json
from enum import Enum

from decimal import Decimal
from .version import __version__ as version


class OrderType(Enum):
  MARKET = 'market_order'
  LIMIT = 'limit_order'


class TimeInForce(Enum):
  FOK = 'fok'
  IOC = 'ioc'
  GTC = 'gtc'


class DeltaRestClient:

  def __init__(self, base_url, api_key=None, api_secret=None, raise_for_status=True):
    self.base_url = base_url
    self.api_key = api_key
    self.api_secret = api_secret
    self.raise_for_status = raise_for_status
    self.session = self._init_session()

  def _init_session(self):
    session = requests.Session()
    user_agent = 'delta-rest-client-v%s' % version
    session.headers.update({'User-Agent': user_agent})
    return session

  # Check if payload and query are working
  def request(self, method, path, payload=None, query=None, auth=False, base_url=None, headers={}):
    if base_url == None:
      base_url = self.base_url
    url = '%s%s' % (base_url, path)

    res = None
    if auth:
      if self.api_key is None or self.api_secret is None:
        raise Exception('Api_key or Api_secret missing')
      timestamp = get_time_stamp()
      signature_data = method + timestamp + path + \
        query_string(query) + body_string(payload)
      signature = generate_signature(self.api_secret, signature_data)
      headers['Content-Type'] = 'application/json'
      headers['api-key'] = self.api_key
      headers['timestamp']  = timestamp
      headers['signature'] = signature

      res = self.session.request(
        method, url, data=body_string(payload), params=query, timeout=(3, 6), headers=headers
      )
    else:
      non_auth_headers = {'User-Agent':'delta-rest-client-v%s'%version, 'Content-Type':'application/json'}
      res = requests.request(method, url, data=body_string(payload), params=query, timeout=(3, 6), headers=non_auth_headers)

    if self.raise_for_status:
      res.raise_for_status()
    return res


  def get_assets(self, auth=False):
    response = self.request('GET', '/v2/assets', auth=auth)
    return parseResponse(response)

  def get_product(self, product_id, auth=False):
    response = self.request("GET", "/v2/products/%s" % (product_id), auth=auth)
    product = parseResponse(response)
    return product

  def batch_create(self, product_id, orders):
    response = self.request(
      "POST",
      "/v2/orders/batch",
      { 'product_id': product_id, 'orders': orders },
      auth=True
    )
    return parseResponse(response)

  def create_order(self, order):
    response = self.request('POST', "/v2/orders", order, auth=True)
    return parseResponse(response)

  def batch_cancel(self, product_id, orders):
    response = self.request(
      "DELETE",
      "/v2/orders/batch",
      {'product_id': product_id, 'orders': orders},
      auth=True
    )
    return parseResponse(response)

  def batch_edit(self, product_id, orders):
    response = self.request(
      "PUT",
      "/v2/orders/batch",
      {'product_id': product_id, 'orders': orders},
      auth=True
    )
    return parseResponse(response)

  def get_live_orders(self, query=None):
    response = self.request(
      "GET",
      "/v2/orders",
      query=query,
      auth=True
    )
    return parseResponse(response)

  def get_l2_orderbook(self, identifier, auth=False):
    response = self.request("GET", "/v2/l2orderbook/%s" % identifier, auth=auth)
    return parseResponse(response)

  def get_ticker(self, identifier, auth=False):
    response = self.request("GET", "/v2/tickers/%s" % (identifier), auth=auth)
    return parseResponse(response)

  def get_balances(self, asset_id):
    response = self.request("GET", "/v2/wallet/balances", auth=True) #query={'asset_id': asset_id}, auth=True)
    wallets = parseResponse(response)
    wallets = list(
      filter(lambda w: w['asset_id'] == asset_id, wallets)
    )
    return wallets[0] if len(wallets) > 0 else None

  def get_position(self, product_id):
    response = self.request(
      "GET",
      "/v2/positions",
      query={
        'product_id': product_id
      },
      auth=True
    )
    return parseResponse(response)

  def get_margined_position(self, product_id):
    response = self.request(
      "GET",
      "/v2/positions/margined",
      query={
        'product_ids': product_id
      },
      auth=True
    )
    positions = parseResponse(response)
    if len(positions) == 0:
      return None
    else:
      return positions[0]

  def set_leverage(self, product_id, leverage):
    response = self.request(
      "POST",
      "/v2/products/%s/orders/leverage" % product_id,
      {
        'leverage':  leverage
      },
      auth=True
    )
    return parseResponse(response)

  def change_position_margin(self, product_id, delta_margin):
    response = self.request(
      'POST',
      '/v2/positions/change_margin',
      {
        'product_id': product_id,
        'delta_margin': delta_margin
      },
      auth=True
    )
    return parseResponse(response)

  def cancel_order(self, product_id, order_id):
    order = {
      'id': order_id,
      'product_id': product_id
    }
    response = self.request('DELETE', "/v2/orders", order, auth=True)
    return parseResponse(response)

  def place_stop_order(self, product_id, size, side, stop_price=None, limit_price=None, trail_amount=None, order_type=OrderType.LIMIT, isTrailingStopLoss=False):
    order = {
      'product_id': product_id,
      'size': int(size),
      'side': side,
      'order_type': order_type.value,
      'stop_order_type': 'stop_loss_order',
    }
    if order_type.value == 'limit_order':
      if limit_price is None:
        raise Exception('limit_price is nil')
      order['limit_price'] = str(limit_price)

    if isTrailingStopLoss is True:
      if trail_amount is None:
        raise Exception('trail_amount is nil')
      order['trail_amount'] = str(trail_amount) if side == 'buy' else str(-1 * trail_amount)
    else:
      if stop_price is None:
        raise Exception('stop_price is nil')
      order['stop_price'] = str(stop_price)
    return self.create_order(order)

  def place_order(self, product_id, size, side, limit_price=None, time_in_force=None, order_type=OrderType.LIMIT, post_only='false', client_order_id = None):
    order = {
      'product_id': product_id,
      'size': int(size),
      'side': side,
      'order_type': order_type.value,
      'post_only': post_only
    }
    if order_type.value == 'limit_order':
      order['limit_price'] = str(limit_price)

    if time_in_force:
      order['time_in_force'] = time_in_force.value
    
    if client_order_id:
      order['client_order_id'] = client_order_id

    return self.create_order(order)

  def order_history(self, query={}, page_size=100, after=None):
    if after is not None:
      query['after'] = after
    query['page_size'] = page_size
    response = self.request(
      'GET',
      '/v2/orders/history',
      query=query,
      auth=True
    )
    return response.json()

  def fills(self, query={}, page_size=100, after=None):
    if after is not None:
      query['after'] = after
    query['page_size'] = page_size
    response = self.request(
      'GET',
      '/v2/fills',
      query=query,
      auth=True
    )
    return response.json()


def parseResponse(response):
  response = response.json()
  if response['success']:
    return response['result']
  elif 'error' in response:
    raise requests.exceptions.HTTPError(response['error'])
  else:
    raise requests.exceptions.HTTPError()

def create_order_format(price, size, side, product_id, post_only='false'):
  order = {
    'product_id': product_id,
    'limit_price': str(price),
    'size': int(size),
    'side': side,
    'order_type': 'limit_order',
    'post_only': post_only
  }
  return order


def cancel_order_format(order):
  order = {
    'id': order['id'],
    'product_id': order['product_id']
  }
  return order


def round_by_tick_size(price, tick_size, floor_or_ceil=None):
  remainder = price % tick_size
  if remainder == 0:
    price = price
  if floor_or_ceil == None:
    floor_or_ceil = 'ceil' if (remainder >= tick_size / 2) else 'floor'
  if floor_or_ceil == 'ceil':
    price = price - remainder + tick_size
  else:
    price = price - remainder
  number_of_decimals = len(format(Decimal(repr(float(tick_size))), 'f').split('.')[1])
  price = round(Decimal(price), number_of_decimals)
  return price


def generate_signature(secret, message):
  message = bytes(message, 'utf-8')
  secret = bytes(secret, 'utf-8')
  hash = hmac.new(secret, message, hashlib.sha256)
  return hash.hexdigest()


def get_time_stamp():
  d = datetime.datetime.utcnow()
  epoch = datetime.datetime(1970, 1, 1)
  return str(int((d - epoch).total_seconds()))


def query_string(query):
  if query == None:
    return ''
  else:
    query_strings = []
    for key, value in query.items():
      query_strings.append(key + '=' + urllib.parse.quote_plus(str(value)))
    return '?' + '&'.join(query_strings)


def body_string(body):
  if body == None:
    return ''
  else:
    return json.dumps(body, separators=(',', ':'))
