# Portuss

# Web project to rent a car quickly.
## Portuss project architecture:
The project consists of 3 apps: pproject, payments and posts.
1. pproject is the base app, here is implemented all basic functionality: user registration, editing profile, searching and getting the car for a rent, putting the car for a rent etc.
2. payments app is created to process payments. When user is going to rent a car, he/she follows the url ['complete_booking'](https://github.com/vilnitskiy/Portuss/blob/payments_app/pproject/urls.py#L33-L36), where after loading all docs that is needed (driver's license, passport and own photo with passport) he/she redirects on payments form. On the payments form user should be able to pay with Visa/Mastercard, PayPal or WebMoney. Payments processes with [Braintree](https://www.braintreepayments.com/). In this moment Braintree is on sandbox version and payments app could only get payments for site owners.
3. posts app is for livechats. It is based on django channels. In that moment you can create the new chat room from admin page and just give the link on newly created chat for any user you want. You can see all the chats if you follow the <potruss_domain>/chose-chat/.

Each app has its own urls and migrations. The portuss/urls.py file is the main file with urls. It inherits from pproject, payments and posts urls. Project settings are locaded in portuss/settings.py. All templates are locaded in templates/ folder.

# How to run server:
$ wget http://download.redis.io/redis-stable.tar.gz

$ tar xvzf redis-stable.tar.gz

$ cd redis-stable

$ make

$ sudo make install

$ redis-server

$ git clone git@github.com:vilnitskiy/Portuss.git

$ cd Portuss

$ sudo -u postgres psql

	CREATE DATABASE portuss_table;

$ virtualenv .venv --no-site-packages

$ source .venv/bin/activate

$ pip install -r requirements.txt

$ make migrate

$ make run