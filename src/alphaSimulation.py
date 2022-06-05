import numpy as np

n_MAX_customers = 10000 # Number of customers
n = 2 # number of products
size = n+1
alpha = np.zeros(size) # ?? aplha 0 => competitor website, alpha 1 => product 1, ...
alpha_ratio = [2/3, 2/9, 1/9] #Probability to go on page 0, 1, ... How to choose te mu ?

alpha = np.random.multinomial(n_MAX_customers, alpha_ratio)

# np.random.shuffle(alpha)
print(alpha)
alpha_noise = np.random.dirichlet(alpha,size=None)

print(alpha_noise)
