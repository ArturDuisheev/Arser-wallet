## Инструкция по запуску

Для запуска нод необходимо указать команду
~~~
docker compose up -d --build
~~~

После запуска нод необходимо провести дополнительные работы

### monero 

Т.к запуск monero средствами docker и docker-compose невозможны (запуск monero останавливается), необходимо указать комманды вручную

1 Получить список контейнеров
```
docker ps
```
2 Найти идентификатор контейнера monero и указать команду
```
docker exec -it <id контейнера> ./monerod --testnet --rpc-bind-ip 0.0.0.0 --rpc-bind-port 28081 --confirm-external-bind
```
После запуска monero необходимо создать кошелек \
3 
```
./monero-wallet-cli --password <ваш пароль> --generate-new-wallet <название кошелька> --daemon-port 28081
```
4 В открывшемся меню выбрать язык \
После этого необходимо создать rpc клиент

5 
```
./monero-wallet-rpc --rpc-bind-port 28088 --wallet-file <название кошелька> --password <пароль кошелька> --testnet
```

