import logging
from plpipes.database.driver import Driver
from plpipes.database.driver.transaction import Transaction
import sqlalchemy as sa
import sqlalchemy.sql as sas
from contextlib import contextmanager
from plpipes.util.method_decorators import optional_abstract

from plpipes.database.sqlext import CreateTableAs, CreateViewAs, DropTable, DropView, Wrap, InsertIntoTableFromQuery

class SQLAlchemyDriver(Driver):

    _transaction_factory = Transaction

    @classmethod
    def _init_plugin(klass, key):
        super()._init_plugin(key)
        klass._create_table.td.register(sas.elements.ClauseElement, '_create_table_from_clause')

    def __init__(self, name, drv_cfg, url, **kwargs):
        super().__init__(name, drv_cfg)
        self._url = url

        logging.debug(f"calling sqlalchemy.create_engine(url={url}, kwargs={kwargs})")
        self._engine = sa.create_engine(url, **kwargs)

    @contextmanager
    def begin(self):
        with self._engine.connect() as conn:
            with conn.begin():
                yield self._transaction_factory(self, conn)

    def _execute(self, txn, sql, parameters=None):
        txn._conn.execute(Wrap(sql), parameters)

    def _execute_script(self, txn, sql):
        logging.debug(f"database execute_script code: {repr(sql)}")
        txn._conn.execute(Wrap(sql))

    def _read_table(self, txn, table_name, backend, kws):
        try:
            column_names = kws.pop("columns")
            columns = [sas.column(n) for n in column_names]
        except KeyError:
            columns = ["*"]
        query = sas.select(*columns).select_from(sas.table(table_name))
        return self._query(txn, query, None, backend, kws)

    def _drop_table(self, txn, table_name, only_if_exists):
        txn._conn.execute(DropTable(table_name, if_exists=only_if_exists))

    @optional_abstract
    def _list_tables_query(self):
        ...

    @optional_abstract
    def _list_views_query(self):
        ...

    def _list_tables(self, txn):
        df = txn.query(self._list_tables_query())
        return df.rename(columns={0: "name"})[["name"]]

    def _list_views(self, txn):
        df = txn.query(self._list_views_query())
        return df.rename(columns={0: "name"})[["name"]]

    def _table_exists_p(self, txn, table_name):
        sq = self._list_tables_query().subquery()
        q = sa.select(sas.literal(1)).where(sq.c.name == table_name)
        # print(f"query: {q}")
        df = txn._conn.execute(q)
        return df.scalar() is not None

    def _create_table_from_str(self, txn, table_name, sql, parameters, if_exists, kws):
        return self._create_table_from_clause(txn, table_name, Wrap(sql), parameters, if_exists, kws)

    def _create_table_from_clause(self, txn, table_name, clause, parameters, if_exists, kws):
        if if_exists == "append":
            if txn.table_exists_p(table_name):
                txn._conn.execute(InsertIntoTableFromQuery(table_name, clause),
                                  parameters)
                return
            # else fall through...

        if_not_exists = False
        if if_exists == "replace":
            self._drop_table(txn, table_name, True)
        elif if_exists == "ignore":
            if_not_exists = True
        txn._conn.execute(CreateTableAs(table_name, clause,
                                        if_not_exists=if_not_exists),
                          parameters)

    def _create_view(self, txn, view_name, sql, parameters, if_exists, kws):
        if_not_exists = False
        if if_exists == "replace":
            txn._conn.execute(DropView(view_name, if_exists=True))
        elif if_exists == "ignore":
            if_not_exists = True
        txn._conn.execute(CreateViewAs(view_name, Wrap(sql),
                                       if_not_exists=if_not_exists),
                          parameters)

    def _copy_table(self, txn, from_table_name, to_table_name, if_exists, kws):
        return self._create_table_from_str(txn, to_table_name,
                                           f"select * from {from_table_name}", None,
                                           if_exists, kws)

    def engine(self):
        return self._engine

    def url(self):
        return self._url

    def _read_table_chunked(self, txn, table_name, backend, kws):
        return self._query_chunked(txn, f"select * from {table_name}", None, backend, kws)

    def _pop_kw(self, kws, name, default=None):
        try:
            return kws.pop(name)
        except KeyError:
            return self._cfg.get(name, default)

