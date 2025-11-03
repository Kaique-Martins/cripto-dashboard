from scripts.fetch_cryptos import fetch_cryptos
from scripts.analyze_cryptos import analyze_data
from scripts.predict_trends import predict_trends

if __name__ == "__main__":
    print("🚀 Iniciando coleta de dados...")
    df = fetch_cryptos()
    print("✅ Dados coletados!")

    print("\n📊 Analisando dados...")
    analyze_data(df)
    print("✅ Análise concluída!")
    
    df = fetch_cryptos()
    analyze_data(df)
    prediction = predict_trends(df)
    print(f"\n🔮 Previsão de preço médio para o próximo dia: ${prediction:.2f}")