#!/usr/bin/env bash
# Sets up a web server for the deployment of web_static

if ! [ -x "$(command -v nginx)" ]; then
	apt update -y
	apt install nginx -y
	service nginx restart
fi

data_dir="/data"
web_static="$data_dir/web_static"
releases="$web_static/releases"
shared="$web_static/shared"
curr="$web_static/current"
test_dir="$releases/test"

mkdir -p "$test_dir"
mkdir -p "$shared"
rm -rf $curr
ln -s "$test_dir" "$curr"
chown -R ubuntu:ubuntu $data_dir

test_page="
<!DOCTYPE html>
<html>
<head>
<title>Welcome to alx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Hello World!</h1>
<p>If you're seeing this something's wrong. 
<p><em>We are using nginx.</em></p>
</body>
</html>"
echo "$test_page" > "$test_dir/index.html"

location_block="location /hbnb_static {\n\t\talias $curr/;\n\t}\n"

conf_file="/etc/nginx/sites-available/default"
search="server_name _"

if ! grep -Fq "location /hbnb_static {" "$conf_file";
then
    sed -i "/$search/a \\\t$location_block" $conf_file
fi

nginx -s reload
