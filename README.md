ZabbixInfo
========================

A python script to search for specific values in **Zabbix** database.

We created this script because we needed to process the data that **Zabbix** obtained from the hosts in our network.

So far it queries the **Zabbix** database in order to search for a specific host, then it lets you select which item's data you wanna view.

It lets you export the data of the selected item into a **.csv** file (optional) and gives you the mean of the maximum, minimum and average values that **Zabbix** has stored on its' database. 

You can search the host you're looking for by passing the option **--name**, but if you don't it will still prompt you for one.

It will ask you for the database's user, password and address (defaults to: **'root'**, **'1234'**, **'localhost'** respectively). So far you can't connect to a remote database, but we'll work on that.

Installation
-------------------

### It depends on:

- Python3
- SQLAlchemy
- Click

I hope this results useful to some of you, further development in process :)

You can install python dependencies using `pip install -r requirements.txt`

### To use it:

```bash
python zabbixinfo.py 
```
