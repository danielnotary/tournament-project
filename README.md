Tournament Database v. 1.0 07/11/2016

-------------
GENERAL USAGE
-------------

-To begin, open your Vagrant virtual machine and navigate to the tournament
folder. Navigate to your Vagrant directory and type 'vagrant up' to bring up
the machine. When that is finished, type 'vagrant ssh' to open the command
shell.

-You can access the psql console by typing 'psql' in the vagrant command
line. Connect to your database in this console by typing:
<pre><code>CREATE DATABASE tournament;
\c tournament
</pre></code>

-To create the necessary tables, you can either paste the commands from the
tournament.sql file in the psql console, or type:
<pre><code>\i tournament.sql
</pre></code>
This will run any SQL code found in the file, and if the tables have already
been created, the command line will tell you. These instructions are also
contained in the tournament.sql file.

-If you need to drop the tables (maybe to make a correction), use this 
command:
<pre><code>DROP TABLE table name;
</pre></code>
You will then need to run tournament.sql again to recreate the tables.

-Run the tournament_test.py file to test the current tournament functions.

-Files: tournament.py has functions to handle tournament results (win,
loss, draw) and pair players based on standings, tournament.sql creates
the data tables (currently 'players' and 'matches'), and tournament_test.py
contains several test functions to ensure the code written in tournament.py
runs correctly.

------------
CAPABILITIES
------------

-The minimum requirements for the code were to register players, report
matches, display standings ordered by number of wins, and pair players
based on win records (players with 1 win are paired, players with 1 loss
are paired, etc.)

-Additional functions were added to tournament.py to account for byes and
draws. New test functions were created to handle these cases, respectively
named testByes() and testDraws(). 

------------
CONTACT INFO
------------

Email: danielnotary7@gmail.com
