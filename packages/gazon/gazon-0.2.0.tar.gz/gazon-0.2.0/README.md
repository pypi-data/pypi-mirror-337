# wildapies

Парсер информации о товарах с Ozon

## Установка
```bash
pip install gazon
```
или
```bash
python3 -m pip install gazon
```
## Использование
```python
import gazon as ozon

data = ozon.getinfo("https://www.ozon.ru/product/1577622901/") # также поддерживаются и полные ссылки(https://www.ozon.ru/product/internet-kabel-patch-kord-1m-100mbit-sek-1577622901/)
print(data)
```