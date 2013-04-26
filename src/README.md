## Software Dependency
This package is built on `redis-py`, which is the python client of Redis server. If you are using Ubuntu, use the following command to install `redis-py`:
> $ sudo apt-get install python-redis

For other operating system, please check the [official site][1].


## Configuration
Go to the src/ directory where a file called `configure.py` exists. Edit the file with your preferred machines and port, and other preference. Note that you must provide at least one Master Node and one Slave Node.


## Run Master Node
The Master Node can be started easily on the master machine by the following command:
> $ python master.py

Note that, only one Master Node can claim itself as the Master Node, even though you may provide many different backups. The first one defined in the `MASTER_HOST` will be chosen as the default Master Node.


## Run Slave Node
The Slave Node can also be easily started on any slave machine by the following command:
> $ python slave.py

Note that, the Slave Node cannot be started automatically from Master Node, so you have to start all of the Slave Node one-by-one manually. The automatical start has been scheduled to future work.


## Run Jobs and Tasks
In the current version, the Master Node is bundled with the Job so that when you start the Master Node, it start to run your predefine Job which defines in `jobs.py`. Therefore, the Slave Node should be started first, because once you run Master Node, the job starts.

[1]: https://github.com/andymccurdy/redis-py
