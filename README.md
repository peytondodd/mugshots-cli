# Mugshots CLI

> Python 3 CLI for fetching latest mugshots from mugshots.starnewsonline.com

### Uses **BeautifulSoup4** and **Requests** libraries under the hood.

## Important Information
**This site records those taken into custody by local law enforcement. Booking information has been collected from the Bladen, Brunswick, New Hanover and Pender County jail systems.**


**This program makes no assumptions or representations about guilt or innocence. People charged with crimes are presumed innocent unless proven guilty. Information on the StarNewsOnline site and this program should not be used to determine any person’s actual criminal record.**

## Features
* Will automatically add demographics to the local `records.csv` file.

* Will automatically fetch the mugshot image and store in the `mugs/` folder with respected ID as file name.

* CLI output will show ID - Name with list of charges below and a total bond amount.

## Installation
```bash
$ git clone git@github.com:zacharytyhacz/mugshots-cli.git

$ cd mugshots-cli

$ pip install requirements.txt

$ mv .env_example .env

$ python3 main.py
```
<img src="https://i.ibb.co/RHkzRBJ/shot1.png" alt="shot1" border="0">
<img src="https://i.ibb.co/c8p2WsT/shot2.png" alt="shot2" border="0">
