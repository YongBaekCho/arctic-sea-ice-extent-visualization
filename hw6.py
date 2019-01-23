import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Author: YongBaek Cho
# Date : 10/11/2018

# Description: This program will call the csv file and create the line graph with using matplotlib
def get_column_labels():
#Generate and return a list of strings that will be used as column labels in a DataFrame  
    dates = pd.date_range('1/1/2018', periods=365)
    list_string = []

    for i in range(len(dates)):
        if dates[i].month < 10:
            if dates[i].day < 10:
                list_string.append(str(0) + str(dates[i].month) + str(0) + str(dates[i].day))
            else:
                list_string.append(str(0) + str(dates[i].month) + str(dates[i].day))
        else:
            if dates[i].day < 10:
                list_string.append(str(dates[i].month) + str(0) + str(dates[i].day))
            else:
                list_string.append(str(dates[i].month) + str(dates[i].day))

    return list_string
    
def get_2018():
    # This function reads the data from data_2018.csv
    df = pd.read_csv('data_2018.csv',names = [1,'Extent'],  usecols = [0,1],parse_dates = {'Dates': [0]}, header= None)
    data = df['Extent'].values
    col = get_column_labels()[:len(data)]
    ts = pd.Series(data,col)
    return ts
    
def extract_fig_1_frame(df):
    # This function takes the DataFrame from Hw5
    MeanList = []
    SdList = []

    for i in range(len(df.columns)):
        MeanList.append(df.iloc[:,i].mean())
        SdList.append((df.iloc[:,i].std()) * 2)

    df2 = pd.DataFrame([MeanList,SdList], index = ['mean','two_s'],columns = df.columns)

    return df2

def extract_fig_2_frame(df):
    # This function takes the DataFrame from hw5.
    MeanList = []

    df2 = pd.DataFrame(index = ['1980s','1990s','2000s','2010s'],columns=df.columns)

    for i in range(len(df.columns)):
        df2.iloc[0,i] = df.iloc[1:11,i].mean()
        df2.iloc[1,i] = df.iloc[11:21,i].mean()
        df2.iloc[2,i] = df.iloc[21:31,i].mean()
        df2.iloc[3,i] = df.iloc[31:39,i].mean()

    return df2
    
def make_fig_1(f1,df):
    '''
    This functions takes a figure 1 frame and DataFrmae from hw5, and creates a figure.
    '''
    
    f1.loc['mean'].plot(label='mean')
    df.loc[2012].plot(linestyle='dashed',label='2012')
    get_2018().plot(label='2018')
    
    ax = plt.gca()
    ax.set_ylabel(r"NH Sea Ice Extent ($10^6$ km$^2$)")
    ax.yaxis.label.set_fontsize(24)
    ax.set_xlim(0,len(f1.loc['mean',:]))
    low = f1.loc['mean',:]-f1.loc['two_s',:]
    up = f1.loc['mean',:]+f1.loc['two_s',:]
    rang = np.arange(0,len(f1.loc['mean',:]))
    ax.fill_between(rang, low, up, color='lightgray',label=r'$\pm$2 std devs')
    ax.set_xticklabels(['0101','0220','0411','0531','0720','0908','1028','1217'])

    plt.legend()
def make_fig_2(f2,df):
    # This function takes a figure 2 frame and creates a figure.
    
    pltDF = extract_fig_2_frame(df)
    df2018 = get_2018()
    
def make_fig_2(df2):
    b = get_Mar_Sept_frame()    
    
    plt.plot(pltDF.loc['1980s',:], linestyle = 'dashed')
    plt.plot(pltDF.loc['1990s',:], linestyle = 'dashed')
    plt.plot(pltDF.loc['2000s',:], linestyle = 'dashed')
    plt.plot(pltDF.loc['2010s',:], linestyle = 'dashed')
    plt.plot(df2018)
    
    ax = plt.gca()
    ax.set_ylabel(r"NH Sea Ice Extent ($10^6$ km$^2$)")
    ax.set_xlim(0,len(pltDF.loc['1980s',:]))
    ax.yaxis.label.set_fontsize(24)
    ax.set_xticks(['0101','0220','0411','0531','0720','0908','1028','1217'])
    march_ols_params = get_ols_parameters(pd.Series(df2['March_means'], df2.index))
    xs_m = np.arange(1979, 2018)
    ys_m = march_ols_params[0] * xs_m + march_ols_params[1]
    plt.plot(xs_m, ys_m)
    plt.legend(['1980s','1990s','2000s','2010s','2018'])


def main():
    '''
    This main function creates Dataframe by using csv file and create figures.
    '''
    
    filename = "data_79_17.csv"
    
    df = pd.read_csv(filename,index_col=0)
    f1 = extract_fig_1_frame(df)
    f2 = extract_fig_2_frame(df)
    
    make_fig_1(f1,df)
    plt.figure()
    make_fig_2(f2,df)
    plt.show()
    

main()