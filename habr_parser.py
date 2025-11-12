import requests
from bs4 import BeautifulSoup

print("🔍 Парсер статей с Хабра")
print("Загружаем статьи...")

# Слова для поиска
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'игры']

# Адрес сайта
url = 'https://habr.com/ru/articles/'

try:
    # Загружаем страницу
    response = requests.get(url)
    
    # Проверяем успешность
    if response.status_code == 200:
        print("✅ Страница загружена успешно!")
        
        # Читаем HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем все статьи
        articles = soup.find_all('article')
        print(f"📰 Найдено статей на странице: {len(articles)}")
        
        # Счетчик подходящих статей
        found_count = 0
        
        # Проверяем каждую статью
        for article in articles:
            # Ищем заголовок
            title_elem = article.find('h2')
            if title_elem:
                link_elem = title_elem.find('a')
                if link_elem:
                    title = link_elem.text.strip()
                    link = link_elem.get('href', '')
                    
                    # Делаем ссылку полной
                    if link and not link.startswith('http'):
                        link = 'https://habr.com' + link
                    
                    # Ищем дату
                    time_elem = article.find('time')
                    date = time_elem.get('title', '') if time_elem else 'Дата не указана'
                    
                    # Ищем описание статьи
                    preview_elem = article.find('div', class_='article-formatted-body')
                    preview_text = preview_elem.get_text() if preview_elem else ''
                    
                    # Объединяем весь текст для поиска
                    all_text = (title + ' ' + preview_text).lower()
                    
                    # Проверяем ключевые слова
                    for word in KEYWORDS:
                        if word in all_text:
                            found_count += 1
                            print(f"\n🎯 НАЙДЕНА СТАТЬЯ #{found_count}")
                            print(f"📅 Дата: {date}")
                            print(f"📖 Заголовок: {title}")
                            print(f"🔗 Ссылка: {link}")
                            break
        
        if found_count == 0:
            print("\n❌ Статьи по вашим словам не найдены.")
        else:
            print(f"\n✅ Всего найдено статей: {found_count}")
            
    else:
        print(f"❌ Ошибка загрузки. Код: {response.status_code}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("Возможно, нет интернета или сайт недоступен")

print("\n✨ Работа завершена!")
