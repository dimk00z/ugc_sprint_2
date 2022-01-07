## MongoDB Research

**Research Setup**

1. Run project on shared MongoDB**

`$ docker-compose -f docker-compose.prod.yml up --build -d`

`$ chmod +x ./mongo-init.sh`

`$ ./mongo-init.sh`

2. Generate data and load on shared MongoDB.

`$ cd ugcmongo/research`

`$ python generator.py`

Uploading takes some time, default amount could be changed in source code.
You can check progress with MongoDB Compass.

3. Extract random records and save to JSON-files.

`$ python saver.py`

4. Run locust to test performance: 

`$ locust`

- Open [http://0.0.0.0:8089](http://0.0.0.0:8089)
- Fill number of users (for example, 50) and host (`http://localhost`)
- Start swarming
