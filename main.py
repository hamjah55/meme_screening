import time
from datetime import datetime
from modules.scanner import get_scored_memecoins
from modules.telegram_bot import send_telegram_message

def run_bot():
    """Menjalankan bot untuk scanning dan mengirimkan 5 koin terbaik ke Telegram"""
    last_message = ""
    
    while True:
        memecoins = get_scored_memecoins()
        
        if memecoins:
            # Ambil hanya 5 koin dengan skor tertinggi
            top_coins = memecoins[:5]

            current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            message = f"🔥 *5 Memecoin Potensial Tertinggi!* 🔥\n\n🕒 Update: {current_time} UTC\n\n"
            
            for coin in top_coins:
                message += (
                    f"📌 *{coin['name']}*\n"
                    f"💰 Harga: ${coin['price']:.6f}\n"
                    f"📊 Volume 24H: ${coin['volume']:,}\n"
                    f"💦 Likuiditas: ${coin['liquidity']:,}\n"
                    f"🏦 Market Cap: ${coin['market_cap']:,}\n"
                    f"👥 Holders: {coin['holders']}\n"
                    f"🐋 Whale (≥1% supply): {coin['whale_count']}\n"
                    f"🔢 Skor: {coin['score']}/10\n"
                    f"🔗 [Lihat di DexScreener](https://dexscreener.com/solana/{coin['address']})\n\n"
                )
            
            if message != last_message:
                send_telegram_message(message)
                last_message = message
            else:
                print("🔄 Data belum berubah, tidak mengirim pesan baru.")
        else:
            send_telegram_message("❌ Tidak ada koin potensial ditemukan saat ini.")
        
        time.sleep(600)  # Tunggu 10 menit sebelum scan lagi

if __name__ == "__main__":
    run_bot()
