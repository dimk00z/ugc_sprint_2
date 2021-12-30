## UGC Service

OpenAPI: [http://localhost/api/v1/docs](http://localhost/api/v1/docs)

**Setup**
1. Create .env file with sample:

`$ mv env.sample .env`

`$ vi .env`

**Run project without tests on single machine**

`$ docker-compose up --build -d`

**Run project on sharded MongoDB**

`$ docker-compose -f docker-compose.prod.yml up --build -d`

`$ chmod +x ./mongo-init.sh`

`$ ./mongo-init.sh`


**Testing**

`$ docker-compose --profile=testing up --build`

 - Clear docker containers with all data:
 
`$ docker-compose down -v`

`$ docker-compose -f docker-compose.prod.yml down -v`
