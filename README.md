# Python Rest Client for Delta Api

Delta Exchange is a crypto derivatives exchange where you can trade bitcoin, ethereum, ripple futures upto 100x leverage. This package is a wrapper around rest apis of Delta Exchange.
User Guide - https://www.delta.exchange/user-guide
API Documentation - https://docs.delta.exchange


# Get started

1. Create an account on https://testnet.delta.exchange/signup
2. Install the package: 
	```
	pip install delta-rest-client
	```
3. Follow the below snippet to trade on testnet:
   ```
	from delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size, OrderType, TimeInForce
    
    delta_client = DeltaRestClient(
	    base_url='https://testnet-api.delta.exchange',
	    api_key='',
	    api_secret=''
   )
      ```
4. Get json list of available contracts to trade from given url and note down the product_id and asset_id, as it will be used in most of the api calls.

production -  https://api.delta.exchange/products 
testnet -  https://testnet-api.delta.exchange/products  


## Methods

>**Get Product Detail**

Get product detail of current product id.
[response](https://docs.delta.exchange/#delta-exchange-api-products)


>**Get Product Detail**

Get product detail of current product id.
[See sample response](https://docs.delta.exchange/#delta-exchange-api-products)

```
product = delta_client.get_product(product_id) # Current Instrument
settling_asset = product['settling_asset'] # Currency in which the pnl will be realised
```
|Name            |     Type                      |     Description               |  Required                         |
|----------------|-------------------------------|-------------------------------|-------------------------|
|product_id        |`integer`                    |     id of product             |true


> **Get Ticker Data**

[See sample response](https://docs.delta.exchange/#get-24hr-ticker)
```
response = delta_client.get_ticker(product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                    |     id of product             |true


> **Get Orderbook**

Get level-2 orderbook of the product.
[See sample response](https://docs.delta.exchange/#delta-exchange-api-orderbook)
```
response = delta_client.get_L2_orders(product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|------------------------|
|product_id        |`integer`                      |     id of product              |true


> **Open Orders**

Get open orders.
Authorization required. [See sample response](https://docs.delta.exchange/#get-orders)
```
orders = delta_client.get_orders()
```
> **Create Order Format**

This method creates order object to pass in create_order.
```
order = create_order_format(product_id, size, side, price, order_type=OrderType.LIMIT, time_in_force=TimeInForce.GTC)
```
|Name            |     Type                      |     Description                |Required                    |
|----------------|-------------------------------|--------------------------------|----------------------------|
|product_id      |`int`                          |     id of product              |true                        |
|size            |`int`                          |     order size                 |true                        |
|side            |`string`                       |     buy or sell                |true                        |
|order_type      |`string`                       |     limit or market            |false (LIMIT by default)    |
|time_in_force   |`string`                       |     IOC or GTC or FOK          |false (GTC by default)      |
|post_only       |`string`                       |     true or false              |false (false by default)    |


> **Place Order**

Create a new market order or limit order.
Authorization required. [See sample response](https://docs.delta.exchange/#place-order)

```
order = create_order_format(product_id, size, side, price, )
order_response = delta_client.create_order(order)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order        |`object`                      |     order object             |true


> **Cancel Order**

Delete open order.
Authorization required. [See sample response](https://docs.delta.exchange/#cancel-order)
```
order = cancel_order_format(order)
cancel_response = delta_client.cancel_order(order)
```

|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order        |`object`                      |     order object             |true


> **Batch Create Orders**

Create multiple limit orders. Max number of order is 5. 
Authorization required. [See sample response](https://docs.delta.exchange/#create-batch-orders)
```
response = delta_client.batch_create(product_id, orders)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order           |`array`                        |    array of orders            |true


> **Batch Cancel Orders**

Cancel multiple open orders. Max number of order is 5. 
Authorization required. [See sample response](https://docs.delta.exchange/#delele-batch-orders)
```
response = delta_client.batch_cancel(product_id, orders)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|order           |`array`                        |    array of orders            |true


> **Change Order Leverage**

Change leverage for new orders.
Authorization required. [See sample response](https://docs.delta.exchange/#change-order-leverage)
```
response = delta_client.set_leverage(product_id, leverage)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id      |`integer`                      |     id of product             |true
|leverage        |`string`                       |     leverage value            |true

> **Open Position**

Current open position of product.
Authorization required. [See sample response](https://docs.delta.exchange/#get-open-positions)
```
response = delta_client.get_position(product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                      |     id of product               |true


> **Close Position**

Close position of product.
Authorization required. [See sample response](https://docs.delta.exchange/#close-position)
```
response = delta_client.close_position(product_id)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                    |     id of product             |true


> **Add/Remove Position Margin**

Add/Remove margin to/from open position.
Authorization required. [See sample response](https://docs.delta.exchange/#add-remove-position-margin)

```
response = delta_client.change_position_margin(product_id, margin)
```
|Name            |     Type                      |     Description                      |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|product_id        |`integer`                    |     id of product             |true
|margin            |`string`                     |     new margin                |true



> **Get Wallet**

Get user's balance.
Authorization required. [See sample response](https://docs.delta.exchange/#get-wallet-balances)
```
response = delta_client.get_wallet(asset_id)
```
|Name            |     Type                      |     Description               |Required                         |
|----------------|-------------------------------|-------------------------------|-----------------------------|
|asset_id        |`integer`                      |     id of asset               |true


> **Price History**

Get price history.
[See sample response](https://docs.delta.exchange/#delta-exchange-api-ohlc-candles)
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

