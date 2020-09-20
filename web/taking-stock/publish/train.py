# Don't upload this file to production.
# Train models locally and copy them into the deployment

import os
import joblib
import quandl
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

WINDOW = 30
quandl.ApiConfig.api_key = "REDACTED"

def get_data(name, cache=True):
    fn = f'{name.replace("/", "_")}.cache.joblib'
    if cache:
        if os.path.isfile(fn):
            df = joblib.load(fn)
            return df

    df = quandl.get(name)
    joblib.dump(df, fn)

    return df

def get_model(data):
    df = data[['Adj. Close']]
    df['Prediction'] = df[['Adj. Close']].shift(-WINDOW)

    ds = np.array(df.drop(['Prediction'], 1))
    ds = ds[:-WINDOW]

    lb = np.array(df['Prediction'])
    lb = lb[:-WINDOW]

    ds_train, ds_test, lb_train, lb_test = train_test_split(ds, lb, test_size=0.2)

    model = LinearRegression()
    model.fit(ds_train, lb_train)

    return model

if __name__ == '__main__':
    import sys
    stock = sys.argv[1]
    stock_name = stock.split('/')[1]
    use_cache = len(sys.argv) > 2 and sys.argv[2] == '--no-cache'

    data = get_data(stock, cache=sys.argv)
    model = get_model(data)
    joblib.dump(model, f'{stock_name}.joblib')
