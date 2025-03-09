import requests
from config import DEXSCREENER_API_URL

def get_scored_memecoins():
    """Menilai memecoin berdasarkan berbagai faktor tambahan"""
    response = requests.get(DEXSCREENER_API_URL).json()
    scored_coins = []

    for pair in response["pairs"]:
        token_address = pair["baseToken"]["address"]
        name = pair["baseToken"]["name"]
        price = float(pair["priceUsd"])
        volume = float(pair["volume"]["h24"])
        liquidity = float(pair["liquidity"]["usd"])
        total_supply = float(pair["baseToken"].get("totalSupply", 0))
        price_change_1h = float(pair["priceChange"]["h1"])
        price_change_6h = float(pair["priceChange"]["h6"])
        holders = int(pair["baseToken"].get("holders", 0))
        whale_buys = int(pair["whaleTrades"]["buy"])
        whale_sells = int(pair["whaleTrades"]["sell"])

        # Hitung market cap
        market_cap = price * total_supply

        # Hitung rasio indikator tambahan
        volume_to_market_cap_ratio = volume / market_cap if market_cap > 0 else 0
        whale_buy_sell_ratio = (whale_buys / (whale_sells + 1))  
        liquidity_to_volume_ratio = liquidity / (volume + 1)  

        # Inisialisasi skor
        score = 0

        # **Indikator**
        if whale_buys > 5:  
            score += 4  
        if holders > 1000:  
            score += 3  
        if volume > 500_000:
            score += 3  
        if liquidity > 100_000:
            score += 2  
        if market_cap < 5_000_000:
            score += 1  
        if price_change_1h > 5 and price_change_6h > 10:
            score += 4  
        if whale_buy_sell_ratio > 2:  
            score += 3  
        if liquidity_to_volume_ratio > 0.5:  
            score += 3  

        # Hanya ambil koin dengan skor minimal 8 dan market cap < 10 juta
        if market_cap < 10_000_000 and score >= 8:
            scored_coins.append({
                "name": name,
                "address": token_address,
                "price": price,
                "volume": volume,
                "liquidity": liquidity,
                "market_cap": market_cap,
                "score": score
            })

    # Urutkan berdasarkan skor tertinggi
    scored_coins.sort(key=lambda x: x["score"], reverse=True)

    return scored_coins
