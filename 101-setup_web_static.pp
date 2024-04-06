# Sets up a web server for the deployment of web_static

Exec { path => '/bin/:/sbin/:/usr/bin/:/usr/sbin/' }

$data_dirs = ['/data', '/data/web_static', '/data/web_static/shared',
'/data/web_static/releases', '/data/web_static/releases/test']

$curr_link = '/data/web_static/current'
$test_file =  "${data_dirs[4]}/index.html"
$conf_file = '/etc/nginx/sites-available/default'

package { 'nginx':
    ensure => installed
}

file { $data_dirs:
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu'
}

file { $curr_link:
    ensure => 'link',
    target => $data_dirs[4],
    owner  => 'ubuntu',
    group  => 'ubuntu'
}

$index_page = @(HOMEPAGE)
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
</html>
| HOMEPAGE

file { $test_file:
    ensure  => present,
    content => $index_page,
    owner  => 'ubuntu',
    group  => 'ubuntu'
}

$location_block="location /hbnb_static {\n\t\talias ${curr_link}/;\n\t}\n"

exec { 'set_route' :
    command => "sed -i \"/server_name _/a ${location_block}\" ${conf_file}",
    #onlyif  => "grep -Fq \"location /hbnb_static {\" ${conf_file}"
}

service { 'nginx' :
    restart => 'reload'
}
