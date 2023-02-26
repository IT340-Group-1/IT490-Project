ssh -i "cra_ssh_key.pem" ubuntu@$(<../backend/ip.txt) "bash -s" <<"ENDSSH"
  cd ~/IT490-Project/backend
  nohup python3 -m bermq > bermq.out 2>&1 </dev/null &
ENDSSH

ssh -i "cra_ssh_key.pem" ubuntu@$(<../database/ip.txt) "bash -s" <<"ENDSSH"
  sudo systemctl start mysql.service
  cd ~/IT490-Project/database
  nohup python3 dbrmq.py > dbrmq.out 2>&1 </dev/null &
ENDSSH

ssh -i "cra_ssh_key.pem" ubuntu@$(<../frontend/ip.txt) "bash -s" <<"ENDSSH"
  cd ~/IT490-Project/frontend
  nohup /home/ubuntu/.local/bin/gunicorn --workers 4 --bind 0.0.0.0:7007 'craui:create_app()' > craui.out 2>&1 </dev/null &
ENDSSH