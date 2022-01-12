# simple chat with python flask & socket
![alt text](https://github.com/Cypher999/flask_chat/blob/main/screenshoot.png?raw=true)<br>
This is python flask program to demonstrate how socket work for web based chat app

##### Requirements?
```
python v 3.4 or above (recommend to use v 3.9)
mysql server / mariadb installed on operating system
flask (available at req.txt)
flask_socketio (available at req.txt)
mysql.connector (available at req.txt)
```


##### How to Install?
```
run "git clone https://github.com/Cypher999/flask_chat" on terminal
navigate to flask_chat location (usualy on the same location as the terminal's working directory when you run previous command)
run "pip install -r req.txt" on the terminal
```

##### How to Use?
```
edit the "config.py" file to set the configuration
set the ip address with the ip you desire by editing the "IP" value on line 1(default is "127.0.0.1")
set the port number with the port you desire by editing the "PORT" value on line 2(default is 5000)
set the database host by editing the "HOST" value on line 3(default is "localhost")
set the database user by editing the "USER" value on line 4(default ip is "root")
set the database password by editing the "PASSWORD" value on line 5(default ip is "")
finnaly , open "app.py" or run ""python app.py" " on the terminal to run the app
```
compatible with linux,windows and android (using termux / python compiler application), if the requirements is 
satisfied
