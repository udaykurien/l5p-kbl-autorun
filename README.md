Auto turn on and off keyboard backlight on keypress / idle time. <br>
Unit file example: <br>

[Unit] <br>
Description=Keyboard backlight auto on/off <br>
After=multi-user.target <br>

<br>

[Service] <br>
Type=simple <br>
User=<whoami> <br>
ExecStart=<path-to-python-interpreter> <path-to-script> <br>
Restart=on-failure <br>

<br>

[Install] <br>
WantedBy=multi-user.target <br>
