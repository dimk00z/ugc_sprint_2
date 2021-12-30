#!/bin/bash
echo "1. Настройка серверов конфигурации"
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongo'
sleep 3

echo "2. Сборка набора реплик первого шарда"
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongo'
sleep 15

echo "3. Добавление первого шарда в маршрутизатор"
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongo'
sleep 3

echo "4. Сборка набора реплик первого шарда"
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongo'
sleep 6

echo "5. Добавление второго шарда в маршрутизатор"
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongo'
sleep 3

echo "6. Создание базы данных"
docker exec -it mongors1n1 bash -c 'echo "use films" | mongo'
sleep 3

echo "7. Включение шардирования базы данных"
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"films\")" | mongo'
sleep 3

echo "8. Создание коллекций"
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"films.votes\")" | mongo'
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"films.reviews\")" | mongo'
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"films.bookmarks\")" | mongo'
sleep 3

echo "9. Настройка шардирования по полю"
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"films.votes\", {\"movie_id\": \"hashed\"})" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"films.reviews\", {\"movie_id\": \"hashed\"})" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"films.bookmarks\", {\"user_id\": \"hashed\"})" | mongo'