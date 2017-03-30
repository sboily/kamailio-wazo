This tutorial is aimed to help people to use kamailio in front of wazo (version min. 17.02).
You can read the [getting
started](http://documentation.wazo.community/en/stable/getting_started/getting_started.html)
for more help to install wazo.

This tutorial is inspired by http://kb.asipto.com/asterisk:realtime:kamailio-4.0.x-asterisk-11.3.0-astdb.

I'm using docker to install kamailio because it's simple to use and funny to
work with it :-)

Kamailio installation
---------------------

The kamailio version is : 4.4.5

    docker pull quintana/kamailio

Clone the repository to get the configuration for the kamailio.

    git clone https://github.com/sboily/kamailio-wazo

Connect to your postgres with xivo database.

    su - postgres
    psql
    postgres> ALTER USER postgres WITH ENCRYPTED PASSWORD '<postgres_password>';
    postgres> exit;

Add your subnet or ip to the file /etc/postgresql/9.4/main/pg_hba.conf.

Edit the pgpass file add the following line. In most cases, the IP address will
be the same as your wazo. The default port for postgres is 5432.

    <postgres_ip>:<postgres_port>:*:postgres:<postgres_password>

Launch kamailio

    cd <kamailio_xivo_repo>/kamailio/
    docker run --rm --name kamailio -v $(pwd):/etc/kamailio -p 5060:5060/udp -it quintana/kamailio bash

Before running kamailio for the first time you need to initialize the database.
Edit the init.sh script and put in the right IP address. You can get your ip
inside a docker container by running:

    ip a s

Or, if you are outside of the container:

    docker inspect --format '{{ .NetworkSettings.IPAddress }}' kamailio

Then launch the init.sh inside of the container

    cd /etc/kamailio/
    ./init.sh 

Then further launches can be run with:

    kamailio -ddDDe

Wazo configuration
------------------

We need to removed the SIP challenge, so to do this asterisk check if you have a
secret to your user. On Wazo the daemon xivo-confgend is in charge to generate
the asterisk configuration. 

You need to use my specific driver who removed the secret generation from
xivo-confgend.

Copy xivo/confgend directory to your wazo and type:

    python setup.py install
    cp conf/kamailio.yml /etc/xivo-confgend/conf.d

Then restart the daemon and reload the SIP config in asterisk

    systemctl restart xivo-confgend
    asterisk -rx "sip reload"

After that go to the web interface and secure your access. Go to general
settings/sip protocol in the network tab. Fill in the denied address with
0.0.0.0/0.0.0.0 and the allowed address with <docker_ip>/255.255.255.255 or
your docker subnet (172.17.0.0/255.255.0.0) if you do a lot of tests. Do not
forget to enable NAT in the default tab.

Provisioning your phone
-----------------------

If you want to use Wazo provd, don't forget to add a new template line in the
Configuration/Provisioning/Template Line with the IP of your kamailio
installation.

Uninstall
---------

To uninstall the driver

    apt-get install python-pip
    pip uninstall wazo_confgend_driver_kamailio
    rm /etc/xivo-confgend/conf.d/kamailio.yml
