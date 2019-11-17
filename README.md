ZabbixInfo
========================

A python script to search for specific values in **Zabbix** database.

We created this script because we needed to process the data that **Zabbix** obtained from the hosts in our network.

So far it queries the **Zabbix** database in order to search for a specific host, then it lets you select which item's data you wanna view.

It lets you export the data of the selected item into a **.csv** file (optional) and gives you the mean of the maximum, minimum and average values that **Zabbix** has stored on its' database. 

Since this is the very first version of the script you need to manually replace in your readingdb.py your database's username and password, the default **username**:**password** is **root**:**1234**. We're planning on doing this in a smarter way soon :blush:

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