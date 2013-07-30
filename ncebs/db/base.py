from util.config import options, define
from util import importutils


define('--db_driver', name='db_driver', type='string')


class DBBase(object):
    """DB driver is injected in the init method."""

    def __init__(self, db_driver=None):
        if not db_driver:
            db_driver=options.db_driver
        self.db=importutils.import_module(db_driver)
        super(DBBase, self).__init__()
