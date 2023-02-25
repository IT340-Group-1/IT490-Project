# Multiple attempts to install RabbitMQ following the instructions
# at https://www.rabbitmq.com/install-debian.html failed due to
# dependency issues that have not been resolved.
# 
# In order to not block everything that depends on RabbitMQ (everything else),
# we will use the community Docker image
# (https://registry.hub.docker.com/_/rabbitmq/), and must install Docker.

sudo apt install docker.io
