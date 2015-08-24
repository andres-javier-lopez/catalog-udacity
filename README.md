# Item Catalog #

To load the project you need to have vagrant configured.

Enter into the vagrant directory, and then run `vagrant up` to configure the
server. Then run `vagrant ssh` to enter the server, and move to the
`/vagrant/catalog` directory.

To create initialize the database run the comand `python database.py`. This will
create a _catalog.sqlite_ file with some default categories and item. If you
want to reset the database, just delete the sqlite file and run the command
again.

To execute the application run `python application.py`. Then visit the address
_localhost:8000_ in your web browser.
