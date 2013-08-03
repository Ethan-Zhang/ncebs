from db.sqlalchemy import models
from sqlalchemy import sql
from sqlalchemy import create_engine

engine = create_engine('mysql://root@192.168.0.176:19800/ncebs_domains', echo=True)

models.metadata.create_all(engine)

def dns_add(domain, name, ip, port):
    conn = engine.connect()
    ins = models.hualuyunhai.insert().values(name=name, ip=ip, port=port)
    conn.execute(ins)

def dns_getList(domain):
    conn = engine.connect()
    sel = sql.select([models.hualuyunhai])
    result = conn.execute(sel).fetchall()
    return  result
