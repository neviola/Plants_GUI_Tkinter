from matplotlib import pyplot as plt
from .sync_values import data_for_charts
from datetime import datetime, timedelta
from collections import Counter

plt.style.use('seaborn')

time_one_day_less = datetime.now() - timedelta(hours=24.0)
time_x = []
# lista sa datetime objects za x os 
for i in range(24):
     time_x.append(time_one_day_less)
     time_one_day_less += timedelta(hours=1.0)



def one_day_temp(graph_type):

    temp_y = data_for_charts()[0]
    
    if graph_type == 'line':
        plt.plot(time_x, temp_y)

    # BAR plot
    else:
        plt.bar(time_x, temp_y, width=0.04)
        
    plt.title('Air temperature in the last 24h [random]')
    plt.xlabel('Time')
    plt.ylabel('Temperature [C]')
    plt.tight_layout()
    plt.show()


def one_day_moist(graph_type):
    
    moist_y = data_for_charts()[1]
    
    if graph_type == 'line':       
        plt.plot(time_x, moist_y)
    else:
        plt.bar(time_x, moist_y, width=0.04)

    plt.title('Soil moiusture in the last 24h [random]')
    plt.xlabel('Time')
    plt.ylabel('Moisture [%]')
    plt.tight_layout()
    plt.show()


def one_day_ph(graph_type):
    
    ph_y = data_for_charts()[2]

    if graph_type == 'line':       
        plt.plot(time_x, ph_y)
    else:
        plt.bar(time_x, ph_y, width=0.04)
    
    plt.title('Soil pH in the last 24h [random]')
    plt.xlabel('Time')
    plt.ylabel('Acidity [pH]')
    plt.tight_layout()
    plt.show()


def one_day_salinity(graph_type):
    
    sal_y = data_for_charts()[3]
    if graph_type == 'pie':
        count = Counter(sal_y)

        slices = [count['Non-saline'], count['Slightly Saline'],  count['Moderately saline'], count['Very saline'], count['Highly saline']]
        labels = ['Non-saline', 'Slightly Saline',  'Moderately saline', 'Very saline', 'Highly saline']
        plt.pie(slices, labels=labels, shadow=True, startangle=90,
                autopct='%1.1f%%',
                wedgeprops={'edgecolor': 'black'}
                )
    elif graph_type == 'line':
        sal_y_num = []
        for sal in sal_y:
            if sal == 'Non-saline':
                sal_y_num.append(0)
            elif sal == 'Slightly saline':
                sal_y_num.append(1)
            elif sal == 'Moderately saline':
                sal_y_num.append(2)
            elif sal == 'Very saline':
                sal_y_num.append(3)
            else:
                sal_y_num.append(4)
        
        plt.plot(time_x, sal_y_num, label='4 - Highly Saline\n3 - Very Saline\n2 - Moderately Saline\n1 - Slightly Saline\n0 - Non-saline')
        plt.xlabel('Time')
        plt.ylabel('Salinity level every hour in the last 24h')  
        plt.legend()

    # bar chart
    else:
        sal_y_num = []
        for sal in sal_y:
            if sal == 'Non-saline':
                sal_y_num.append(0)
            elif sal == 'Slightly saline':
                sal_y_num.append(1)
            elif sal == 'Moderately saline':
                sal_y_num.append(2)
            elif sal == 'Very saline':
                sal_y_num.append(3)
            else:
                sal_y_num.append(4)

        plt.bar(time_x, sal_y_num, width=0.04, label='4 - Highly Saline\n3 - Very Saline\n2 - Moderately Saline\n1 - Slightly Saline\n0 - Non-saline')
        plt.xlabel('Time')
        plt.ylabel('Salinity Level')
        plt.legend()

    plt.title('Soil salinity in the last 24h [random]')
    plt.tight_layout()
    plt.show()


def one_day_light(graph_type):
    
    light_y = data_for_charts()[4]
    # pie plot
    if graph_type == 'pie':
        count = Counter(light_y)
        slices = [count['None'], count['Very low'], count['Low'], count['Moderate'], count['High'], count['Very High']]
        labels = ['None', 'Very low', 'Low', 'Moderate', 'High', 'Very High']

        plt.pie(slices, labels=labels, shadow=True, startangle=90,
                autopct='%1.1f%%',
                wedgeprops={'edgecolor': 'black'}
                )
    
    # line plot
    elif graph_type == 'line':
        light_y_num = []
        for lght in light_y:
            if lght == 'None':
                light_y_num.append(0)
            elif lght == 'Very low':
                light_y_num.append(1)
            elif lght == 'Low':
                light_y_num.append(2)
            elif lght == 'Moderate':
                light_y_num.append(3)
            elif lght == 'High':
                light_y_num.append(4)
            else:
                light_y_num.append(5)
        
        plt.plot(time_x, light_y_num, label='5 - Very High\n4 - High\n3 - Moderate\n2 - Low\n1 - Very low\n0 - None')
        plt.xlabel('Time')
        plt.ylabel('Light level')
        plt.legend()
        
    # bar plot  
    else:
        light_y_num = []
        for lght in light_y:
            if lght == 'None':
                light_y_num.append(0)
            elif lght == 'Very low':
                light_y_num.append(1)
            elif lght == 'Low':
                light_y_num.append(2)
            elif lght == 'Moderate':
                light_y_num.append(3)
            elif lght == 'High':
                light_y_num.append(4)
            else:
                light_y_num.append(5)

        plt.bar(time_x, light_y_num, width=0.04, label='5 - Very High\n4 - High\n3 - Moderate\n2 - Low\n1 - Very low\n0 - None')
                
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Light Level')
    
    plt.title('Hourly Light levels in the last 24h [random]')    
    plt.tight_layout()
    plt.show()



# one_day_temp('line')
# one_day_moist('line')
# one_day_ph('line')
# one_day_salinity('')
# one_day_light('line')