# NAVIO

Your GPS, for indoors.

## Documentation (Usage)

Complete navio project is divided into three different modules.
- Admin website
- Android app
- Flask(python) backend

> First shopkeepers will signup using our admin website, there they have to upload their shop floor plan and draw the navigation directions inside the shop.

> Shopkeepers have to add qr slots and add corresponding items inside the qr slots.

> Now once everything in ready in admin side, indoor floor plan is published inside navio store. 

> On the customer side, users have to select the corresponding shop or complex inside navio app and follow the further instruction.

> Customers have to select the items that they want to shop, and rest work is done by navio.

> NAVIO will suggest the shortest path that they have to follow and show their current location inside the store.

## Installation

- Admin website ([Github link](https://github.com/Abhi1code/navio_final)) 
([hosted link](https://matrixfrats.com/navio/)) 

1) Download the above repo.
2) Make sure xampp server is installed inside your system.
3) Open phpmyadmin and create one database with name `ips1`.
4) All configuration setting to mysql database can be found inside the file `navio_website/src/db/db_connect.php`.
5) Import this ([SQL file](https://matrixfrats.com/download_api/download/upload/580617045785.sql
)) inside `ips1` database.
6) Now run `navio_website/src/bin/server.php` file in CMD using this command.
```
php server.php
```
7) Now open `navio_website/client/demo_1/index.html` file in any browser.
8) Here shopkeepers have to upload their floor plan and mark navigation directions(Sample floor plan is already uploaded).
9) For simplicity leave the admin panel as it is.

- Flask(python) backend ([Github link](https://github.com/Abhi1code/navio_flask))

1) Download the above repo.
2) Make sure python is installed inside your system.
3) Open `app.py` file inside `pycharm ide` and install suggested dependencies.
4) Run `app.py` file using the below command in the `pycharm` terminal.
```
python app.py
```

- Android app ([Github link](https://github.com/Abhi1code/navio_android))

1) Open the above repo in `android studio`.
2) Make sure above flask app is running in your system.
3) Open `cmd` and type `ipconfig`.
4) Copy the ipv4 address inside Local area connection (For me it was `192.168.137.1`).
5) Open `navio/ui/workers` directory in android studio.
6) Inside the `workers` folder, you can see four files.
7) Open each file and search for `String url = http://192.168.137.1:5000/`.
8) Replace `192.168.137.1` from your ipv4 address, which is obtained from cmd.
9) Everything is now ready, you just have to build and install the application inside your android phone.
10) Make sure your phone is connected to your system hotspot, otherwise the app will not work.
11) Select `current location` in the first page inside android app.
12) Follow the instructions until a `+` button in the bottom right portion of screen is visible.
13) Click the `+` button, there you can see a list of items present inside the complex.
14) Select multiple items and press Okay.
15) Now you can see direction and path to navigate.
