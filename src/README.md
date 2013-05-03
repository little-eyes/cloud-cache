## Software Dependency
This package is built on `redis-py`, which is the python client of Redis server. If you are using Ubuntu, use the following command to install `redis-py`:
> $ sudo apt-get install python-redis

For other operating system, please check the [official site][1].

Also the the Data Node needs `redis-server` to be installed and run as a service in the system. If you are using Ubuntu, use the following command to install:
> $ sudo apt-get install redis-server

For other operating system, please check the [official site][2].


## Configuration
Go to the src/ directory where a file called `configure.py` exists. Edit the file with your preferred machines and port, and other preference. Note that you must provide at least one Master Node, one Slave Node, one Data Node and one Sinker Node.


## Run Master Node
The Master Node can be started easily on the master machine by the following command:
> $ python master.py

Note that, only one Master Node can claim itself as the Master Node, even though you may provide many different backups. The first one defined in the `MASTER_HOST` will be chosen as the default Master Node.


## Run Slave Node
The Slave Node can also be easily started on any slave machine by the following command:
> $ python slave.py

Note that, the Slave Node cannot be started automatically from Master Node, so you have to start all of the Slave Node one-by-one manually. The automatical start has been scheduled to future work.


## Run Sinker Node
The Sinker Node is another node needs to manually start, using the following command:
> $ python sinker.py

## Run Data Node
The Data Node is automatically started after you install the redis=server.

## Run Jobs and Tasks
After the Master Node, Slave Node, Data Node and Sinker Node has been successfully started, you can submit a job by running a small client program. We provide a sample client program called `sample-client.py` in the directory, you can run it with the following command:
> $ python sample-client.py

After the job is finished by CloudCache framework, you can go ahead and retrieve the results back from Sinker Node.

[1]: https://github.com/andymccurdy/redis-py
[2]: http://redis.io
