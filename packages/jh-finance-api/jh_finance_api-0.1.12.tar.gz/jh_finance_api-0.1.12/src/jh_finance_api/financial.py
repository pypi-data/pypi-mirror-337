import sys; sys.dont_write_bytecode=True
import pandas as pd


# =========================================== #
# ================ Endpoints ================ #
# =========================================== #
def _list(pages=10):
    return pd.read_json(f'http://project-finance-backend.onrender.com/financial-list?pages={pages}')


def raw(slug='microsoft'):
    return pd.read_json(f'http://project-finance-backend.onrender.com/financial-raw/{slug}')


def ratios(slug='microsoft'):
    res     = pd.read_json(f'http://project-finance-backend.onrender.com/financial-ratios/{slug}')
    Raw     = pd.DataFrame([dict(x) for x in res['Raw']])
    Ratios  = pd.DataFrame([dict(x) for x in res['Ratios']])
    return Raw, Ratios