#!/usr/bin/env python3
"""Offline validation of this package's public config. No third-party packages."""
import json, re, sys
from pathlib import Path
from urllib.parse import urlparse
PKG='app.weather.usa.forecast.g26galaxy'
def validate(c):
 def need(ok, msg):
  if not ok: raise ValueError(msg)
 def integer(o,k,low,high): need(type(o.get(k)) is int and low<=o[k]<=high,k+' out of range/type')
 def boolean(o,k): need(type(o.get(k)) is bool,k+' must be boolean')
 def string(o,k,n): need(isinstance(o.get(k),str) and len(o[k])<=n,k+' must be bounded string')
 def store_url(url,store):
  return url in ({'samsungapps://ProductDetail/'+PKG,'https://apps.samsung.com/appquery/appDetail.as?appId='+PKG,'https://galaxystore.samsung.com/detail/'+PKG} if store=='galaxy_store' else {'market://details?id='+PKG,'https://play.google.com/store/apps/details?id='+PKG})
 integer(c,'schema_version',1,1); need(c.get('package')==PKG,'wrong package'); need(c.get('store')=='galaxy_store','wrong store')
 integer(c,'config_version',1,2147483647); string(c,'revision',100); need(re.fullmatch(r'[A-Za-z0-9._-]+',c['revision']),'revision characters')
 integer(c,'refresh_seconds',60,3600); integer(c,'max_cache_age_seconds',3600,604800)
 for name in ['global','android','links','features','kill_switches','ads']: need(type(c.get(name)) is dict,'missing section '+name)
 boolean(c['global'],'maintenance_mode'); string(c['global'],'maintenance_message',1000)
 for k,v in c['features'].items(): boolean(c['features'],k)
 boolean(c['kill_switches'],'ads_enabled')
 if 'iap_enabled' in c['kill_switches']: boolean(c['kill_switches'],'iap_enabled')
 if 'iap' in c:
  iap=c['iap']; need(type(iap) is dict,'iap must be object'); boolean(iap,'enabled')
  need(type(iap.get('products')) is list and len(iap['products'])<=8,'iap products must be array of at most 8')
  ids=set()
  for product in iap['products']:
   need(type(product) is dict,'iap product object'); string(product,'id',128)
   need(re.fullmatch(r'[A-Za-z0-9._-]{1,128}',product['id']) and product['id'] not in ids,'invalid or duplicate iap id'); ids.add(product['id'])
   need(product.get('type') in ('lifetime','subscription'),'invalid iap type'); boolean(product,'enabled')
 for store in ['galaxy_store','google_play']:
  s=c['android'][store]
  integer(s,'min_supported_version_code',1,2147483647); integer(s,'latest_version_code',s['min_supported_version_code'],2147483647)
  need(s['update_mode'] in ['none','soft','force'],'update mode'); need(store_url(s['update_url'],store),'wrong store destination')
 for k,v in c['links'].items():
  string(c['links'],k,2048)
  if not v: continue
  if k=='support_email': need(re.fullmatch(r'[^\s@]+@[^\s@]+\.[A-Za-z]{2,}',v),'invalid support email'); continue
  if k in ('rate','share'): need(store_url(v,'galaxy_store') or store_url(v,'google_play'),'package-specific store link required')
  if v.startswith(('samsungapps:','market:')): need(store_url(v,'galaxy_store' if v.startswith('samsungapps:') else 'google_play'),'wrong app link'); continue
  u=urlparse(v); h=(u.hostname or '').lower()
  need(u.scheme=='https' and '.' in h and not re.fullmatch(r'[\d.]+',h) and not h.endswith(('.local','.localhost','.internal')) and u.username is None and u.port in (None,443) and not re.search(r'\.(apk|apks|aab|xapk|dex|jar|so|exe|sh)(?:/.*)?',u.path,re.I),'unsafe link '+k)
 a=c['ads']; boolean(a,'enabled'); boolean(a,'production_enabled'); string(a,'app_id',100)
 need(not a['app_id'] or re.fullmatch(r'ca-app-pub-\d{16}~\d{10}',a['app_id']),'app id syntax')
 integer(a,'global_cooldown_seconds',30,86400); integer(a,'max_fullscreen_per_session',0,20)
 for f in ['banner','native','interstitial','app_open']: boolean(a['formats'][f],'enabled')
 expected={n for group in [['banner_'+x for x in ['main','locations','units','widgets','features','notifications','hourly','daily']],['native_'+x for x in ['weather','exit','hourly','daily']],['interstitial_splash','interstitial_navigation','app_open_foreground']] for n in group}
 need(set(a['placements'])==expected,'15 known placement keys are required')
 for key,p in a['placements'].items():
  boolean(p,'enabled'); need(p['format']==('app_open' if key.startswith('app_open_') else key.split('_')[0]),'placement format')
  string(p,'unit_id',100); need(not p['unit_id'] or re.fullmatch(r'ca-app-pub-\d{16}/\d{10}',p['unit_id']),'unit id syntax')
  integer(p,'every_n_actions',1,100); integer(p,'min_interval_seconds',120 if p['format']=='app_open' else 60,86400)
  integer(p,'max_per_session',0,50); integer(p,'max_per_day',0,100); integer(p,'first_session_delay_seconds',0,3600)
  if 'collapsible' in p: boolean(p,'collapsible')
 if a['production_enabled']:
  need(a['app_id'] and '3940256099942544' not in a['app_id'],'production needs own package-specific app id')
  for key,p in a['placements'].items():
   if p['enabled'] and a['formats'][p['format']]['enabled']:
    need(p['unit_id'] and '3940256099942544' not in p['unit_id'],key+' production unit missing')
 return c
if __name__=='__main__':
 path=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('config.json'))
 body=path.read_bytes()
 if len(body)>131072: raise SystemExit('config is larger than 128KiB')
 def reject_duplicates(pairs):
  result={}
  for k,v in pairs:
   if k in result: raise ValueError('duplicate key '+k)
   result[k]=v
  return result
 c=validate(json.loads(body,object_pairs_hook=reject_duplicates,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite '+x))))
 print('VALID',c['package'],c['revision'],'15 placements')
