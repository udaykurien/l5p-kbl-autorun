Auto turn on and off keyboard backlight on keypress / idle time.
Unit file example: <br>
[Unit] <br>
Description=Keyboard backlight auto on/off
After=multi-user.target

[Service]
Type=simple
User=<whoami>
ExecStart=<path-to-python-interpreter> <path-to-script>
Restart=on-failure

[Install]
WantedBy=multi-user.target
