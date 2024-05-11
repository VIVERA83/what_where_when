# Что, где, когда 

___
<span id="0"></span>

### <span id="1">1. </span><span style="color:purple">Описание</span>

Имитация игры одноименно игры "Что, где, когда?" 

### <span id="2">2. </span><span style="color:purple">Служебные команды для запуска</span> 

Монтировать образ
```bash
docker build -t ii_clicker_lb .
```
Запуск приложения в docker контейнере
```bash
docker run --rm --name ii_clicker_lb  vivera83/ii_labor_protect:1
```

```bash
docker build -t vivera83/ii_labor_protect:1 .
```


```bash
docker push vivera83/ii_labor_protect:1
```  


```bash
cd app 
alembic init -t async alembic
```


```bash
cd app 
alembic revision --autogenerate -m "Initial tables"
```
```bash
cd app
alembic upgrade head
```
```
docker run -d -p 6378:6378 --name myredis redis
```