#!/bin/bash
#
# Deployment of Flask App

# Create security group
az network nsg create --name myNSG -o none
az network nsg rule create \
   --nsg-name myNSG \
   --name myNSGruleSSH \
   --protocol tcp \
   --priority 1000 \
   --destination-port-range 22 \
   --access allow \
   -o none

az network nsg rule create \
   --nsg-name myNSG \
   --name myNSGruleHTTP \
   --protocol tcp \
   --priority 1001 \
   --destination-port-range 80 \
   --access allow \
   -o none

az network nsg rule create \
   --nsg-name myNSG \
   --name myNSGruleHTTPS \
   --protocol tcp \
   --priority 1002 \
   --destination-port-range 443 \
   --access allow \
   -o none

# Create VM with Static IP
az vm create \
    --name "ppp_app" \
    --image UbuntuLTS \
    --admin-username mota-engil \
    --generate-ssh-keys \
    --public-ip-address PPPIpAdress \
    --public-ip-address-allocation static \
    --nsg myNSG
    --output none

APP_VM_IP=$(az network public-ip show --name PPPIpAdress --query ipAddress -o tsv)

# Prepare variables to be used in sed
sed_primary_endpoint_key=$(echo $PRIMARY_ENDPOINT_KEY | sed 's/&/\\\&/g;s/\//\\\//g')
sed_scoring_uri=$(echo $SCORING_URI | sed 's/&/\\\&/g;s/\//\\\//g')

# Create the vars file for deploying to the server
sed "s/FLASK_SECRET/${SECRET_KEY}/; \
    s/MAIL_PLACEHOLDER/${MAIL_USERNAME}/; \
    s/MAIL_PWD_PLACEHOLDER/${MAIL_PASSWORD}/; \
    s/AZURE_DB_PLACEHOLDER/$DATABASE/; \
    s/AZURE_SERVER_PLACEHOLDER/${SERVER_NAME}/; \
    s/AZURE_USER_PLACEHOLDER/${LOGIN_INPUT}/; \
    s/AZURE_PWD_PLACEHOLDER/${PASSWORD_INPUT}/; \
    s/AZURE_SURI_PLACEHOLDER/${sed_scoring_uri}/; \
    s/AZURE_EKEY_PLACEHOLDER/${sed_primary_endpoint_key}/; \
    s/APP_DOMAIN_NAME/${APP_DOMAIN_NAME}/; \
    s/SSL_EMAIL/${SSL_EMAIL}/" ansible/group_vars/all_template > ansible/group_vars/all
sed "s/IP/${APP_VM_IP}/" ansible/hosts_template > ansible/hosts

# Run the ansible deployment to set up the code in the machine
cd ansible/
ansible-playbook -i hosts machine_initial_setup.yml
ansible-playbook -i hosts install_nginx_supervisor.yml
ansible-playbook -i hosts install_app.yml



