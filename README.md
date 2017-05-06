# wireless-clients-monitor
Periodally scan a network subnet to detect potentially unknown clients and notify admin

TODO
* change project name to: LAN clients monitoring
* write README file
  * dependencies: python modules, linux packages, host permissions
    * arp-scan
    * \# chmod u+s /usr/bin/arp-scan
    * \# python-pip -r requirements.txt
  * rationale
  * config.py
* [DONE] do not create a new token if one already exist in the database
* [DONE] create a Jinja file with buttons created dynamically with token values
* [DONE] get the most out of config.py file
* [DONE] create token file if does not exist (first run)
* [DONE] add unsnooze feature
