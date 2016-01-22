# Tournament Database
=====================

## Requirements
* [Python 2.7.x or higher](https://www.python.org/downloads/)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

## Quick Start
* [Download files](https://github.com/AdnanJaffal/Tournament-Database/archive/master.zip)
* Use a command prompt and browse to the /vagrant folder.
* Run [vagrant up] and [vagrant ssh] to connect to the vagrant virtual machine.
* Run [cd /vagrant/tournament] to browse to the folder containing the python and sql code.
* Using psql, import the tournament.sql file to create the database, tables, and views:

  * >> psql
  * psql >> \i tournament.sql;
  * tournament >> \q;

* Run [python tournament_test.py] to test the Swiss Tournament database, or use your own python file to call tournament.py
  and use the database.
