# Python Rest Client for Delta Api

Delta Exchange is a crypto derivatives exchange where you can trade bitcoin, ethereum, ripple futures upto 100x leverage. This package is a wrapper around rest apis of Delta Exchange.

# Get started

1. Create an account on https://testnet.delta.exchange/signup
2. Install the package: 
	```
	pip install delta-rest-client
	```
3. Follow the below snippet to trade on testnet:
   ```
	from delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size
    
    delta_client = DeltaRestClient(
	    base_url='https://testnet-api.delta.exchange',
	    api_key='',
	    api_secret=''
   )
      ```

## Methods

>**Get Product Detail**
```
product = delta_client.get_product(product_id)
settling_asset = product['settling_asset']
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                      |     id of product               |true


> **Get Ticker Data**
```
response = delta_client.get_ticker(product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                    |     id of product             |true


> **Get Orderbook**
```
response = delta_client.get_L2_orders(product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|------------------------|
|product_id        |`integer`                      |     id of product              |true


> **Open Orders**
```
orders = delta_client.get_orders()
```

> **Create Order Format**
```
order = create_order_format(price, size, side, product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                      |     id of product               |true


> **Place Order**
```
order_response = delta_client.create_order(order)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order        |`object`                      |     order object             |true



> **Cancel Order Format**
```
cancel_order = cancel_order_format(order)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order        |`object`                      |     order object             |true



> **Cancel Order**
```
cancel_response = delta_client.cancel_order(order)
```

|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order        |`object`                      |     order object             |true


> **Batch Create Orders**
```
response = delta_client.batch_create(orders)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order           |`array`                        |    array of orders            |true


> **Batch Cancel Orders**
```
response = delta_client.batch_cancel(orders)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order           |`array`                        |    array of orders            |true


> **Change Order Leverage**
```
response = delta_client.set_leverage(product_id, leverage)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id      |`integer`                      |     id of product             |true
|leverage        |`string`                       |     leverage value            |true

> **Open Position**
```
response = delta_client.get_position(product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                      |     id of product               |true


> **Close Position**
```
response = delta_client.close_position(product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                      |     id of product               |true


> **Add/Remove Position Margin**
```
response = delta_client.change_position_margin(product_id, margin)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                    |     id of product             |true
|margin            |`string`                     |     new margin                |true



> **Get Wallet**
```
response = delta_client.get_wallet(asset_id)
```
|Name            |     Type                      |     Description               |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|asset_id        |`integer`                      |     id of asset               |true


> **Price History**
```
response = delta_client.get_price_history(symbol, duration, resolution) 
```
|Name            |     Type                      |     Description               |Required                         |
|----------------|-------------------------------|-------------------------------|--------------------
|symbol          |`integer`                      |     id of product             |true
|duration        |`string`                       |     default to 5              |false
|resolution      |`string`                       |     default to 1              |false

> **Mark Price**
```
response = delta_client.get_mark_price(product_id) 
```
|Name            |     Type                      |     Description               |Required                         |
|----------------|-------------------------------|-------------------------------|--------------------
|product_id      |`integer`                      |     id of product             |true

