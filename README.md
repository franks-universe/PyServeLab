# PyServeLab
PyServeLab is a simple web server GUI written in Python which allows you to quickly spin up a local development server to test out HTML/CSS code.


## Requirements
PyServeLab requires PyQt6 and Flask to be installed, you can install these with:
`pip install PyQt6 flask`

Due to being a GUI app, PyServLab requires a desktop environment, it will not run on a cli-only system.

## Usage

PyServeLab is GUI based, please run `PyServeLab.py` and set the following options:

**Select Directory**

Select the root directory where you have your HTML/CSS files saved.

**Port**

Select the port you wish to use, you may need to open this port in your local firewall.

**Default Document**

This is the default document to serve for the root folder, the default is *index.html*

**Start Server**

This button will start the server, a folder must be selected to start the server.

**Stop Server**

This button will stop the running server.

Open your browser and go to http://localhost:5000

If you are using a different port number make sure to update the address in your browser, and you may need to open the port in your firewall, for example:

`sudo ufw allow 5000`
