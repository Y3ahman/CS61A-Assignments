# Deploy Hog GUI on DigitalOcean (`y3y3yy3.me`)

These steps assume Ubuntu 22.04+ on your DO Droplet.

## 1) Prepare code on server

```bash
sudo useradd --system --create-home --home-dir /home/hog-gui --shell /usr/sbin/nologin hog-gui
sudo mkdir -p /srv
cd /srv
sudo git clone https://github.com/Y3ahman/CS61A-Assignments.git
sudo chown -R hog-gui:hog-gui /srv/CS61A-Assignments
cd /srv/CS61A-Assignments/Project/hog
```

## 2) Install runtime and test locally

```bash
sudo apt update
sudo apt install -y python3 python3-venv nginx
python3 -m venv .venv
source .venv/bin/activate
python3 hog_gui.py
```

By default it listens on `127.0.0.1:31415`. Check:

```bash
curl http://127.0.0.1:31415/health
```

## 3) Configure systemd service

Create `/etc/systemd/system/hog-gui.service`:

```ini
[Unit]
Description=Hog GUI Service
After=network.target

[Service]
Type=simple
User=hog-gui
Group=hog-gui
WorkingDirectory=/srv/CS61A-Assignments/Project/hog
Environment=HOG_GUI_PORT=31415
Environment=HOG_GUI_HOST=127.0.0.1
ExecStart=/srv/CS61A-Assignments/Project/hog/.venv/bin/python3 /srv/CS61A-Assignments/Project/hog/hog_gui.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hog-gui
sudo systemctl status hog-gui
```

## 4) Configure Nginx reverse proxy

Create `/etc/nginx/sites-available/y3y3yy3.me`:

```nginx
server {
    listen 80;
    server_name y3y3yy3.me www.y3y3yy3.me;

    location / {
        proxy_pass http://127.0.0.1:31415;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/y3y3yy3.me /etc/nginx/sites-enabled/y3y3yy3.me
sudo nginx -t
sudo systemctl reload nginx
```

## 5) Enable HTTPS (recommended)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d y3y3yy3.me -d www.y3y3yy3.me
```

## 6) DNS records

In your domain DNS panel:

- `@` A record -> your DO Droplet public IP
- `www` A record -> same public IP

## 7) Update release later

```bash
cd /srv/CS61A-Assignments
sudo -u hog-gui git pull
sudo systemctl restart hog-gui
```

If `git pull` asks for credentials, configure one of these first:

- SSH deploy key for `hog-gui` user
- GitHub PAT credential helper on server
- Run pull as an admin user that already has repository access
