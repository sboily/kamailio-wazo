Hello !

This tutorial is to help people to use kamailio in front of to xivo. I'm
considering your XiVO is already installed or you following the getting started
in the xivo documentation. This tutorial is inspired by
http://kb.asipto.com/asterisk:realtime:kamailio-4.0.x-asterisk-11.3.0-astdb.

I'm using docker to install kamailio because it's simple to use and funny to
work with :) (please do not install docker on a xivo because wheezy don't
support the good kernel.

Kamailio installation
---------------------

The kamailio version is the latest : 4.2.4

    docker pull quintana/kamailio

Create a directory for the kamailio config

    mkdir -p ~kamailio/conf
    wget https://raw.githubusercontent.com/sboily/config/master/kamailio/kamailio.cfg
    wget https://raw.githubusercontent.com/sboily/config/master/kamailio/pgpass
    wget https://raw.githubusercontent.com/sboily/config/master/kamailio/init.sh
    cd ~kamailio/conf
    chmod +x init.sh

Go to your xivo postgres

    su - postgres
    psql
    postgres> ALTER USER postgres WITH ENCRYPTED PASSWORD '<user_postgres_password>';
    postgres> exit;

Edit the pgpass file and fill it with your good information.

    <ip_postgres_xivo>:<port_postgres_xivo>:*:postgres:<user_postgres_password>

Chmod the pgpass file to 600

    chmod 600 pgpass

Launch kamailio

    cd ~kamailio/conf
    docker run --name kamailio -v $(pwd):/etc/kamailio -p 5060:5060/udp -it quintana/kamailio bash

The first time you need to init you kamailio database, edit the init.sh before
launch it.

    cd /etc/kamailio/
    ./init.sh

Get your ip

    ip a s

Or if you're not in the container

    docker inspect kamailio | grep IPAddress | awk -F\" '{print $4}'

XiVO configuration
------------------

We need to removed the SIP challenge, so to do this asterisk check if you have a
secret to your user. On XiVO the daemon xivo-confgend is in charge to generate
the asterisk configuration. We need to hack the file
/usr/share/pyshared/xivo_confgen/generators/sip.py and add to the tuple the
secret keyword to be ignored.

On XiVO 15.06, this is the line 96 in method _gen_user(), you need to have this.

        sip_unused_values = (
            'id', 'name', 'protocol',
            'category', 'commented', 'initialized',
            'disallow', 'regseconds', 'lastms',
            'name', 'fullcontact', 'ipaddr', 'number', 'secret'
        )

Restart your daemon

    service xivo-confgend restart
    asterisk -r
    CLI> sip reload

Go to you webi and securise the access. Go to the general settings/sip protocol
and network tab.

Fill the denied address with 0.0.0.0/0.0.0.0 and the allowed address with your
docker <ip>/255.255.255.255 or your docker subnet (172.17.0.0/255.255.0.0) if you
do lot of tests. Do not forget to enabled NAT on the default tab.

Provisioning your phone
-----------------------

If you want to use the xivo provd, please don't forget to add a new template
line in the Configuration/Provisioning/Template Line with the IP of your
kamailio installation !
