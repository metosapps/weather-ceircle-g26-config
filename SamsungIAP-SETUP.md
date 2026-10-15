# Samsung IAP setup for Weather 14-26-Ceircle

Package: `app.weather.usa.forecast.g26galaxy`  
Support: `ahmetefeerdal3@gmail.com`  
Remote config: https://github.com/metosapps/weather-ceircle-g26-config

## Product catalog to create

| Benefit | Samsung product type | Billing period | Product ID | Price |
| --- | --- | --- | --- | --- |
| Remove ads weekly | Subscription | 1 week | Not created | Choose in Seller Portal |
| Remove ads monthly | Subscription | 1 month | Not created | Choose in Seller Portal |
| Remove ads yearly | Subscription | 1 year | Not created | Choose in Seller Portal |
| Remove ads permanently | Item | One-time | Not created | Choose in Seller Portal |

No other app's SKU or price is used. Samsung discontinued separate nonconsumable registration in January 2026; register lifetime ad removal as Item. This app acknowledges it and never consumes it. It must not also be sold as an unrelated consumable through another client.

## Connect the real products

1. Register/upload this exact package with the intended release signing identity in Samsung Seller Portal. The locally rebuilt QA APK uses the existing local QA key, not the unknown original developer key.
2. Create the four products above, choose prices/countries/translations, and configure subscription renewal/trial terms if desired.
3. Add each real Product ID to `config.json` under `iap.products`, with `type: subscription` for the three subscriptions or `type: lifetime` for the item, and `enabled: true`.
4. Set `iap.enabled: true`, retain `kill_switches.iap_enabled: true`, increment `config_version` and `revision`, run `python3 validate.py config.json`, and publish. Ads remain controlled independently and are currently disabled.
5. Use Samsung's licensed tester setup. QA is fixed TEST mode; Beta and production builds use PRODUCTION mode. Never assume that an unlicensed production checkout is free.
6. Verify store-supplied titles/prices/periods, cancelled checkout, completed purchase, receipt verification, restart, same-account Restore, subscription expiry/cancellation and all-format ad removal before publishing.

A network or Samsung error keeps the last verified purchase. An authoritative successful ownership result can revoke a missing purchase. TEST purchases cannot grant production Premium. This client-only implementation is not a server entitlement service; no refund webhook or backend account sync is claimed.

The production build workflow also requires this package's verified AdMob App ID (`WEATHER_ADMOB_APP_ID`) and a release signing process. No production APK or Seller Portal submission is included in the current QA build.

## Official references

- https://developer.samsung.com/iap/release-note.html
- https://developer.samsung.com/iap/programming-guide.html
- https://developer.samsung.com/iap/programming-guide/iap-helper-programming.html
- https://developer.samsung.com/iap/programming-guide/samsung-iap-server-api.html
- https://developer.samsung.com/iap/test-guide/prepare-to-test.html
