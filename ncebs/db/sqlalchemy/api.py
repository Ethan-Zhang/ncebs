import time

from db.sqlalchemy import models
from sqlalchemy import sql
from sqlalchemy import create_engine

engine = create_engine('mysql://root@192.168.0.176:19800/ncebs_domains', echo=True)

models.metadata.create_all(engine)

def dns_add(domain, name, ip, port):
    _now = time.time()
    conn = engine.connect()
    ins = models.hualuyunhai.insert().values(name=name, ip=ip, port=port,
            deleted=0, create_time=str(_now), update_time=str(_now))
    conn.execute(ins)

def dns_getList(domain):
    conn = engine.connect()
    sel = sql.select([models.hualuyunhai])
    result = conn.execute(sel).fetchall()
    return  result

def dns_getDetail(domain, id):
    conn = engine.connect()
    sql_sel = sql.select([models.hualuyunhai]).where(models.hualuyunhai.c.id
                                                    == id)
    result = conn.execute(sql_sel).fetchone()
    return result

def dns_edit(domain, id, name, ip, port):
    _now = time.time()
    conn = engine.connect()
    sql_up = models.hualuyunhai.update().where(models.hualuyunhai.c.id ==id)\
                                    .values(name=name, ip=ip, port=port,
                                            update_time=str(_now))
    result = conn.execute(sql_up)
    return result

def dns_del(domain, id):
    conn = engine.connect()
    sql_del = models.hualuyunhai.delete().where(models.hualuyunhai.c.id == id) 
    result = conn.execute(sql_del)
