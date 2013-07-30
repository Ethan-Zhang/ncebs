import db.sqlalchemy.api

IMPL = db.sqlalchemy.api

def dns_add(domain, name, ip, port):
    IMPL.dns_add(domain, name, ip, port)

def dns_get(domain):
    IMPL.dns_get(domain)
