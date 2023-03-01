ssh -i ~/.ssh/cra_ssh_key.pem ubuntu@$(<../backend/ip.txt) "bash -s" <<"ENDSSH"
<<<<<<< HEAD
  cd ~/IT490-Project/backend
=======
  cd ~/Project/IT490-Project/backend
>>>>>>> d6d95928594f9765e8024d088ebe022cbe5fd824
  nohup python3 -m bermq > bermq.out 2>&1 </dev/null &
ENDSSH

ssh -i ~/.ssh/cra_ssh_key.pem ubuntu@$(<../database/ip.txt) "bash -s" <<"ENDSSH"
<<<<<<< HEAD
  sudo systemctl start mysql.service
=======
  sudo service mysql start
>>>>>>> d6d95928594f9765e8024d088ebe022cbe5fd824
  cd ~/IT490-Project/database
  nohup python3 dbrmq.py > dbrmq.out 2>&1 </dev/null &
ENDSSH

ssh -i ~/.ssh/cra_ssh_key.pem ubuntu@$(<../frontend/ip.txt) "bash -s" <<"ENDSSH"
<<<<<<< HEAD
  cd ~/IT490-Project/frontend
=======
  cd ~/Project/IT490-Project/frontend
>>>>>>> d6d95928594f9765e8024d088ebe022cbe5fd824
  nohup /home/ubuntu/.local/bin/gunicorn --workers 4 --bind 0.0.0.0:7007 'craui:create_app()' > craui.out 2>&1 </dev/null &
ENDSSH
