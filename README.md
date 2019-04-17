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
   from delta_rest_client import DeltaRestClient

   delta_client = DeltaRestClient(
    base_url='https://testnet-api.delta.exchange',
    api_key='',
    api_secret=''
  )
   ```

4. Get json list of available contracts to trade from given url and note down the product_id and asset_id, as it will be used in most of the api calls.

production - https://api.delta.exchange/products
testnet - https://testnet-api.delta.exchange/products

## Methods

> **Get All Products**

Get list of current live contracts.

```
response = delta_client.get_all_products()
```

> **Get Assets**

Get list of assets supported on Delta.

```
response = delta_client.get_assets()
```

> **Get Product Detail**

Get product detail of current product.
[See sample response](https://docs.delta.exchange/#delta-exchange-api-products)

```
product = delta_client.get_product(product_id) # Current Instrument
settling_asset = product['settling_asset'] # Currency in which the pnl will be realised
```

| Name       | Type      | Description   | Required |
| ---------- | --------- | ------------- | -------- |
| product_id | `integer` | id of product | true     |

> **Get Ticker Data**

[See sample response](https://docs.delta.exchange/#get-24hr-ticker)

```
response = delta_client.get_ticker(symbol)
```

| Name   | Type     | Description    | Required |
| ------ | -------- | -------------- | -------- |
| symbol | `string` | product symbol | true     |

> **Get Orderbook**

Get level-2 orderbook of the product.
[See sample response](https://docs.delta.exchange/#delta-exchange-api-orderbook)

```
response = delta_client.get_L2_orders(product_id)
```

| Name       | Type      | Description   | Required |
| ---------- | --------- | ------------- | -------- |
| product_id | `integer` | id of product | true     |

> **Open Orders**

Get open orders.
Authorization required. [See sample response](https://docs.delta.exchange/#get-orders)

```
orders = delta_client.get_orders()
```

> **Place Order**

Create a new market order or limit order.
Authorization required. [See sample response](https://docs.delta.exchange/#place-order)

```
order_response = delta_client.place_stop_order(
        product_id=product_id,
        size=10,
        side='sell',
				limit_price='7800',
        order_type=OrderType.LIMIT,
     		time_in_force=TimeInForce.FOK
    )
```

| Name          | Type     | Description                           | Required                 |
| ------------- | -------- | ------------------------------------- | ------------------------ |
| product_id    | `int`    | id of product                         | true                     |
| size          | `int`    | order size                            | true                     |
| side          | `string` | buy or sell                           | true                     |
| limit_price   | `string` | order price (ignored if market order) | false                    |
| order_type    | `string` | limit or market                       | false (LIMIT by default) |
| time_in_force | `string` | IOC or GTC or FOK                     | false (GTC by default)   |
| post_only     | `string` | true or false                         | false (false by default) |

> **Place Stop Order**

Add stop loss or trailing stop loss.
Authorization required. [See sample response](https://docs.delta.exchange/#place-order)

```
# Trailing Stop loss
order_response = delta_client.place_stop_order(
        product_id=product_id,
        size=10,
        side='sell',
				limit_price='7800',
        order_type=OrderType.LIMIT,
        trail_amount='20',
        isTrailingStopLoss=True
    )

# Stop loss
order_response = delta_client.place_stop_order(
        product_id=product_id,
        size=10,
        side='sell',
        order_type=OrderType.MARKET,
        stop_price='8010.5',
    )
