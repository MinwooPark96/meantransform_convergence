import numpy as np
import matplotlib.pyplot as plt
import copy
import os
import seaborn as sns
import pandas as pd
import random

from src import transform


def save(meantrans : transform.MeanTransform, name):
    
    assert isinstance(meantrans,transform.MeanTransform) == True ,'meantrans is not Meantrans object'

    plt.figure(figsize=(16,4))
    
    df = pd.DataFrame({'norm':meantrans.normal_characteristic_list,"iter":range(meantrans.n+1)})
    df.set_index('iter',inplace=True)
    
    ax = sns.lineplot(data = df, x = 'iter', y='norm',lw = 2.5,
                 dashes = False, markersize = 8 , markers=['o']
                )
    for axis in ['bottom', 'left']:
        ax.spines[axis].set_linewidth(2.5)
        ax.spines[axis].set_color('0.2')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(width = 2.5, color = '0.2')

    # plt.xticks(size = 14, weight = 'bold', color = '0.2')
    # plt.yticks(size = 14, weight = 'bold', color = '0.2')
    
    plt.xlim(0,meantrans.n)
    
    # plt.yscale('log')
    
    # try:
    #     plt.locator_params(axis='x', nbins=meantrans.n/10)
    # except:
    #     pass
    

    ax.set_xlabel(ax.get_xlabel(), fontsize = 14, weight = 'bold', color = '0.2')
    ax.set_ylabel(ax.get_ylabel(), fontsize = 14, weight = 'bold', color = '0.2')
    
    plt.grid(True,linestyle = '--',linewidth=0.5)
    
    title_font = {
    'fontsize': 16,
    'fontweight': 'bold'
    }
    
    plt.title("The Normal Characteristic of Matrix", fontdict=title_font, loc='left', pad=20)
    
    # total_ax.plot(range(meantrans.n+1),meantrans.normal_characteristic_list,color="b",alpha=0.5,marker="o",linestyle="dashed")
    
    os.makedirs('figure',exist_ok=True)
    plt.savefig('figure/'+name+'.png', bbox_inches = 'tight', dpi = 250, facecolor = ax.get_facecolor())

    os.makedirs('norm',exist_ok=True)
    df.to_csv('norm/'+name+'.csv')

    os.makedirs('matrix',exist_ok=True)
    np.save('matrix/'+name,np.array(meantrans.get_sequence))
    
    
def generate_random_complex(dim,seed = 42):
    gen_list = list()
    random.seed(seed)
    def generate_one_random_complex():
        real_part = random.uniform(-100, 100)  # 임의의 범위에서 실수부 생성
        imaginary_part = random.uniform(-100, 100)  # 임의의 범위에서 허수부 생성
        return complex(real_part, imaginary_part)  # 복소수 생성
    
    for _ in range(dim*dim):
        gen_list.append(generate_one_random_complex())
    
    return np.matrix(gen_list).reshape(dim,dim)

def load_matrix(name,dir='matrix/'):
    return list(np.load(dir+name))


def is_decreasing(nr_ch : list) -> bool:
    if len(nr_ch) <= 1:
        return True
    
    e = 1e-14
    
    i = 0
    
    while i < len(nr_ch)-1:
        if nr_ch[i+1] < e:
            break
        
        d = nr_ch[i] - nr_ch[i+1]
        
        if d < 0:
            return False
        i+=1
    
    return True