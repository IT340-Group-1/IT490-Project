sudo docker run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
sleep 15
sudo docker exec -i rabbitmq /bin/sh -c "rabbitmqctl add_user db password"
sudo docker exec -i rabbitmq /bin/sh -c "rabbitmqctl set_permissions -p / db '.*' '.*' '.*'"
sudo docker exec -i rabbitmq /bin/sh -c "rabbitmqctl add_user fe password"
sudo docker exec -i rabbitmq /bin/sh -c "rabbitmqctl set_permissions -p / fe '.*' '.*' '.*'"
sudo docker exec -i rabbitmq /bin/sh -c "rabbitmqctl add_user be password"
sudo docker exec -i rabbitmq /bin/sh -c "rabbitmqctl set_permissions -p / be '.*' '.*' '.*'"

# sudo docker kill rabbitmq