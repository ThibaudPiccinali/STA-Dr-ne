SERV 	:= ./src/server.c ./src/messagerie.c ./src/drone.c
USR		:= ./src/clientUser.c ./src/messagerie.c ./src/drone.c
DRONE 	:= ./src/clientDrone.c ./src/messagerie.c ./src/drone.c
OPT := 

all: 
	gcc $(OPT) $(SERV) -lm -lpthread -o ./bin/server
	gcc $(OPT) $(USR) -lm -o ./bin/user
	gcc $(OPT) $(DRONE) -lm -o ./bin/drone
	
server:
	gcc $(OPT) $(SERV) -lm -lpthread -o ./bin/server

drone:
	gcc $(OPT) $(DRONE) -lm -o ./bin/drone

user:
	gcc $(OPT) $(USR) -lm -o ./bin/user

clean:
	rm ./bin/*