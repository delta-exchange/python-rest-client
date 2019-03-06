from delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size, OrderType, TimeInForce
import requests
delta_client = DeltaRestClient(
    base_url='https://testnet-api.delta.exchange',
    api_key='2661d75a99b400cb2cc327b8a65b06',
    api_secret='00488fc9a7d56828c05da81db5fd23d5a4f6cb4728068e7da0f6a1049192'
)

product_id = 11
order1 = create_order_format(
    product_id=product_id, size=10, side="sell", price=3790.5)
order2 = create_order_format(
    product_id=product_id, size=10, side="sell", price=3778)

delta_client.create_order(order1)  # will create order on testnet
delta_client.get_product(product_id)
# delta_client.batch_create(product_id, [order1, order2])
# delta_client.batch_cancel(product_id, [order1, order2])
delta_client.get_orders(query={'product_id': product_id})
delta_client.get_L2_orders(product_id)
delta_client.get_ticker(product_id)
delta_client.get_wallet(2)

delta_client.get_mark_price(product_id)
delta_client.get_position(product_id)
delta_client.set_leverage(product_id, 2)
try:
    order_limit_gtc = delta_client.place_order(
        product_id, 10, 'buy', limit_price=3800, time_in_force=TimeInForce.FOK)
    stop_order = delta_client.place_stop_order(
        product_id, order_type=OrderType.MARKET, size=10, side='sell')

    trailing_stop_order = delta_client.place_stop_order(
        product_id=product_id,
        size=10,
        side='sell',
        order_type=OrderType.MARKET,
        trail_amount=20,
        isTrailingStopLoss=True
    )
except requests.exceptions.HTTPError as e:
    print(e.response.text)
delta_client.order_history()
delta_client.fills()
delta_client.get_assets()
delta_client.get_all_products()