```

| Name               | Type     | Description                            | Required                              |
| ------------------ | -------- | -------------------------------------- | ------------------------------------- |
| product_id         | `int`    | id of product                          | true                                  |
| size               | `int`    | order size                             | true                                  |
| side               | `string` | buy or sell                            | true                                  |
| stop_price         | `string` | price at which order will be triggered | false(required if stop_loss)          |
| trail_amount       | `string` | trail price                            | false(required if trailing_stop_loss) |
| limit_price        | `string` | order price (ignored if market order)  | false                                 |
| order_type         | `string` | limit or market                        | false (LIMIT by default)              |
| time_in_force      | `string` | IOC or GTC or FOK                      | false (GTC by default)                |
| isTrailingStopLoss | `string` | true or false                          | false (false by default)              |

> **Cancel Order**

Delete open order.
Authorization required. [See sample response](https://docs.delta.exchange/#cancel-order)

```
cancel_response = delta_client.cancel_order(product_id, order_id)
```

| Name       | Type  | Description   | Required |
| ---------- | ----- | ------------- | -------- |
| product_id | `int` | id of product | true     |
| order_id   | `int` | order id      | true     |

> **Batch Create Orders**

Create multiple limit orders. Max number of order is 5.
Authorization required. [See sample response](https://docs.delta.exchange/#create-batch-orders)

```
response = delta_client.batch_create(product_id, orders)
```

| Name  | Type    | Description     | Required |
| ----- | ------- | --------------- | -------- |
| order | `array` | array of orders | true     |

> **Batch Cancel Orders**

Cancel multiple open orders. Max number of order is 5.
Authorization required. [See sample response](https://docs.delta.exchange/#delele-batch-orders)

```
response = delta_client.batch_cancel(product_id, orders)
```

| Name  | Type    | Description     | Required |
| ----- | ------- | --------------- | -------- |
| order | `array` | array of orders | true     |

> **Change Order Leverage**

Change leverage for new orders.
Authorization required. [See sample response](https://docs.delta.exchange/#change-order-leverage)

```
response = delta_client.set_leverage(product_id, leverage)
```

| Name       | Type      | Description    | Required |
| ---------- | --------- | -------------- | -------- |
| product_id | `integer` | id of product  | true     |
| leverage   | `string`  | leverage value | true     |

> **Open Position**

Current open position of product.
Authorization required. [See sample response](https://docs.delta.exchange/#get-open-positions)

```
response = delta_client.get_position(product_id)
```

| Name       | Type      | Description   | Required |
| ---------- | --------- | ------------- | -------- |
| product_id | `integer` | id of product | true     |

> **Change Leverage Positions**

Change leverage for open position by adding or removing margin to an open position.
Authorization required. [See sample response](https://docs.delta.exchange/#add-remove-position-margin)

```
response = delta_client.change_position_margin(product_id, margin)
```

| Name       | Type      | Description   | Required |
| ---------- | --------- | ------------- | -------- |
| product_id | `integer` | id of product | true     |
| margin     | `string`  | new margin    | true     |

> **Get Wallet**

Get user's balance.
Authorization required. [See sample response](https://docs.delta.exchange/#get-wallet-balances)

```
response = delta_client.get_wallet(asset_id)
```

| Name     | Type      | Description | Required |
| -------- | --------- | ----------- | -------- |
| asset_id | `integer` | id of asset | true     |

> **Price History**

Get price history.
[See sample response](https://docs.delta.exchange/#delta-exchange-api-ohlc-candles)

```
response = delta_client.get_price_history(symbol, duration, resolution)
```

| Name       | Type      | Description   | Required |
| ---------- | --------- | ------------- | -------- |
| symbol     | `integer` | id of product | true     |
| duration   | `string`  | default to 5  | false    |
| resolution | `string`  | default to 1  | false    |

> **Mark Price**

```
response = delta_client.get_mark_price(product_id)
```

| Name       | Type      | Description   | Required |
| ---------- | --------- | ------------- | -------- |
| product_id | `integer` | id of product | true     |

> **Order History**

```
response = delta_client.order_history(page_num=1, page_size=100)
```

| Name      | Type      | Description | Required |
| --------- | --------- | ----------- | -------- |
| page_num  | `integer` | page number | false    |
| page_size | `integer` | page size   | false    |

> **Fills**

Get fill history of your orders

```
response = delta_client.fills(page_num=1, page_size=100)
```

| Name      | Type      | Description | Required |
| --------- | --------- | ----------- | -------- |
| page_num  | `integer` | page number | false    |
| page_size | `integer` | page size   | false    |
