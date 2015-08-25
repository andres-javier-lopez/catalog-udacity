# Item Catalog

## Section 1: Intro
This system is a basic catalog for any kind of items. It can be arranged on
categories, and you can add a name, description and an image to the item. It
providesa json and atom endpoint to consult the information, and has a recently
added items page.

## Section 2: Requirements
The project runs with the following libraries:
* Flask == 0.10.1
* SQLAlchemy == 0.8.4
* Requests == 2.2.1
* oauth2client == 1.4.11
* werkzeug == 0.9.4

This list is included in the _requirements.txt_ file. For an easy installation
use `pip install -r requirements.txt`.

## Section 3: Installation
To install and run the project run the following commands:

 1. `git clone https://github.com/odinjv/catalog-udacity.git`
 2. `cd catalog-udacity/vagrant`
 3. `vagrant up`
 4. `vagrant ssh`
 5. `cd /vagrant/catalog`
 6. `pip install -r requirements.txt`

 You need to have vagrant already installed and configured.


## Section 4: Set Up
To create initialize the database run the comand `python database.py`. This will
create a _catalog.sqlite_ file with some default categories and item. If you
want to reset the database, just delete the sqlite file and run the command
again.

## Section 5: How to run
To execute the application run `python application.py`. Then visit the address
_localhost:8000_ in your web browser.

## Section 6: Usage
You have to be logged in with your google account to create new categories or
items. You can edit the names of all categories, but can only delete them if
they are empty.

You can only edit and delete the items that you have created. The items provided
by default on the setup have no owner and can be deleted and edited by everyone.
To create your own catalog, you can delete the existing items and create your
own categories and items.
