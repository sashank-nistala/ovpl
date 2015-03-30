test: stop-server
	python http_logging/http_logging_server.py &
	python2 adapters/AdapterServer.py &
	python2 ControllerServer.py &

start-server:
	python http_logging/http_logging_server.py &
	python2 adapters/AdapterServer.py &
	python2 Controller.py &
stop-server:
	-killall python2 #HACK!
	-killall python #HACK!

server-ip:
	@ps aux | grep py

restart-server: stop-server start-server


start-mongodb:
	service mongod start

repair-mondodb:
	service mongod stop
	mongod --repair
	service mongod start
