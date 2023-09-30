

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import datetime


from sklearn import metrics

def get_expected_wins(week):

    team_data = pd.read_csv('prod_data/fantasy_team_stats.csv')

    fant = team_data.copy() #dataset used for model
    if week > 1:
        fant = fant[fant['week'] < week] #ignore current_week

    #result is a win
    fant['result'] = (fant['points'] > fant['opp_points']).astype(int)

    X = fant[['points']] #independent variable
    y = fant.result #dependent variable

    #train test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=16)

    # model building
    model = LogisticRegression(random_state=0)
    model.fit(X_train, y_train)
    LogisticRegression(random_state=0)

    #model results
    expected_wins_model = {'intercept': model.intercept_[0], 'coefficient': model.coef_[0][0]}

    #create expected wins column
    team_data['expected_wins'] = 1 / (1+np.exp(-(expected_wins_model['intercept'] + team_data['points'] * expected_wins_model['coefficient'])))


    #overwrite team data
    team_data.to_csv('prod_data/fantasy_team_stats.csv', index=False)

    expected_wins_df = pd.DataFrame([expected_wins_model])
    expected_wins_df.to_csv('prod_data/expected_wins.csv', index=False)

    print ('expected wins are done')


    return None

if __name__ == '__main__':
    get_expected_wins()
