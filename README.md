# python-rest-client

# Get started

1. Create an account on https://testnet.delta.exchange/signup

2. Install the package:

```
pip install delta-rest-client
```

3. Follow the below snippet to trade on testnet:

```python
from delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size

delta_client = DeltaRestClient(
  base_url='https://testnet-api.delta.exchange',
  api_key='',
  api_secret=''
)

# Get orders
product_id = 2
product = delta_client.get_product(product_id)
settling_asset = product['settling_asset']

# Single Order
order = create_order_format(7078.5, 10, "buy", product_id)
delta_client.create_order(order) # will create order on testnet

# Batch orders
order1 = create_order_format(7078.5, 10, "buy", product_id)
order2 = create_order_format(7078.5, 10, "sell", product_id)
orders = [order1, order2]
delta_client.batch_create(product_id, orders)

# get my open orders
delta_client.get_orders(query={
  'state': 'open'
})
# Get l2 orderbook
delta_client.get_L2_orders(product_id)
# Get l1 orderbook
delta_client.get_ticker(product_id)

# Get wallet balance
delta_client.get_wallet(settling_asset['id'])

# Change Leverage for all open orders
delta_client.set_leverage(product_id=product_id, leverage='2.5')

# Change margin for a product
delta_client.change_position_margin(product_id=product_id, delta_margin='0.05')

# Use can use .request to access rest apis which are not covered
# Example on how to top up a position without using the exposed function
response = delta_client.request('POST', 'positions/change_margin', {
  'product_id': product_id,
  'delta_margin': '0.05'
}, auth=True)
print(response.json())

# Calculating position value & unrealized pnl for the position
from decimal import Decimal
product_id = 2
product = delta_client.get_product(product_id)
position = delta_client.get_position(product_id=product_id)
print('Liquidation Price: %s, Entry Price: %s, Margin: %s' % (
  position['liquidation_price'], position['entry_price'], position['margin'])

mark_price = delta_client.get_mark_price(product_id=product_id)
if product['product_type'] == 'inverse_future':
  position_value = int(position['size']) / Decimal(position['entry_price'])
  unrealized_pnl = int(position['size']) * (1/Decimal(position['entry_price']) - 1/Decimal(mark_price))
else:
  position_value = int(position['size']) * Decimal(position['entry_price'])
  unrealized_pnl = int(position['size']) * (Decimal(mark_price) - Decimal(position['entry_price']))
```

4. Verify your orders on https://testnet.delta.exchange

Same steps can used for production trading.

5. Production base_url is https://api.delta.exchange
6. Production trade terminal url is https://trade.delta.exchange/
