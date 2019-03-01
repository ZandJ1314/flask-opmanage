if [ ! -d logs ];then
	mkdir logs
	chown -R uwsgi:uwsgi logs
else
	chown -R uwsgi:uwsgi logs
fi
if [ ! -d cache ];then
	mkdir cache
	chown -R uwsgi:uwsgi cache
else
	chown -R uwsgi:uwsgi cache
fi
/usr/bin/uwsgi --uid uwsgi --gid uwsgi -x /etc/uwsgi.xml -d /var/log/uwsgi.log
