# PPP Flask Application

## <span style="color:green">How to run?</span>

To build up the app, we need to run the deployment bash script.
This file will deploy the infrastructure and deploy all the code needed with ansible.
```bash
bash deployment.sh
```

All needed variables need to be set in the group_vars/all file. We use a sed that uses predefined environment variables. But these can also be set manually in the terminal.

This will be used by Ansible to fill in the templates and tasks.

Then we can finally move on with the full software deployment by invoking the Ansible Playbooks.
```bash
cd ansible
ansible-playbook -i hosts machine_initial_setup.yml
ansible-playbook -i hosts install_nginx_supervisor.yml
ansible-playbook -i hosts install_app.yml
```

---
## <span style="color:green">Infrastructure</span>

### <span style="color:lightgreen">Network Security Group</span>

First of all we need to set up the Network Security Group that will be attached to the Virtual Machine. This allows inbound traffic from port 22 (ssh), 80 (http) and 443 (https).

### <span style="color:lightgreen">Virtual Machine</span>

The virtual machine runs a flask app using gunicorn and supervisor to run it as a background job. The app allows the search of materials through two different gateways. One is using an Azure SQL Database to query pre-calculated clusters. The other one is using a deployed model in Azure Machine Learning to get the closest materials to a query.

### <span style="color:lightgreen">Public IP Address</span>
In order to get an ssl certificate, we need to assign a static public IP address to the virtual machine. This is all done when deploying the virtual machine.

---
## <span style="color:green">Software</span>

For this project we use Flask to build up the app code, together with several other libraries to create the authentication, users database and forms. The code is running with gunicorn that is better for running apps in production since it is more reliable. Supervisor runs the gunicorn command in the background so it is kept running whenever the system is on.

### <span style="color:lightgreen">Ansible</span>

The ansible consists of three roles, one for initial machine deployment, another to set up the nginx listening to HTTP and supervisor for background jobs, and a last one to deploy the actual APP which comes from this same repository.
Credentials and Keys need to be handled with care.

### <span style="color:lightgreen">NGINX Configuration</span>

Nginx takes all requests at a specified port, in this case 80 HTTP and 443 HTTPS. All the requests at 80 are forwarded to HTTPS for secure encrypted connection.

I use the LetsEncrypt package to certify my domain. They are referenced in the Nginx configuration file, which are added when deploying the certification.

```nginx
events {
  worker_connections  4096;  ## Default: 1024
}

http { 
    server {
        listen       80;
        server_name {{ domain_name }} *.{{ domain_name }};

        location / {
            return 301  https://{{ domain_name }}$request_uri;
        }

    }
    server {
        server_name {{ domain_name }} *.{{ domain_name }};
        listen 443 ssl;

        # certbot will modify this when it is installed
        
        include /etc/nginx/conf.d/*.conf;
    }
}
```
*/etc/nginx/nginx.conf*


The server is then configured to forward all requests and receive answers from a specified host IP and local Port.

```nginx
location / {
        proxy_pass http://127.0.0.1:{{ local_port }};
        proxy_redirect off;
        # Redefine the header fields that NGINX sends to the upstream server
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
}
```
*/etc/nginx/conf.d/api.conf*

### <span style="color:lightgreen">APP</span>

The APP itself is in this same repository. After cloning it to the virtual machine we proceed with the following steps:
1. Create virtual environment
2. Install requirements.txt
3. Install gunicorn

This way the supervisor will be able to access the gunicorn executable and run the api service.

### <span style="color:lightgreen">Supervisor Configuration</span>

Supervisor in this project is used to ensure the reliable job execution of the Flask service in the background. To do this we only have to specify the service configuration file and reload the Supervisor service.

```
[program:{{ api_name }}]
command=/home/ubuntu/{{ api_name }}/venv/bin/gunicorn -b localhost:{{ local_port }} -w 4 search_app:app
directory=/home/ubuntu/{{ api_name }}
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
*/etc/supervisor/conf.d/search_app.conf*

### <span style="color:lightgreen">Post Deployment Configuration</span>

Before being able to log in, it is needed to set up at least one user in the users database.
```bash
# First we create the Users table in a SQLlite db
flask db upgrade
# We go into flask shell to log in
flask shell
```

Once we are using python in the Flask environment, we can submit a new user to the database.
```python
u = User(username="user", email="user@example.pt")
u.set_password("password123!")
db.session.add(u)
db.session.commit()
```

We can then use the user created username and password to log in to the app.

## <span style="color:green">Search App Application</span>

The application is a simple search application that makes use of two other projects:
1. An Azure SQL Database with material_proximity table that contains the 10 closest materials to each material using a distance calculation.
2. An Azure Machine Learning deployed model that returns the 10 closest materials to a search query.

After logging in, the user can select the type of search he wants, write in the query box, and click submit to get the top 10 results.