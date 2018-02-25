# ZabbixInfo
A python script to search for specific values in Zabbix database.

We created this script because we needed to process the data that Zabbix obtained from the hosts in our Network.

So far it queries the Zabbix database in order to search for a specific host, then it lets you select which item's data you wanna view.

It lets you export the data of the selected item into a .csv file (optional) and gives you the mean of the maximum, minimum and average values that Zabbix has stored on its' database. 

#Installation

It depends on:

-Python3
-SQLAlchemy
-Click

I hope this results useful to some of you, further development in process :)

#To use it:

python zabbixinfo.py "name of the host for which you wanna search the values"
