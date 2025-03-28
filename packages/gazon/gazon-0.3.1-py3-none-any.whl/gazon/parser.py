from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def getinfo(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Ожидаем появления body (макс. 30 сек)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Функция для поиска элемента (возвращает текст или "Не найдено")
        def find_element_text(xpath, element_name="Элемент"):
            try:
                element = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                return element.text.strip()
            except TimeoutException:
                return f"{element_name} не найден"
        
        # Получаем данные (ждём макс. 30 сек, но если есть раньше — берём сразу)
        name = find_element_text(
            "/html/body/div[1]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[1]/h1",
            "Название"
        )
        price = find_element_text(
            "/html/body/div[1]/div/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span",
            "Цена"
        )
        seller = find_element_text(
            "/html/body/div[1]/div/div[1]/div[5]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/a",
            "Продавец"
        )
        
        # Обработка рейтинга (если есть)
        rating_text = find_element_text(
            "/html/body/div[1]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[2]/div[1]/a/div",
            "Рейтинг"
        )
        rating = rating_text.split("•")[0].strip() if "не найден" not in rating_text else "Нет рейтинга"
        
        return {
            "name": name if "не найден" not in name else "Название не указано",
            "price": clean_price(price) if "не найден" not in price else "0",
            "rating": rating,
            "brand": seller if "не найден" not in seller else "Продавец не указан",
            "url": url
        }
        
    except Exception as e:
        return {"Ошибка": str(e)}
    finally:
        driver.quit()

def clean_price(price_str):
    if not price_str or "не найден" in price_str:
        return "0"
    cleaned = ''.join(c for c in price_str if c.isdigit() or c in {'.', ','})
    cleaned = cleaned.replace(',', '.')
    try:
        return str(int(round(float(cleaned))))
    except (ValueError, TypeError):
        return "0"