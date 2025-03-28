# wildapies

Парсер информации о товарах с Wildberries

## Установка
```bash
pip install wildapies
```
или
```bash
python3 -m pip install wildapies
```
## Использование
```python
import wildapies as wb

data = wb.getinfo("https://www.wildberries.ru/catalog/12345678/detail.aspx")
print(data)
```