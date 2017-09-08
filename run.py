#----------------------------
#@author: pompompurin
#@func: calc long-term momentum for stock selection
#----------------------------
import time
import tushare as ts

industry_list = [u'仪器仪表', u'电子信息', u'电子器件']


def get_momentum(x):
    print x
    time.sleep(30) # otherwise http error 456
    retry = 5
    df_hist = None
    while retry > 0:
        try:
    	    df_hist = ts.get_h_data(x, '2016-09-07', '2017-09-06')
        except Exception as e:
            time.sleep(1)
            retry -= 1
            continue
        break
    if df_hist is None:
        return -100.0
    if 'open' in df_hist.columns:
    	start_price = df_hist.open.ix[-1]
    elif 'close' in df_hist.columns:
	start_price = df_hist.close.ix[-1]
    else:
        return -100.0
    end_price = df_hist.close.ix[0]
    return 100.0 * (end_price - start_price) / start_price

df_industry = ts.get_industry_classified()
df_e = df_industry[df_industry.c_name.isin(industry_list)]
df_e.loc[:, 'momentum'] = [-100.0 for _ in range(len(df_e))]
for code in df_e.code.unique():
    if df_e.loc[df_e.code==code, 'momentum'].tolist()[0] != -100:
	continue
    df_e.loc[df_e.code==code, 'momentum'] = get_momentum(code)

