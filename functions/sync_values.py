'''ovdje se generiraju svi podaci sa senzora sa 'sync' gumbom'''

import random
from datetime import datetime
from .api_weather import get_current_info


def generate_values():

    moisture = random.randint(0,100)
    ph = random.randint(55, 75)/10
    
    # mnozim kako bi se neke vrijednosti pokazale cesce sto je realnije
    non_saline =  ['Non-saline'] * 3
    slightly = ['Slightly saline'] * 5
    moderate = ['Moderately saline'] * 4
    very = ['Very saline'] * 2
    salinity_list = non_saline + slightly + moderate + very + ['Highly saline']
    salinity = random.choice(salinity_list)
    
    # ako je noc onda nema svjetlosti
    hrs_now = datetime.now().hour
    if hrs_now <= 6 or hrs_now >= 19:
        light_level = 'None'
    elif hrs_now <= 8 or hrs_now >=17:
        light_level = 'Very low'
    elif hrs_now <= 9 or hrs_now >=16:
        light_level = 'Low'
    elif hrs_now <= 10 or hrs_now >=15:
        light_level = 'Moderate'
    elif hrs_now <= 11 or hrs_now >=14:
        light_level = 'High'
    else:
        light_level = 'Very High'
    
    return moisture, ph, salinity, light_level


def data_for_charts():
    # generira podatke za proteklih 24h za grafove

    temp = get_current_info()
    moisture, ph, salinity, light_level = generate_values()

    temp_list = []
    moisture_list = []
    ph_list = []
    sal_list = []
    light_options = ['None', 'Very low', 'Low', 'Moderate', 'High', 'Very High']
    light_list = []

    # generira random vrijednosti 
    for hour in range(23):
        temp_list.append(round(random.randint(90, 110)/100 * temp, 2))
        moisture_list.append(round(random.randint(88, 110)/100 * moisture, 0))
        ph_list.append(round(random.randint(95, 105)/100 * ph, 1))
        sal_list.append(generate_values()[2]) 
        light_list.append(random.choice(light_options))

    temp_list.append(temp)
    moisture_list.append(moisture)
    ph_list.append(ph)
    sal_list.append(salinity)
    light_list.append(random.choice(light_options))

    return temp_list, moisture_list, ph_list, sal_list, light_list

# print(data_for_charts())

