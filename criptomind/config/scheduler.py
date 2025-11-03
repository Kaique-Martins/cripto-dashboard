import schedule
import time
from datetime import datetime
from scripts.fetch_cryptos import fetch_cryptos
from scripts.analyze_cryptos import analyze_data

def job():
    print(f"\n⏰ Atualizando dados - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    df = fetch_cryptos()
    analyze_data(df)
    with open("data/logs.txt", "a") as f:
        f.write(f"[{datetime.now()}] Atualização concluída.\n")

schedule.every().day.at("09:00").do(job)

print("🔁 Scheduler iniciado...")
while True:
    schedule.run_pending()
    time.sleep(60)
