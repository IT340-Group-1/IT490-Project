unzip cra_ssh_key.zip -d ~/.ssh/
rm cra_ssh_key.zip
mv ~/.ssh/cra_ssh_key ~/.ssh/cra_ssh_key.pem
chmod 400 ~/.ssh/cra_ssh_key.pem
