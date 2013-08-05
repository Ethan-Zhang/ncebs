ncebs
=====

Nginx Configure Edit and Boot System

#Usage
```shell
python ncebs/ncebs/bin/ncebs-api.py --nginx_conf_path=xxxx --nginx_bin_path=xxx --db_driver=db
```

#Service API
index domain
```url
GET /domains/{domain}/{name}
response json
{
  "domains":[
    {
      "ip":"192.168.0.1",
      "port":"8080",
      "name":"test"
    },
    ...
  ]
}
```
create domain
```url
POST /domains/{domain}/{name}
request json
{
  "ip":"192.168.0.1",
  "port":"8080"
}
```
edit domain
```url
PUT /domains/{domain}/{id}
request json
{
  "ip":
  "name":
  "port":
}
```
delete domain
```url
DELETE /domains/{domain}/{id}
```

#Thanks
Thanks for xyz_ to give many suggestions of the project. 
