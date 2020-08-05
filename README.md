# CryptoNotifier
Creates a desktop crypto notifier. You will need install pync and requests.
Run ```pip install pync``` and ```pip install requests```.

To run the project: ```python notification.py```

To have a scheduled notifier you will need to set up a cronjob. On a mac you can edit crontab via the terminal with the command ```crontab -e```.
In the crontab add ```0 */1 * * * cd DIRECTORY/OF/NOTIFIER && /DIRECTORY/OF/PYTHON2/OR/PYTHON3 notification.py```

For more details on cronjobs wiki have good example: ```https://en.wikipedia.org/wiki/Cron```
