# Weather 14-26-Ceircle remote controls

This repository controls only `app.weather.usa.forecast.g26galaxy`, Galaxy Store variant. The APK must include the v18 remote-control implementation or a later compatible version. Earlier APKs cannot acquire this behavior from JSON alone.

Edit **config.json**, validate it with `python3 validate.py config.json`, increase `config_version`, update `revision`, and commit. The app fetches the raw `main/config.json` over HTTPS at launch and periodically while foregrounded. Default refresh is 300 seconds; GitHub cache propagation can add delay. Accepted settings persist across restarts. A malformed response, wrong package/store, network failure or older config version never replaces the last good snapshot. Cache expires after 72 hours; the bundled fallback disables ads and keeps the app usable.

## Ads

Production ads start disabled. QA APKs always use official Google sample units, even when production unit IDs are entered here. Production requires a separately signed release with this package's verified AdMob App ID, matching `ads.app_id`, plus `ads.production_enabled: true`. The manifest App ID cannot be changed remotely. Do not reuse another app's IDs.

| Field | Effect |
| --- | --- |
| `kill_switches.ads_enabled` | Emergency switch for all active ad formats |
| `ads.enabled` | Global ads switch |
| `ads.production_enabled` | Separate production eligibility switch; initially false |
| `ads.app_id` | Expected production manifest App ID; empty until configured |
| `ads.formats.FORMAT.enabled` | Enable/disable banner, native, interstitial or app_open |
| `ads.placements.NAME.enabled` | Enable/disable one placement |
| `unit_id` | AdMob unit for this placement; production IDs are initially empty |
| `every_n_actions` | Count eligible placement opportunities: 3 means every third opportunity |
| `min_interval_seconds` | Minimum spacing for this placement |
| `max_per_session` | Maximum actual shows/impressions in one app process session |
| `max_per_day` | Persistent daily cap, UTC day; changing config does not reset counters |
| `first_session_delay_seconds` | Wait from process start before that placement is eligible |
| `ads.global_cooldown_seconds` | Minimum gap shared by all full-screen formats |
| `ads.max_fullscreen_per_session` | Shared full-screen cap |
| banner `collapsible` | Allow collapsible banner where the compiled placement supports it |

Default navigation interstitial: every 3 eligible transitions, at least 90 seconds apart, maximum 3 per session and 10 per UTC day. Splash: maximum 1 per process session and 2 per day. Shared full-screen cap: 5 per process session. App-open starts disabled. Frequency only controls existing app opportunities; it never creates a background/timer ad.

A session is the lifetime of the app process, not each foreground resume. Hard minimum spacing: 60 seconds per banner/native/interstitial placement, 120 seconds app-open, 30 seconds shared full-screen cooldown. Config cannot override Pro, consent, lifecycle, active full-screen safety or update/maintenance gates. Counts come from actual SDK show/impression callbacks. Failed loads and canceled “Showing ads” notices are not impressions.

### Placement map

- Banners: `banner_main`, `banner_locations`, `banner_units`, `banner_widgets`, `banner_features`, `banner_notifications`, `banner_hourly`, `banner_daily`.
- Native: `native_weather`, `native_exit`, `native_hourly`, `native_daily`.
- Interstitial: `interstitial_splash`, `interstitial_navigation`.
- App-open: `app_open_foreground`.

Rewarded SDK classes are present in the original APK, but there is no active user reward flow. No fake remote switch is offered for an unimplemented placement.

Changing accepted config invalidates ad inventory. Disabling ads removes active inline ad views and rejects late load callbacks and pending full-screen shows. An SDK full-screen ad already visible is allowed to finish normally. Turning ads back on takes effect at the next eligible app placement.

## Links, legal pages, support

`links.privacy_policy`, `terms`, `help`, `website`, `support_email`, `rate`, and `share` control app-owned destinations. Contact for this app: **ahmetefeerdal3@gmail.com**. The navigation menu includes **Help & legal** with offline Privacy Policy, Terms and Help, plus an **Open online** action using the current remote URL.

Web destinations must use HTTPS without credentials or executable file targets. Store destinations must identify this exact package. Arbitrary `intent:`, `javascript:`, file and APK-install links are rejected. No GitHub token or weather API key belongs in this public repository. The existing weather-provider/Firebase configuration stays separate.

## Maintenance and updates

`global.maintenance_mode` blocks entry with `maintenance_message`, Retry, Support and Exit. Turning it off resumes normal entry. A gate never launches a browser in the background.

Each `android.galaxy_store` / `android.google_play` section has `min_supported_version_code`, `latest_version_code`, `update_mode` (`none`, `soft`, `force`), and a package-bound `update_url`. Install source selects the store; sideloaded builds use Galaxy Store. `soft` offers Later; `force` or an installed version below minimum requires updating. Only enable forced updates after the new version is available to the affected users. No APK is downloaded or installed by this config.

## Safe edits and rollback

- Disable all ads: set `kill_switches.ads_enabled` to false.
- Disable only navigation interstitial: set its placement `enabled` to false.
- Reduce frequency: raise `every_n_actions` or `min_interval_seconds`, or lower caps.
- Roll back behavior by restoring older values in a **new higher** `config_version`; old versions are rejected.
- Do not delete required fields or placements. Disable an unused placement instead.

Native code, SDKs, permissions, package name, signing, app icon, new placements and new features still need an APK build. `features` is reserved and empty; undocumented flags do not invent executable functionality.

The repository's validation workflow checks each push. Validation failure after a direct push does not undo that push; the APK separately validates every response before accepting it.
