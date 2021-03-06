import seaborn as sns
import matplotlib.pyplot as plt
import ssl
import pandas as pd 
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

sns.set(style="white")
# 获取数据

def str2time(str):
    return float(str.split(':')[1])

def get_line_plot():
    fig, ax1 = plt.subplots()

    dataset = pd.read_csv("./Hipster/results/f1/replicas.csv")
    dataset.columns = ['rca', 'replicas', '1fPR@1', '1fMAP@1', '2fPR@2', '2fMAP@2']

    print(dataset)
    ax1 = sns.lineplot(y="1fMAP@1", x="replicas", hue="rca", style='rca', markers=True, linewidth=2, data=dataset)
    box = ax1.get_position()
    my_y_ticks = np.arange(0, 1.01, 0.1)
    plt.yticks(my_y_ticks)
    # ax1.set_position([box.x0, box.y0, box.width , box.width* 0.8])
    # ax1.legend(loc='center left', bbox_to_anchor=(0.2, 1.12),ncol=3)
    ax1.legend( bbox_to_anchor=(0.75, 0.98), loc=2, borderaxespad=0, numpoints=1)
    fig.subplots_adjust(right=0.8)
    plt.show()

def get_bar_plot():
    fig, ax1 = plt.subplots()

    dataset = pd.read_csv("results/test1.csv")
    dataset.columns = ['method', 'value', 'type']

    print(dataset)
    ax1 = sns.barplot(y="value", x="type", hue="method", data=dataset)
    box = ax1.get_position()
    # ax1.set_position([box.x0, box.y0, box.width , box.width* 0.8])
    # ax1.legend(loc='center left', bbox_to_anchor=(0.2, 1.12),ncol=3)
    ax1.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, numpoints=1)
    fig.subplots_adjust(right=0.8)
    plt.show()

def get_box_plot():
    
    fig, ax1 = plt.subplots()

    plt.figure(figsize=(10, 5))

    time_df = pd.read_csv("THipster/results/test.csv")
    time_df.columns = ['time', 'svc', 'value', 'rca']
    
    value_list = []
    for row in time_df.itertuples():
        time0 = str2time(getattr(row, 'value'))
        value_list.append(time0)
    
    time_df.loc[:,('value')] = value_list

    print(time_df)
    ax1 = sns.boxplot(x='svc' , y='value' , hue='rca', data=time_df)
    # box = ax1.get_position()
    # ax1.set_position([box.x0, box.y0, box.width , box.width* 0.8])
    # ax1.legend(loc='center left', bbox_to_anchor=(0.2, 1.12),ncol=3)

    # 这两个
    # ax1.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, numpoints=1)
    # fig.subplots_adjust(right=0.8)
    plt.show()

if __name__ == "__main__":
    # get_bar_plot()
    # get_box_plot()
    get_line_plot()