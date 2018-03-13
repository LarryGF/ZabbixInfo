import click
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
#Prompts the user to select the databse's user and password
user=click.prompt("\nType your database's user",default='root')
password =click.prompt("Type your database's password",hide_input=True,default='1234')
dbaddr = click.prompt("Type your database's IP address",default='localhost')

#This is the string that needs to be passed to the create_engine function (if anyone finds a better way to do this, feel free to edit)
string='mysql://'+user+':'+password+'@'+dbaddr+'/zabbix' 

#engine = create_engine('mysql://root:1234@localhost/zabbix', echo=False)
engine = create_engine(string, echo=False) 

#I know this is kinda basic, but it's a way to check if the user and password are correct
noError = False
count = int(0)
while noError==False:
    try:
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Session = sessionmaker(bind=engine, expire_on_commit=False)
        session = Session()
        noError = True
    except Exception as e:
        count =count+1

        if count < 3:
            user=click.prompt("\nYou typed the wrong user or password, retype user",default='root')
            password =click.prompt("Retype password",hide_input=True,default='1234')
            dbaddr = click.prompt("Retype IP address",default='localhost')
            
        else:
            print("\nIt seems like you don't know your database very well,exiting for your own sake...\n")
            exit()            
    pass

# File = Base.classes.files
# a = session.query(File).filter(File.filename.like('%snake%')).all()
# print([(e.path_parent + e.filename) for e in a])
# ilike no es case sensitive
hosts = Base.classes['hosts']
items = Base.classes['items']
trends = Base.classes['trends']


def search_host(hostname: str):
    """
    El método recive un hostname y devuelve

    (hosts.id, hosts.name)

    donde hostname es un substring de hosts.name
    """
    return session.query(hosts.hostid, hosts.name).filter(hosts.name.ilike('%{}%'.format(hostname))).all()


def get_items(hostid: int):
    """
    El método recive un hostid y devuelve

    (items.hostid, items.itemid, items.name)

    donde items.hostid == hostid
    """
    return session.query(items.hostid, items.itemid, items.name).filter(items.hostid == hostid).all()


def get_trends(itemid: int):
    """
    El método recive un itemid y devuelve

    (trends.itemid, trends.value_min, trends.value_avg, trends.value_max, trends.clock)

    donde trends. itemid == hostid
    """
    return session.query(trends.itemid, trends.value_min, trends.value_avg, trends.value_max, trends.clock).filter(trends.itemid == itemid).all()


def percentil(scores):
    count = 0
    ans = []
    for i, score in enumerate(scores):
        i += 1
        ans.append(i / len(scores))

    return ans


def rank(scores, percentil_rank, value):

    for i, e in enumerate(percentil_rank):
        if e >= value:
            return scores[i]


def mean(numbers):
    mean = float(sum(numbers)) / max(len(numbers), 1)
    return mean

#Filter the trends where timestamp1 <= time <= timestamp2 & itemid==hostid
def filter_time(timestamp1,timestamp2,itemid: int):
    return session.query(trends.itemid, trends.value_min, trends.value_avg, trends.value_max, trends.clock).filter(and_(trends.itemid == itemid,trends.clock >= timestamp1,trends.clock <= timestamp2)).all()
