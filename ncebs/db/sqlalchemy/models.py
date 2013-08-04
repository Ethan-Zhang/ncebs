from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


metadata = MetaData()

hualuyunhai = Table('hualuyunhai', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(255), nullable=False),
                Column('ip', String(23), nullable=False),
                Column('port', Integer, nullable=False),
                Column('deleted', Integer, nullable=False),
                Column('create_time', String(255), nullable=False),
                Column('update_time', String(255), nullable=False),
            )

