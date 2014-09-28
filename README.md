# Start:

 - get telegram-cli ( [vysheng/tg](https://github.com/vysheng/tg) )
 - ./configure && make it
 - start it normally to get authenticated (bin/telegram-cli -k ../tg-server.pub)
 - start it in deamon mode ( bin/telegram-cli -k ../tg-server.pub -C -R -N -d -P 9012 )
 - start TelegramClient.py (currently testes with python 2.7.7)
