# -*- coding: utf-8 -*-
import sys
import json
import pandas as pd
from datayes import Client
    
def get_fund_nav(st, et):
    try:
        client = Client()
        client.init('ba1cccf77c33371b09c9f6394c72d82f70c55d1edf1ca809c255389cd1dbe8bc') 
	url='/api/fund/getFundNav.json?startDate=%s&endDate=%s' % (st, et)
        code, result = client.getData(url)
        if code==200:
            return pd.DataFrame(json.loads(result)['data'])
        else:
            print code
    except Exception, e:
        raise e


def get_fund_info():
    try:
        client = Client()
        client.init('ba1cccf77c33371b09c9f6394c72d82f70c55d1edf1ca809c255389cd1dbe8bc')

        url='/api/fund/getFund.json?listStatusCd='
        code, result = client.getData(url)
        if code==200:
            return pd.DataFrame(json.loads(result)['data'])
        else:
            print code
    except Exception, e:
        raise e


def get_alpha():
    df = pd.read_csv('fund.nav', sep='\t', dtype={'ticker':str})
    df.set_index(['ticker', 'publishDate'], inplace=True)
    idx = df.index.get_level_values(level=0).unique()
    data_list = []
    for i in idx:
        cur_df = df.ix[i]
        cur_df.loc[:, 'ticker'] = i
        cur_df.loc[:, 'return20'] = cur_df.ADJUST_NAV.pct_change(periods=20)
	cur_df.loc[:, 'return30'] = cur_df.ADJUST_NAV.pct_change(periods=30)
        cur_df.loc[:, 'return60'] = cur_df.ADJUST_NAV.pct_change(periods=60)
	cur_df.loc[:, 'vol1'] = cur_df.ADJUST_NAV.rolling(2).apply(lambda x: math.log(x[1]/x[0]))	
	cur_df.loc[:, 'vol20'] = cur_df.vol1.rolling(20).apply(lambda x: \
		pd.Series(x).ewm(com=0.5).mean().iloc[-1])
	cur_df.loc[:, 'vol60'] = cur_df.vol1.rolling(60).apply(lambda x: \
		pd.Series(x).ewm(com=0.5).mean().iloc[-1])
        cur_df.loc[:, 'max_drawdown20'] = cur_df.ADJUST_NAV.rolling(20).apply(lambda x: \
		max(x[0] - x[1: ]) / x[0])
	cur_df.loc[:, 'max_drawdown60'] = cur_df.ADJUST_NAV.rolling(60).apply(lambda x: \
		max(x[0] - x[1: ]) / x[0])
	cur_df.loc[:, 'sharp20'] = cur_df.apply(lambda x:(x.return20 - 0.03) / x.max_drawdown20 \
					if x.max_drawdown20 else 0, axis=1)
        cur_df.loc[:, 'sharp60'] = cur_df.apply(lambda x:(x.return60 - 0.03) / x.max_drawdown60 \
					if x.max_drawdown60 else 0, axis=1)
	data_list.append(cur_df.reset_index())
    return data_list 

        	
if __name__ == '__main__':
    df_nav = get_fund_nav('20170101', '20170901')
    df_nav.to_csv('fund.nav', sep='\t', encoding='utf8')
    df = pd.concat(get_alpha()).set_index('ticker')
    df.loc[df.publishDate=='2017-09-01', ['secShortName', 'return20']].\
		sort_values(by='return20').to_csv('fund_return20.dat',encoding='utf8')
	
 
	        

