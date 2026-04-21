# Hog GUI 部署到 DigitalOcean（y3y3yy3.me）

下面按 Ubuntu 22.04+ 说明。

## 1) 在服务器准备代码

```bash
cd /var/www
sudo git clone https://github.com/Y3ahman/CS61A-Assignments.git
cd CS61A-Assignments/Project/hog
```

## 2) 创建 Python 虚拟环境并启动服务

```bash
sudo apt update
sudo apt install -y python3 python3-venv nginx
python3 -m venv .venv
source .venv/bin/activate
python3 hog_gui.py
```

默认监听 `0.0.0.0:31415`，先确认：

```bash
curl http://127.0.0.1:31415/health
```

## 3) 配置 systemd（后台常驻）

创建 `/etc/systemd/system/hog-gui.service`：

```ini
[Unit]
Description=Hog GUI Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/CS61A-Assignments/Project/hog
Environment=HOG_GUI_PORT=31415
ExecStart=/var/www/CS61A-Assignments/Project/hog/.venv/bin/python3 /var/www/CS61A-Assignments/Project/hog/hog_gui.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hog-gui
sudo systemctl status hog-gui
```

## 4) 配置 Nginx 反向代理到域名

创建 `/etc/nginx/sites-available/y3y3yy3.me`：

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

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/y3y3yy3.me /etc/nginx/sites-enabled/y3y3yy3.me
sudo nginx -t
sudo systemctl reload nginx
```

## 5) 开启 HTTPS（推荐）

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d y3y3yy3.me -d www.y3y3yy3.me
```

## 6) DNS 检查

在域名 DNS 面板确保：

- `@` A 记录 -> 你的 DO Droplet 公网 IP
- `www` A 记录 -> 同一个公网 IP

## 7) 更新发布流程

```bash
cd /var/www/CS61A-Assignments
sudo git pull
cd Project/hog
sudo systemctl restart hog-gui
```

