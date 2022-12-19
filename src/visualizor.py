import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix
from matplotlib.gridspec import GridSpec
from matplotlib import cycler


# define custom plot style based on ggplot
style = plt.style.library['ggplot']
style['axes.facecolor'] = '#eaeaea'
style['legend.frameon'] = False
style['axes.prop_cycle'] = cycler('color', ['#348ABD', '#E24A33', '#8EBA42', '#988ED5', '#777777', '#FBC15E', '#FFB5B8'])
plt.style.use(style)
# above code is executed whenever this script is imported, thus applying the style


def ratings_heatmap(ratings):
    fig = plt.figure(figsize=(14, 6))
    gs = GridSpec(2, 3, figure=fig, height_ratios=[10, 1])

    top_ax = fig.add_subplot(gs[1, :])

    ax = [fig.add_subplot(gs[0, i]) for i in range(3)]

    for i in range(3):
        j = (i + 1) % 3
        if i == 2:
            sns.heatmap(confusion_matrix(ratings[:, i], ratings[:, j]), ax=ax[i], annot=True, square=True,
                        cbar_ax=top_ax, vmin=0, vmax=70, cbar_kws={'orientation': 'horizontal'})
        else:
            sns.heatmap(confusion_matrix(ratings[:, i], ratings[:, j]), ax=ax[i], annot=True, square=True, cbar=False,
                        vmin=0, vmax=70)
        ax[i].set_xlabel(f'Annotator {i + 1}')
        ax[i].set_ylabel(f'Annotator {j + 1}')
        ax[i].set_xticklabels(['positive', 'neutral', 'negative', 'not app..'])
        ax[i].set_yticklabels(['positive', 'neutral', 'negative', 'not app..'], va='center')


def num_comments_cdf(ratings):
    x = np.linspace(0, 1, 1000)
    y = ratings.num_comments.quantile(x)
    fig, ax = plt.subplots()
    ax.plot(y, x)
    ax.fill_between(y, x, alpha=.2)
    ax.set_xscale('log')
    fig.suptitle('Cumulative density function of log #comments')
    ax.set_xlabel('Log number of comments')
    ax.set_ylabel('Quantile')

    ax.set_ylim(0, 1.05)
    ax.set_xlim(0, y.max())
