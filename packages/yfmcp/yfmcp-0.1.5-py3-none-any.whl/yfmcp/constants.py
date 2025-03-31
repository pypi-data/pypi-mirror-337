import yfinance.const


def _get_industry_list() -> list[str]:
    industry_list = []
    for sector_industries in yfinance.const.SECTOR_INDUSTY_MAPPING.values():
        for industry in sector_industries:
            industry_list.append(industry)
    return sector_industries


SECTOR_LIST = list(yfinance.const.SECTOR_INDUSTY_MAPPING.keys())
INDUSTRY_LIST = _get_industry_list()
