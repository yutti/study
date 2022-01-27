import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

class  stock_data_graff:

    def __init__(self) : 
        self.stock_date  = 0        

    def d_stock(self, date_term, xxl, yyl1, yyl2, yyl3, yyl4, yyl2_1, yl3_min, yl2_max, save_file) :
       
        #max,minの計算
        #yl3_min = yyl3.min() 
        #yl2_max = yyl2.max() 
        y1_min = math.floor(yl3_min / 100) * 100
        y1_max = math.ceil(yl2_max  / 100) * 100

        # Figureを設定
        fig = plt.figure()
        fig = plt.figure(figsize=(8,6))

        # Axesを追加
        ax1 = fig.add_subplot(111)

        plt.xticks(rotation=45)

        ax1.set_title(date_term)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('stock plice')

        ax1.plot(xxl, yyl1,color = "green",  linestyle = "solid",  label = "Open")
        ax1.plot(xxl, yyl2,color = "red",    linestyle = "dashed", label = "High")
        ax1.plot(xxl, yyl3,color = "blue",   linestyle = "dashed", label = "Low")
        ax1.plot(xxl, yyl4,color = "orange", linestyle = "solid",  label = "Close")

        #Add bar for 2rd label
        ax2 = ax1.twinx()
        ax2.bar(xxl,yyl2_1,color="lightblue",label="Volume")
        #X軸レンジ調整
        ax2.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        #ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        
        #Swap before and after the graph
        ax1.set_zorder(2)
        ax2.set_zorder(1)
        ax1.patch.set_alpha(0)
        ax1.grid(True)  # grid 表示 ON
        plt.ticklabel_format(style='plain',axis='y')
        plt.rcParams['figure.subplot.bottom'] = 0.1 #下端の調整

        ax1.set_ylim(y1_min,y1_max)
        ax2.set_ylim(0,10000000)

        plt.show()
        
        #画像の保存
        fig.savefig(save_file)
        
