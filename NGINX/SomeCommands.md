## Set Password Authentication
``` 
htpasswd -c ./admin.htpasswd admin
```


### htpasswd: To Install/Find htpasswd utility
```
yum install httpd-tools 
yum provides \*bin/htpasswd
```

### SELinux: Allow reverse-proxy connect to Kibana
```
semanage port -a -t http_port_t -p tcp 5601 # Kibana port
```
