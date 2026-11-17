# ЧистоДім — інтернет-магазин (Django)

Побутова хімія, підгузки, засоби гігієни. Каталог, пошук, фільтри, кошик, оформлення замовлення, обране, реєстрація/вхід, кабінет з історією замовлень, адмінка. Адаптивний дизайн для телефона.

## Запуск у PyCharm
1. `git pull`, відкрийте папку `shop/` як проєкт.
2. Settings → Python Interpreter → Add → Virtualenv (Python 3.11+).
3. У терміналі PyCharm:
   ```
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed        # демо-товари + адмін admin / admin12345
   python manage.py runserver 0.0.0.0:8000
   ```
4. Сайт: http://127.0.0.1:8000 · Адмінка: http://127.0.0.1:8000/admin
5. **З телефона:** телефон у тій самій Wi-Fi мережі → відкрийте `http://<IP вашого компʼютера>:8000` (IP: `ipconfig` у Windows).

Змініть пароль адміна одразу після першого входу.

## Тести
`python manage.py test store`

## Що де
- `store/models.py` — Категорія, Товар, Обране, Замовлення.
- `store/cart.py` — кошик у сесії (працює без входу).
- `store/admin.py` — адмінка: редагування ціни/залишку прямо в списку, статуси замовлень.
- `store/templates/`, `store/static/store/style.css` — дизайн.

## Перед публікацією
Задайте змінні `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS=ваш-домен`, запустіть `collectstatic`, використовуйте PostgreSQL замість SQLite.
