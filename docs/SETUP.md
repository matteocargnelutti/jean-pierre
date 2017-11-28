![logo](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/ban.png)
# Docs : Setup guide
-- [**Back to README**](http://github.com/matteocargnelutti/jeanpierre)

# How does Jean-Pierre work ?
**It uses 2 parrallel processes to work :**
* **A scanner**, that allows users to add items on their grocery list by scanning them.
* **A web server**, that allows users to connect to the web interface.

The install script will configure and start theses two processes, using **supervisor** to manage them.

# Install
To achieve the following steps, open a terminal on your **Raspberry Pi**. It must run Raspbian *(preferably "lite")* and have a working internet connexion.

## Clone the repository
```shell
git clone https://github.com/matteocargnelutti/jean-pierre.git
```

## What does the install process do ?
**The install script ...**
* Makes shell files executable
* Installs system dependencies
* Sets a Python virtual environment
* Installs Python dependencies
* Launches the configuration assistant
* Creates 2 **supervisor** tasks to make Jean-Pierre's scanner and web server run automatically.

## Launch the install.sh script
```shell
cd jean-pierre
chmod a+x install.sh
./install.sh
```

These 3 commands will "go" to the directory where Jean-Pierre has been cloned, allow install.sh to be executed and execute it.

## Configuration assistant
The install process will take a while. After a moment, a **configuration assistant** will appear, asking you for the following info.

**The questions are pretty self-explanatory, but take heed of the following :**
* `Camera resolution` : by default, the camera resolution is set to 500x500, which is a good compromise between performances and range. You can set it to whatever you want, but please note that a higher resolution will have an impact on Jean-Pierre's performances.
* `Password` : this password is needed to connect to the web interface.
* `Language` : only **en** and **fr** are available for now.

**Note that calling this configuration assistant will not erase your database :** you can hance run it whenever you want to change Jean-Pierre's settings.

This **configuration assistant** can be called anytime with this command :

```shell
./jeanpierre.py --do config
```

## Reboot !
**Once the install script has finished working, you may have to reboot your Raspberry Pi in order to make everything boot.**

Please note that, on startup, it can take up to 2 minutes to have both the scanner and web server working.

If you've plugged a buzzer on Jean-Pierre, the scanner will make it ring twice to indicate that it works.

If anything went wrong, please look at the logs, open **install.sh** to see what went wrong by doing things manually **(copy / paste each command line)**.

# Uninstall
```shell
./uninstall.sh
```

This command will stop Jean-Pierre's processes so you can then safely remove its directory.

You might want to make a backup of your database before uninstalling Jean-Pierre : to do so, you can make a copy of **database.db**.

# Dependencies
A non-exhaustive of dependencies used in this project.
**These dependencies are managed by install.sh.**

## sudo apt-get install ...
python3-dev, python3-pip, python3-picamera, virtualenv, libzbar0, supervisor, libjpeg8-dev

## pip install
picamera, pyzbar, pytest, requests, RPi.GPIO, flask, gunicorn

-- [**Next : User guide**](https://github.com/matteocargnelutti/jean-pierre/blob/master/docs/USER.md)