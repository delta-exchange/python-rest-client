# Changelog 1.0.0 (Breaking Changes)
From Version 1.0.0, we are using delta exchange v2 api. V2 apis are significantly different than v1 apis. Things to watch out for


## Product Changes
1. Certain properties of product object have been renamed
   - product_type -> notional_type
   - commission_rate -> taker_commission_rate
2. Certian properties have been removed
   - pricing source


## Function Changes
1. Certain functions were renamed
    - get_orders -> get_open_orders
    - get_L2_orders -> get_l2_orderbook
    - get_wallet -> get_balances
2. Certain functions were removed
    - get_mark_price
    - get_price_history
    - get_leverage
    - get_all_products


## Other changes
1. Order, Fill and Position don't carry associated objects like product, asset. This was done to make the api payload lighter
2. The Api response and error format has changed. But we have tried parse the new format and return the relevant response directly as the return value.

