#----------------------------
#@author: pompompurin
#@func: calc long-term momentum for stock selection
#----------------------------
import time
import tushare as ts

industry_list = [u'仪器仪表', u'电子信息', u'电子器件']


def get_momentum(x):
    time.sleep(30) # otherwise http error 456
    retry = 5
    while retry > 0:
        try:
    	    df_hist = ts.get_h_data(x['code'], '2016-09-07', '2017-09-06')
        except Exception as e:
            time.sleep(1)
            retry -= 1
            continue
        break
    start_price = df_hist.open.ix[-1]
    end_price = df_hist.close.ix[0]
    return 100.0 * (end_price - start_price) / start_price

df_industry=ts.get_industry_classified()
df_e=df_industry[df_industry.c_name.isin(industry_list)]
df_e.loc[:, 'momentum'] = df_e.apply(get_momentum, axis=1)

