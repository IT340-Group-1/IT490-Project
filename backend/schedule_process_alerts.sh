echo "0 8 * * * cd /home/ubuntu/IT490-Project/backend && python3 process_alerts.py" > crontab_new
crontab crontab_new
rm crontab_new

# crontab -l
# crontab -r