export DBNAME=kamailio
export DBHOST=10.41.0.104
export DBENGINE=pgsql
export DBRWUSER=kamailio
export DBRWPW=kamailiopw
export DBNAME=kamailio
export DBROUSER=kamailioro
export DBROPW=superpass

chmod 600 /root/.pgpass

kamdbctl create

