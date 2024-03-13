import pandas as pd
import math
from scipy.stats import t
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm


df = pd.read_csv('PAD_09_PD.csv', delimiter=';')


# Zadanie 1

alpha = 0.05
m = df[df['Gender']=='Male']['Annual Income (k$)']
f = df[df['Gender']=='Female']['Annual Income (k$)']

def calculate_t(x, y):
	mean_x = x.mean()
	mean_y = y.mean()
	std_x = x.std()
	std_y = y.std()
	n_x = x.shape[0]
	n_y = y.shape[0]
	result = (mean_x-mean_y)/math.sqrt((std_x**2/n_x)+(std_y**2/n_y))
	return result

def calculate_P(x, y):
	my_t = calculate_t(x, y)
	print(f't: {my_t}')
	P = t.cdf(-my_t, min(x.shape[0], y.shape[0])-1) * 2
	print(f'P: {P}')
	return P

def print_null(P, alpha):
	print(f'P :{P}')
	print(f'alpha: {alpha}')
	if P<alpha:
		print('so the null hypothesis is true')
	else:
		print('so the null hypothesis isn\'t true') 
	print()

P = calculate_P(m, f)
print_null(P, alpha)

# Zadanie 2

df = df.replace(to_replace='Male', value=0)
df = df.replace(to_replace='Female', value=1)
X = df[['Gender', 'Age', 'Annual Income (k$)']]
y = df['Spending Score (1-100)']

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())
pred = model.predict()

model_df = pd.read_html(model.summary().tables[1].as_html(),header=0,index_col=0)[0]
print(model_df['P>|t|'])
print()
print(model_df['std err'])
print()
print(model_df['coef'])
print()

P1 = calculate_P(df['Gender'], df['Age'])
P2 = calculate_P(df['Gender'], df['Annual Income (k$)'])
P3 = calculate_P(df['Age'], df['Annual Income (k$)'])
print_null(P1, alpha)
print_null(P2, alpha)
print_null(P3, alpha)
