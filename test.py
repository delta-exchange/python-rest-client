from delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size, OrderType, TimeInForce
import requests
delta_client = DeltaRestClient(
    base_url='https://devnet-api.delta.exchange',
    api_key='',
    api_secret='',
    raise_for_status=False
)

product_id = 13
product = delta_client.get_product(product_id)
assets = delta_client.get_assets()
print(assets)
print(product)


# Create Order
order1 = create_order_format(product_id=product_id, size=10, side="sell", price=9000)
order2 = create_order_format(product_id=product_id, size=10, side="sell", price=9001)
delta_client.create_order(order1)  # will create order on testnet
delta_client.create_order(order2)
orders = delta_client.batch_create(product_id, [order1, order2])

# Batch edit
edit_orders = list(map(lambda o: {
    'id': o['id'],
    'limit_price': "9002",
    'size': 15,
    'product_id': product_id
}, orders))
delta_client.batch_edit(product_id, edit_orders)


# Get open limits order and pending stop orders
orders = delta_client.get_live_orders(query={'product_ids': product_id, 'states': 'open,pending'})
print(orders)

# Batch delete
delete_orders = list(map(lambda o: {
    'id': o['id'],
    'product_id': product_id
}, orders))
delta_client.batch_cancel(product_id, delete_orders)

# Get balances
wallet = delta_client.get_balances(product['settling_asset']['id'])
print(wallet)

# Get position
position = delta_client.get_position(product_id)
margined_position = delta_client.get_margined_position(product_id)
print(position)
print(margined_position)

# Orderbook and ticker
orderbook = delta_client.get_l2_orderbook(product_id, auth=True)
print(orderbook)
ticker = delta_client.get_ticker(product['symbol'])
print(ticker)


# Set leverage
delta_client.set_leverage(product_id, 2)

# Place order and place stop order
try:
    order_limit_gtc = delta_client.place_order(
        product_id, 10, 'buy', limit_price=8800, time_in_force=TimeInForce.GTC)
    print(order_limit_gtc)
    stop_order = delta_client.place_stop_order(
        product_id, order_type=OrderType.MARKET, size=10, side='sell', stop_price=6000)

    trailing_stop_order = delta_client.place_stop_order(
        product_id=product_id,
        size=10,
        side='sell',
        order_type=OrderType.MARKET,
        trail_amount=20,
        isTrailingStopLoss=True
    )
except requests.exceptions.HTTPError as e:
    print(e.response.code)


#Order history & Fills
query =  {"product_ids": product_id}
print("Getting first order history")
history = delta_client.order_history(query, page_size=1)
print(history)
if history["meta"]["after"] is not None:
    print("Getting next order history via pagination")
    history = delta_client.order_history(query, page_size=1, after=history["meta"]["after"])
    print(history)

fills =  delta_client.fills(query, page_size=1)
print(fills)

