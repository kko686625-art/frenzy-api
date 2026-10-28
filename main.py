import requests
import json
import datetime

def get_korean_frenzy_index():
    url = "https://api.upbit.com/v1/market/all"
    markets = requests.get(url, params={"isDetails":"false"}).json()
    krw_markets = [m['market'] for m in markets if m['market'].startswith('KRW-')]

    target_markets = krw_markets[:50]
    response = requests.get("https://api.upbit.com/v1/ticker", params={"markets": ",".join(target_markets)}).json()
    
    results = []
    for data in response:
        change_rate = data['signed_change_rate'] * 100
        trade_vol = data['acc_trade_price_24h'] / 100000000 
        
        results.append({
            "coin": data['market'],
            "price_krw": data['trade_price'],
            "change_percent": round(change_rate, 2),
            "trade_vol_100m_krw": round(trade_vol, 2),
            "frenzy_score": round(change_rate * trade_vol, 2)
        })
    
    results = sorted(results, key=lambda x: x['frenzy_score'], reverse=True)[:10]
    
    final_data = {
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market": "Upbit Korea",
        "description": "Korean Retail Frenzy Index (Top 10)",
        "data": results
    }
    
    with open("frenzy_index.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_korean_frenzy_index()
