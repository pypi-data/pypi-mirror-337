from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import logging

def getinfo(url):
    # Настройки Chrome (без интерфейса + защита от обнаружения)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    service = webdriver.ChromeService(service_args=['--disable-logging'])
    driver = webdriver.Chrome(options=options, service=service)
    
    try:
        driver.get(url)
        
        # Функция для безопасного поиска элемента
        def find_element_safe(xpath):
            try:
                return driver.find_element(By.XPATH, xpath).text.strip()
            except NoSuchElementException:
                return None

        # Получение данных
        name = find_element_safe('/html/body/div[1]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[1]/h1')
        price = find_element_safe('/html/body/div[1]/div/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span')
        
        # Обработка рейтинга (если есть)
        rating_text = find_element_safe('/html/body/div[1]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[2]/div[1]/a/div')
        rating = rating_text.split('•')[0].strip() if rating_text else "Рейтинг не найден"
        
        # Получение продавца
        seller = find_element_safe('/html/body/div[1]/div/div[1]/div[5]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/a') or "Продавец не найден"

        return {
            "name": name or "Название не найдено",
            "price": clean_price(price) if price else "0",
            "rating": rating,
            "brand": seller,
            "url": url
        }

    except Exception as e:
        return {"Ошибка": str(e)}
    finally:
        driver.quit()
        
def clean_price(price_str: str) -> str:
    """Очистка строки с ценой. Возвращает число в виде строки или '0' при ошибке."""
    if not price_str:
        return "0"
    
    cleaned = ''.join(c for c in price_str if c.isdigit() or c in {'.', ','})
    cleaned = cleaned.replace(',', '.')
    
    try:
        return str(int(round(float(cleaned))))
    except (ValueError, TypeError):
        return "0"