from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///test.db', echo=False)
engine = create_engine('mysql://root:1234@localhost/zabbix', echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

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

    (trends.itemid, trends.value_min, trends.value_avg, trends.value_max)

    donde trends. itemid == hostid
    """
    return session.query(trends.itemid, trends.value_min, trends.value_avg, trends.value_max).filter(trends.itemid == itemid).all()


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
    ans = []
    mean = float(sum(numbers)) / max(len(numbers), 1)
    return mean
