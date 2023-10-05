# Реализация отправки сообщений с помощью брокера сообщений RabbitMQ

В данной реализации продюсер создает:
* exchanger с именем `routing`
* добавляет в этот exchanger два `routing_key` - "both" и "paymentsonly"
  * сообщения с `routing_key` == "both" попадает во все консюмеры,
  * сообщения с `routing_key` == "paymentsonly" попадает только в консюмер который слушает соответствующий `routing_key`
* декларируется очередь по имени `byturn`, которую слушают все консюмеры, но берут сообщения из очереди по очереди

Консюмеры:
* user_consumer:
  * подключен к exchanger `routing` и слушает два `routing_key` - "useronly" и "both"
  * подписан на очередь "byturn"

* analytics_consumer:
  * подключен к exchanger `routing` и слушает два `routing_key` - "analyticsonly" и "both"
  * подписан на очередь "byturn"

* payments_consumer:
  * подключен к exchanger `routing` и слушает два `routing_key` - "paymentsonly" и "both"
  * подписан на очередь "byturn"


Таким образом продюсер может:
* отсылать сообщения напрямую в нужный консюмер указав нужный `routing_key` (useronly, analyticsonly, paymentsonly)
* отсылать сообщения которые попадут во все консюмеры если они все слушают одинаковый `routing_key` (both)
* отсылать сообщения в очередь, из котороый консюмеры, подписанные на эту очередь, будут брать сообщения по очереди


```plantuml
@startuml
participant "Producer" as Producer
participant "Exchanger" as Ex
queue "Queue" as Q
participant "Products_Consumer" as PC
participant "Analytics_Consumer" as AC


alt #LimeGreen routing_key == "products"
note over Producer, PC : Создается сообщение, которое должен получить консюмер, подписанный на rouring_key = "products"

PC --> Q : Создает анонимную очередь
PC --> Ex : Проверяет Exchanger на наличие сообщений с соответствующим routing_key = "products"
Producer --> Ex : Сообщение с routing_key = "products"
end

alt #LimeGreen в Exchanger появляется сообщение с routing_key = "products"
Ex --> Q : В созданную консюмером анонимную очередь передается сообщение
Q --> PC : Консюмер забирает сообщение
end


alt #OliveDrab routing_key == "analytics"
note over Producer, AC : Создается сообщение, которое должен получить консюмер, подписанный на rouring_key = "analytics"

AC --> Q : Создает анонимную очередь
AC --> Ex : Проверяет Exchanger на наличие сообщений с соответствующим routing_key = "analytics"
Producer --> Ex : Сообщение с routing_key = "products"
end

alt #OliveDrab в Exchanger появляется сообщение с routing_key = "analytics"
Ex --> Q : В созданную консюмером анонимную очередь передается сообщение
Q --> AC : Консюмер забирает сообщение
end


alt #GreenYellow routing_key == "all"
note over Producer, AC : Создается сообщение, которое должны получить все консюмеры, подписанные на rouring_key = "all"

AC --> Q : Создает анонимную очередь
PC --> Q : Создает анонимную очередь
AC --> Ex : Проверяет Exchanger на наличие сообщений с соответствующим routing_key = "all"
PC --> Ex : Проверяет Exchanger на наличие сообщений с соответствующим routing_key = "all"
Producer --> Ex : Сообщение с routing_key = "all"
end

alt #GreenYellow в Exchanger появляется сообщение с routing_key = "all"
Ex --> Q : В созданные консюмерами анонимные очереди передается сообщение
note over Ex, AC : Все консюмеры подписанные на routing_key == "all" забирают сообщение

Q --> PC : Консюмер забирает сообщение
Q --> AC : Консюмер забирает сообщение
end


alt #Gold queue == "publicqueue"
note over Producer, AC : Создается сообщение, которое должны получить все консюмеры, подписанные на очередь = "publicqueue"

AC --> Q : Подписывается на очередь "publicqueue"
PC --> Q : Подписывается на очередь "publicqueue"
note over Producer, AC : Все консюмеры подписанные на очередь "publicqueue", по очереди, забирают сообщения из этой очереди

Producer --> Ex : Сообщение в очередь = "publicqueue"
Q --> PC : Забирает сообщение
Producer --> Ex : Сообщение в очередь = "publicqueue"
Q --> AC : Забирает сообщение
end

@enduml
```
