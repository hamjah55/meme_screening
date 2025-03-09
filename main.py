import time
from modules.scanner import get_scored_memecoins
from modules.telegram_bot import send_telegram_message

def run_bot():
    """Menjalankan bot untuk scanning dan mengirimkan 5 koin terbaik ke Telegram"""
    while True:
        memecoins = get_scored_memecoins()

        if memecoins:
            # Ambil hanya 5 koin dengan skor tertinggi
            top_coins = memecoins[:5]

            message = "🔥 *5 Memecoin Potensial Tertinggi!* 🔥\n\n"
            for coin in top_coins:
                message += (
                    f"📌 *{coin['name']}*\n"
                    f"💰 Harga: ${coin['price']:.6f}\n"
                    f"📊 Volume 24H: ${coin['volume']:,}\n"
                    f"💦 Likuiditas: ${coin['liquidity']:,}\n"
                    f"🏦 Market Cap: ${coin['market_cap']:,}\n"
                    f"🔢 Skor: {coin['score']}/10\n"
                    f"🔗 [Lihat di DexScreener](https://dexscreener.com/solana/{coin['address']})\n\n"
                )

            send_telegram_message(message)
        else:
            send_telegram_message("❌ Tidak ada koin potensial ditemukan saat ini.")

        time.sleep(600)  # Tunggu 10 menit sebelum scan lagi

if __name__ == "__main__":
    run_bot()
