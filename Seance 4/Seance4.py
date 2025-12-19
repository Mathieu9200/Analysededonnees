import numpy as np
import pandas as pd
import scipy
import scipy.stats
import matplotlib.pyplot as plt

def get_stats(dist_name, params):
    dist = getattr(scipy.stats, dist_name)
    mean, var = dist.stats(*params, moments='mv')
    return mean, np.sqrt(var)

def visualize(dist_name, params, kind='continuous', label=None):
    if not label: label = dist_name
    dist = getattr(scipy.stats, dist_name)
    
    # Calcul des stats
    mean, std = get_stats(dist_name, params)
    print(f"{label} : Moyenne = {mean:.2f}, Ecart-type = {std:.2f}")

    plt.figure(figsize=(6, 4))
    if kind == 'continuous':
        start = dist.ppf(0.001, *params)
        end = dist.ppf(0.99, *params)
        x = np.linspace(start, end, 100)
        plt.plot(x, dist.pdf(x, *params), 'r-', label='PDF')
        plt.fill_between(x, dist.pdf(x, *params), alpha=0.2, color='red')
    else:
        low = int(dist.ppf(0.001, *params))
        high = int(dist.ppf(0.99, *params))
        if high == low: high += 1 
        if high > low + 40: high = low + 40 
        x = np.arange(low, high + 1)
        plt.stem(x, dist.pmf(x, *params), label='PMF')
    
    plt.title(label)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Variables discrètes
    visualize('randint', (5, 6), 'discrete', 'Loi de Dirac (5)')
    visualize('randint', (1, 7), 'discrete', 'Loi Uniforme Discrète (1-6)')
    visualize('binom', (10, 0.5), 'discrete', 'Loi Binomiale (n=10, p=0.5)')
    visualize('poisson', (3,), 'discrete', 'Loi de Poisson (mu=3)')
    visualize('zipf', (3,), 'discrete', 'Loi de Zipf (a=3)')

    # Variables continues
    visualize('norm', (0, 1), 'continuous', 'Loi Normale')
    visualize('lognorm', (1,), 'continuous', 'Loi Log-Normale')
    visualize('uniform', (0, 1), 'continuous', 'Loi Uniforme')
    visualize('chi2', (5,), 'continuous', 'Loi du Chi2')
    visualize('pareto', (3,), 'continuous', 'Loi de Pareto')
