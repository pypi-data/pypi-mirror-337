import logging
import geopandas
import pandas

from plpipes.database.backend.pandas import PandasBackend
from plpipes.util.database import split_table_name

DEFAULT_CHUNKSIZE = 5000

class GeoPandasBackend(PandasBackend):

    def register_handlers(self, handlers):
        super().register_handlers(handlers)
        handlers["create_table"].register(geopandas.GeoDataFrame, self._create_table_from_geopandas)

    def _create_table_from_geopandas(self, txn, table_name, df, parameters, if_exists, kws):
        logging.debug("Creating table from geopandas")
        chunksize = txn._driver._pop_kw(kws, "chunksize", DEFAULT_CHUNKSIZE)
        schema, table_name = split_table_name(table_name)
        return df.to_postgis(table_name, txn._conn,
                             schema="main" if schema is None else schema,
                             if_exists=if_exists,
                             index=False, chunksize=chunksize, **kws)

    def _df_read_sql(self, txn, sqla, geom_col=None, **kws):
        if geom_col is None:
            return pandas.read_sql(sqla, txn._conn, **kws)
        else:
            return geopandas.read_postgis(sqla, txn._conn, geom_col=geom_col, **kws)

    def _df_concat(self, dfs):
        if isinstance(dfs[0], geopandas.GeoDataFrame):
            return geopandas.concat(dfs)
        else:
            return pandas.concat(dfs)
