import json,os,time,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
ALLOWED={'keepseven.de','smythstoys.com','mueller.de','mediamarkt.de','saturn.de','amazon.de','friese-cards.de','kartenmeier.de'}
def safe(url):
 p=urllib.parse.urlparse(url)
 return p.scheme=='https' and not p.username and not p.password and p.hostname in ALLOWED
def check(url):
 if 'amazon.de' in urllib.parse.urlparse(url).hostname:return 'unbestätigt',None,'Amazon nicht automatisch geprüft'
 try:
  r=requests.get(url,timeout=15,headers={'User-Agent':'Pokemon30Radar/1.0'},allow_redirects=False)
  if r.status_code!=200:return 'unbestätigt',None,'HTTP '+str(r.status_code)
  if 'text/html' not in r.headers.get('Content-Type',''):return 'unbestätigt',None,'Kein HTML'
  soup=BeautifulSoup(r.text[:800000],'html.parser')
  for el in soup.select('script[type="application/ld+json"]'):
   try: root=json.loads(el.string or el.text)
   except (ValueError,TypeError):continue
   stack=[root]
   while stack:
    obj=stack.pop()
    if isinstance(obj,list):stack.extend(obj);continue
    if not isinstance(obj,dict):continue
    for k in ('@graph','mainEntity'): 
     if k in obj:stack.append(obj[k])
    if 'Product' not in str(obj.get('@type','')):continue
    offers=obj.get('offers',[])
    if isinstance(offers,dict):offers=[offers]
    for offer in offers:
     if not isinstance(offer,dict) or offer.get('priceCurrency')!='EUR':continue
     status=str(offer.get('availability','')).lower()
     if 'instock' not in status and 'preorder' not in status and 'presale' not in status:continue
     try:price=float(str(offer['price']).replace(',','.'))
     except (ValueError,TypeError,KeyError):continue
     return ('vorbestellbar' if 'preorder' in status or 'presale' in status else 'lagernd'),price,'Shop-JSON-LD, nicht im Checkout bestätigt'
  return 'unbestätigt',None,'Keine belastbaren strukturierten Angebotsdaten'
 except requests.RequestException:return 'unbestätigt',None,'Netzwerkfehler oder Shop blockiert Zugriff'
def notify(message):
 token=os.getenv('TELEGRAM_BOT_TOKEN');chat=os.getenv('TELEGRAM_CHAT_ID')
 if not token or not chat:return False
 try:
  r=requests.post('https://api.telegram.org/bot'+token+'/sendMessage',json={'chat_id':chat,'text':message,'disable_web_page_preview':True},timeout=15)
  return r.ok and r.json().get('ok') is True
 except (requests.RequestException,ValueError):return False
def main():
 items=json.loads((ROOT/'watchlist.json').read_text())
 path=ROOT/'data/status.json'
 old=json.loads(path.read_text()) if path.exists() else {}
 output={}
 for w in items:
  key=w['id'];url=w['url']
  prev=old.get(key,{})
  record={'id':key,'name':w['name'],'language':w.get('language','DE'),'shop':w['shop'],'url':url,'uvp':w.get('uvp'),'shipping':w.get('shipping'),'checked':datetime.now(timezone.utc).isoformat(timespec='seconds'),'last_alert_key':prev.get('last_alert_key')}
  if not safe(url):status,price,reason='unbestätigt',None,'Nicht freigegebene URL'
  else:status,price,reason=check(url)
  record.update(status=status,price=price,reason=reason)
  uvp=record['uvp'];shipping=record['shipping']
  valid=status in ('lagernd','vorbestellbar') and all(type(v) in (float,int) for v in (price,uvp,shipping)) and uvp>0 and shipping>=0 and 0<price+shipping<=uvp*min(float(w.get('max_multiplier',1.2)),1.3) and w.get('retailer_verified') is True and w.get('uvp_source')
  event=(status,price,shipping) if valid else None
  if event and list(event)!=prev.get('last_alert_key'):
   total=price+shipping
   msg=f"Pokémon 30 Jahre: {w['name']} ({record['language']})\n{w['shop']} | {status}\nGesamt: {total:.2f} EUR | UVP: {uvp:.2f} EUR | Abweichung: {(total/uvp-1)*100:+.1f}%\n{url}\nAutomatisch erkannt; vor Kauf selbst prüfen."
   if notify(msg):record['last_alert_key']=list(event)
  output[key]=record
  time.sleep(1)
 path.parent.mkdir(exist_ok=True)
 path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 print('Scan completed:',len(items),'products; alerts require verified watchlist entries')
if __name__=='__main__':main()
