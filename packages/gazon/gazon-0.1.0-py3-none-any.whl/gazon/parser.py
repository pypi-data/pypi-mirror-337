from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def getinfo(url):
    # Настройки Chrome (без интерфейса + защита от обнаружения)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Ожидание загрузки динамического контента

        # Получение названия товара
        name_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[1]/h1'))
        )
        name = name_element.text.strip()

        # Получение цены
        price_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[3]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/button/span/div/div[1]/div/div/span'))
        )
        price = price_element.text.strip()

        # Получение рейтинга (если есть)
        try:
            rating_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[3]/div[3]/div[1]/div[1]/div[2]/div/div/div/div[2]/div[1]/a/div'))
            )
            rating_text = rating_element.text.strip()
            # Обрезаем всё после •
            rating = rating_text.split('•')[0].strip()
        except:
            rating = "Рейтинг не найден"

        # Получение продавца
        try:
            seller_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[5]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/a'))
            )
            seller = seller_element.text.strip()
        except:
            seller = "Продавец не найден"

        return {
            "name": name,
            "price": price,
            "rating": rating,
            "brand": seller,
            "url": url
        }

    except Exception as e:
        return {"Ошибка": str(e)}
    finally:
        driver.quit()
