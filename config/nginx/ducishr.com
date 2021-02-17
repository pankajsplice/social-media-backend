server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name ducishr.com, *.ducishr.com;


    real_ip_header X-Forwarded-For;

    access_log /var/log/nginx/access_d.log;
    error_log /var/log/nginx/error_d.log;

    gzip on;
    gzip_proxied any;
    gzip_static on;
    gzip_types text/plain application/xml application/x-javascript text/javascript text/css application/x-json application/json;

    client_max_body_size 10M;
    keepalive_timeout 5;

    location /static/ {
        alias /opt/apps/ducis_api/public/static/;
        expires max;
    }
    location /media/ {
        alias /opt/apps/ducis_api/media/;
        expires max;
    }

    location / {
        proxy_redirect     off;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;


        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8000;
            break;
       }
   }
}
