# AirFlask

![AirFlask (2)](https://github.com/user-attachments/assets/73f561cb-74aa-428e-be29-08694574dc2e)

Simplest way to host flask web apps in production.
Using nginx and gunicorn.

## Installation
`pip install airflask`


## Usage
**Deploying**

`sudo airflask deploy <path>`

where path is full path to parent folder containing our app.py (BE sure to rename the main flask file as `app.py`)

for eg. `sudo airflask deploy /home/naitik/flaskecomapp/`



**Stop or Restart**

`sudo airflask restart <path>` 

`sudo airflask stop <path>`

Restart whenever you make any changes





