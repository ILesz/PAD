import pandas as pd
import plotly.express as px

df = pd.read_csv('water_potability.csv')
pd.options.display.max_columns = None
print(df.head())
print(df.describe())
df = df.replace({'Potability':1}, 'yes')
df = df.replace({'Potability':0}, 'no')
df = df.sample(frac = 1)
df['index'] = [i for i in range(df.shape[0])]
	

for col in df.columns.to_list()[:-2]:
	fig = px.scatter(df, x='index', y=col, color='Potability', trendline='ols', marginal_y='violin')
	fig.show()
	
for col in df.columns[:-2]:
	name = col+'-dist-mean-sq'
	mean = df[col].mean()
	df[name] = (df[col]-mean)**2


import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
X = df.drop(columns=['Potability', 'index'])
df = df.replace({'Potability':'yes'}, 1)
df = df.replace({'Potability':'no'}, 0)
y = df['Potability']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
model = LogisticRegression(max_iter=1000, solver='lbfgs')
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
print(confusion_matrix)
acc = metrics.accuracy_score(y_test, y_pred)
prec = metrics.precision_score(y_test, y_pred)
recall = metrics.recall_score(y_test, y_pred)
f1 = metrics.f1_score(y_test, y_pred)
print(acc)
print(prec)
print(recall)
print(f1)
