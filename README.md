[Unit]
Description=Speak MagicMirror News
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/speak_news.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
