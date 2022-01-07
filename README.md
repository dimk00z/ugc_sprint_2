# Проектная работа 9 спринта

[https://github.com/dimk00z/ugc_sprint_2](https://github.com/dimk00z/ugc_sprint_2)


В рамках спринта были реализованы следующие задачи:

1. Реализовано API для лайков, рейтингов  `ugcmongo`. 
Подробное описание в директории [ugcmongo](https://github.com/dimk00z/ugc_sprint_1/tree/main/ugcmongo)

2. Реализован [ELK](https://github.com/dimk00z/ugc_sprint_1/tree/main/ELK).

3. Добавлены проверки для github actions [workflow.yml](https://github.com/dimk00z/ugc_sprint_2/blob/main/.github/workflows/workflow.yml).

4. Проведено исследование скорости работы хранилища MongoDB (`ugcmongo/research`):

- При помощи скрипта `generator.py` создается набор данных в запущенном ugcmongo сервисе (10к фильмов, 50к пользователей, 200к отзывов, 500к голосов, 300к закладок).
- Скриптом `saver.py` делается случайная выборка записей по всем созданным коллекциям (по 1000 из каждой).
- Сервисом Locust проводится нагрузочное тестирование по случайной выборке.
- Результаты тестов хорошие: при 50 пользователях и 400+ rps медианная скорость не превышает 200 мс (Macbook Air M1 8Gb). 

### Выполнили

- [Дмитрий Кузнецов](https://github.com/dimk00z)
- [Вера Герасимович](https://github.com/weraleto)
- [Сергей Сименштейн](https://github.com/simenshteyn)
