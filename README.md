ZabbixInfo
========================

A python script to search for specific values in **Zabbix** database.

We created this script because we needed to process the data that **Zabbix** obtained from the hosts on our network.

So far, it queries the **Zabbix** database to search for a specific host. Then, it lets you select which item's data you want to view.

It lets you export the data of the selected item into a **.csv** file (optional) and gives you the mean of the maximum, minimum and average values that **Zabbix** has stored on its database. 

You can search the host you're looking for by passing the option **--name**. If you don't, it will still prompt you for one.

It will ask you for the database's username, password and address (defaults to: **'root'**, **'1234'**, **'localhost'** respectively). Currently, you can't connect to a remote database. We're working on that.

You can now filter the results by date and time.

I hope this is useful to you! Further development is in process :)

Installation
-------------------

### This code depends on:

- Python3
- SQLAlchemy
- Click

You can install python dependencies using `pip install -r requirements.txt`

### To use it:

```bash
python zabbixinfo.py 
```
