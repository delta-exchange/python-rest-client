from delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size

delta_client = DeltaRestClient(
  base_url='https://testnet-api.delta.exchange',
  api_key='',
  api_secret=''
)

product_id = 3
order1 = create_order_format(7078.5, 10, "buy", product_id)
order2 = create_order_format(7080, 10, "buy", product_id)
delta_client.create_order(order1) # will create order on testnet
delta_client.get_product(product_id)
delta_client.batch_create( product_id, [order1, order2])
delta_client.batch_cancel( product_id, [order1, order2])
delta_client.get_orders( query={'product_id':product_id})
delta_client.get_L2_orders( product_id)
delta_client.get_ticker( product_id)
delta_client.get_wallet(2)
# delta_client.get_price_history( 'BTC', duration=5, resolution=1)
delta_client.get_marked_price(product_id)
delta_client.close_position(product_id) 
delta_client.get_position(product_id) 
delta_client.set_leverage(product_id, 2)