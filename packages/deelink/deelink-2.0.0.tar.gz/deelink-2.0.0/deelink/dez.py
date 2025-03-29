import requests

def print_banner():
    print("=== Deelink - Конвертер Deezer-ссылок ===")
    print("Автор: Avinion")
    print("Telegram: @akrim")
    print("=" * 40 + "\n")

def convert_deezer_link(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        final_url = response.url
        
        base_url = "https://www.deezer.com"
        track_id = final_url.split("/track/")[-1].split("?")[0]
        clean_url = f"{base_url}/track/{track_id}"
        
        return {
            "original": short_url,
            "final_url": final_url,
            "clean_url": clean_url
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    print_banner()
    print("Вставьте короткую ссылку (например, https://dzr.page.link/LRUfLcTwaZ13SGaA9)")
    print("Для выхода введите 'exit' или нажмите Ctrl+C\n")
    
    while True:
        short_url = input("> ").strip()
        
        if not short_url:
            print("Введите ссылку или 'exit' для выхода.")
            continue
        
        if short_url.lower() == 'exit':
            print("\nРабота скрипта завершена.")
            break
        
        if "dzr.page.link" not in short_url:
            print("❌ Ошибка: Это не короткая Deezer-ссылка! Попробуйте ещё раз.")
            continue
        
        result = convert_deezer_link(short_url)
        
        if "error" in result:
            print(f"❌ Ошибка: {result['error']}")
        else:
            print("\n🔗 Результат:")
            print(f"• Оригинальная ссылка: {result['original']}")
            print(f"• После редиректа: {result['final_url']}")
            print(f"• Чистая ссылка: {result['clean_url']}\n")
        
        print("Введите новую ссылку или 'exit' для выхода.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nРабота скрипта завершена.")