This tutorial will guide you on how to install and use kamailio in front of a
XiVO server.  Please have a XiVO installed and ready before starting. You can
read the [getting
started](http://documentation.xivo.io/en/stable/getting_started/getting_started.html)
document for more help. This tutorial is inspired by
http://kb.asipto.com/asterisk:realtime:kamailio-4.0.x-asterisk-11.3.0-astdb

I will be using docker to install kamailio because it's simple to use and fun to
work with :) (please do not install docker on a XiVO because wheezy does not
support a kernel version that is recent enough)

Kamailio installation
---------------------

As of this writing the latest version of kamalio is 4.2.4. Start by pulling
the latest version from the docker registry

    docker pull quintana/kamailio

Create a directory and download a few config files

    mkdir -p ~/kamailio/conf
    cd ~/kamailio/conf
    wget https://raw.githubusercontent.com/sboily/config/master/kamailio/kamailio.cfg
    wget https://raw.githubusercontent.com/sboily/config/master/kamailio/pgpass
    wget https://raw.githubusercontent.com/sboily/config/master/kamailio/init.sh
    chmod +x init.sh

Change the postgres password on your XiVO

    su - postgres
    psql
    postgres> ALTER USER postgres WITH ENCRYPTED PASSWORD '<postgres_password>';
    postgres> exit;

Edit the pgpass file add the following line. In most cases, the IP address will
be the same as your xivo. The default port for postgres is 5432.

    <postgres_ip>:<postgres_port>:*:postgres:<postgres_password>

Chmod the pgpass file to 600

    chmod 600 pgpass

Launch a new container with a terminal for further steps

    cd ~/kamailio/conf
    docker run --name kamailio -v $(pwd)/pgpass:/root/.pgpass -v $(pwd):/etc/kamailio -p 5060:5060/udp -it quintana/kamailio bash

Before running kamailio for the first time you need to initialize the database.
Edit the init.sh script and put in the right IP address. You can get your ip
inside a docker container by running:

    ip a s

Or, if you are outside of the container:

    docker inspect kamailio | grep IPAddress | awk -F\" '{print $4}'

Then launch the init.sh inside of the container

    cd /etc/kamailio/
    ./init.sh 

Then further launches can be run with:

    kamailio -ddDDe

XiVO configuration
------------------

When using kamailio we need to disable SIP authentication challenges. In
asterisk, this is accomplished by omitting the 'secret' of a user. On XiVO,
xivo-confgend is in charge of generating secrets, so we will need to hack it
a bit and add 'secret' to the list of values to ignore.

As of this writing, the ignore list can be found in
```/usr/share/pyshared/xivo_confgen/generators/sip.py``` around line 96 in the
method _gen_user(). You need to add 'secret' to the list as follows:

        sip_unused_values = (
            'id', 'name', 'protocol',
            'category', 'commented', 'initialized',
            'disallow', 'regseconds', 'lastms',
            'name', 'fullcontact', 'ipaddr', 'number', 'secret'
        )

Then restart the daemon and reload the SIP config in asterisk

    service xivo-confgend restart
    asterisk -r
    CLI> sip reload

After that go to the web interface and secure your access. Go to general
settings/sip protocol in the network tab. Fill in the denied address with
0.0.0.0/0.0.0.0 and the allowed address with <docker_ip>/255.255.255.255 or
your docker subnet (172.17.0.0/255.255.0.0) if you do a lot of tests. Do not
forget to enable NAT in the default tab.

Provisioning your phone
-----------------------

If you want to use XiVO provd, don't forget to add a new template line in the
Configuration/Provisioning/Template Line with the IP of your kamailio
installation.
