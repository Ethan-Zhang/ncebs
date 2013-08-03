import db.sqlalchemy.api

IMPL = db.sqlalchemy.api

def dns_add(domain, name, ip, port):
    return IMPL.dns_add(domain, name, ip, port)

def dns_getList(domain):
    return IMPL.dns_getList(domain)

def dns_getDetail(domain, id):
    return IMPL.dns_getDetail(domain, id)

def dns_del(domain, id):
    return IMPL.dns_del(domain, id)
