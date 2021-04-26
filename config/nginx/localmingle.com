server {
    #listen 80 default_server;
    #listen [::]:80 default_server;
    server_name localmingle.keycorp.in;


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
        alias /opt/apps/local_mingle_backend/public/static/;
        expires max;
    }
    location /media/ {
        alias /opt/apps/local_mingle_backend/public/media/;
        expires max;
    }

    location / {
        proxy_redirect     off;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;


        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8004;
            break;
       }
   }


    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/localmingle.keycorp.in/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/localmingle.keycorp.in/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
server {
    if ($host = localmingle.keycorp.in) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    server_name localmingle.keycorp.in;
    listen 80;
    return 404; # managed by Certbot


}
