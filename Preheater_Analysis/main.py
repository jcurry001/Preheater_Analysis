# This python script will analyze the Preheater

import iapws as pt
import pandas as pd
import numpy as np
import datetime
import os
from tkinter import filedialog
import matplotlib.pyplot as plt


import warnings
warnings.simplefilter(action='ignore', category=Warning)

# Functions


def f_to_k(f):
    k = (f-32)*5/9+273
    return k


def gpm_to_m3per_sec(gpm):
    m3per_sec = gpm*0.00006309
    return m3per_sec


def kw_to_w(kw):
    w = kw*1000
    return w


def point_slope_form(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    b = (y1-m*x1)
    return m, b


def filename(analized, filetype, starttime=0, endtime=0):
    today = datetime.date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    file_name_to_use = str.replace(str.replace(f'{analized}{month}_{day}_{year}_between{starttime}_and_{endtime}{filetype}', ' ', ''), ':', '_')
    return file_name_to_use


### Preheater hot side inlet state calculation ###
path = filedialog.askdirectory(initialdir="/c:/Users/jcurry/OneDrive - Janicki Industries/Automations/GitHubRepository/Preheater_Analysis/DataSets")
for filename in os.listdir(path):
    f = os.path.join(path, filename)
    if os.path.isfile(f):
        data = pd.read_csv(f)
        Test = 0
        A = 306.58
        data['Date and Time'] = pd.to_datetime(data['Time'])
        hotsidetempinlet_K = f_to_k(data['Hot Side Inlet Temp [F]'])
        hotsidetempoutlet_K = f_to_k(data['Hot Side Outlet Temp [F]'])
        if Test:
            preheater_hot_side_inlet_density = np.empty(len(data['Hot Side Inlet Temp [F]']))
            preheater_hot_side_inlet_enthalpy = np.empty(len(data['Hot Side Inlet Temp [F]']))
            preheater_hot_side_outlet_enthalpy = np.empty(len(data['Hot Side Outlet Temp [F]']))
            preheater_hot_side_inlet_enthalpy_approx = np.empty(len(data['Hot Side Outlet Temp [F]']))
            i = 0
            for row in hotsidetempinlet_K:
                temp_value = pt.IAPWS95(P=0.18, T=row)
                preheater_hot_side_inlet_density[i] = temp_value.rho
                preheater_hot_side_inlet_enthalpy[i] = temp_value.h
                i = i + 1
                max_HS_temp_K = max(hotsidetempinlet_K)
                min_HS_temp_K = min(hotsidetempinlet_K)
                [m, b] = point_slope_form(max_HS_temp_K, pt.IAPWS95(P=0.18, T=max_HS_temp_K).h, min_HS_temp_K, pt.IAPWS95(P=0.18, T=min_HS_temp_K).h)
                preheater_hot_side_inlet_enthalpy_approx = m * hotsidetempinlet_K + b
                [m, b] = point_slope_form(max_HS_temp_K, pt.IAPWS95(P=0.18, T=max_HS_temp_K).rho, min_HS_temp_K, pt.IAPWS95(P=0.18, T=min_HS_temp_K).rho)
                preheater_hot_side_inlet_density_approx = m * hotsidetempinlet_K + b
                print("Difference between estimate for hot side inlet density and actual value =", max(abs(preheater_hot_side_inlet_density-preheater_hot_side_inlet_density_approx)))
                print("Difference between estimate for hot side inlet enthalpy and actual value =", max(abs(preheater_hot_side_inlet_enthalpy - preheater_hot_side_inlet_enthalpy_approx)))
            i = 0
            for row in hotsidetempoutlet_K:
                temp_value = pt.iapws95.IAPWS95(P=0.18, T=row)
                preheater_hot_side_outlet_enthalpy[i] = temp_value.h
                i = i+1
            max_HS_outlet_temp_K = max(hotsidetempoutlet_K)
            min_HS_outlet_temp_K = min(hotsidetempoutlet_K)
            [m1, b1] = point_slope_form(min_HS_outlet_temp_K, pt.IAPWS95(P=0.18, T=min_HS_outlet_temp_K).h, max_HS_outlet_temp_K, pt.IAPWS95(P=0.18, T=max_HS_outlet_temp_K).h)
            preheater_hot_side_outlet_enthalpy_approx = m1 * hotsidetempoutlet_K + b1
            print("Difference between estimate for hot side outlet enthalpy and actual value =", max(abs((preheater_hot_side_outlet_enthalpy - preheater_hot_side_outlet_enthalpy_approx))))
        else:
            max_HS_temp_K = max(hotsidetempinlet_K)
            min_HS_temp_K = min(hotsidetempinlet_K)
            [m, b] = point_slope_form(max_HS_temp_K, pt.IAPWS95(P=0.18, T=max_HS_temp_K).h, min_HS_temp_K, pt.IAPWS95(P=0.18, T=min_HS_temp_K).h)
            preheater_hot_side_inlet_enthalpy = m * hotsidetempinlet_K + b
            [m, b] = point_slope_form(max_HS_temp_K, pt.IAPWS95(P=0.18, T=max_HS_temp_K).rho, min_HS_temp_K, pt.IAPWS95(P=0.18, T=min_HS_temp_K).rho)
            preheater_hot_side_inlet_density = m*hotsidetempinlet_K+b
            max_HS_outlet_temp_K = max(hotsidetempoutlet_K)
            min_HS_outlet_temp_K = min(hotsidetempoutlet_K)
            [m1, b1] = point_slope_form(min_HS_outlet_temp_K, pt.IAPWS95(P=0.18, T=min_HS_outlet_temp_K).h, max_HS_outlet_temp_K, pt.IAPWS95(P=0.18, T=max_HS_outlet_temp_K).h)
            preheater_hot_side_outlet_enthalpy = m1 * hotsidetempoutlet_K + b1

        data['Hot Side Volume Flow [m^3/s]'] = gpm_to_m3per_sec(data['Infeed Flow [gpm]'])
        data['Hot Side Inlet Density [kg/m^3]'] = preheater_hot_side_inlet_density
        data['Hot Side Mass Flow [kg/s]'] = data['Hot Side Volume Flow [m^3/s]']*data['Hot Side Inlet Density [kg/m^3]']
        data['Hot Side Inlet Enthalpy [kj/kg]'] = preheater_hot_side_inlet_enthalpy
        data['Hot Side Outlet Enthalpy [kj/kg]'] = preheater_hot_side_outlet_enthalpy
        data['Hot Side Outlet Enthalpy Change [kj/kg]'] = data['Hot Side Inlet Enthalpy [kj/kg]']-data['Hot Side Outlet Enthalpy [kj/kg]']
        data['Hot Side Duty Cycle [kW]'] = data['Hot Side Mass Flow [kg/s]']*data['Hot Side Outlet Enthalpy Change [kj/kg]']
        data['Delta T1 [K]'] = f_to_k(data['Hot Side Inlet Temp [F]'])-f_to_k(data['Cold Side Outlet Temp [F]'])
        data['Delta T2 [K]'] = f_to_k((data['Hot Side Outlet Temp [F]'])) - f_to_k((data['Cold Side Inlet Temp [F]']))
        data['Log mean delta T [K]'] = (data['Delta T2 [K]']-data['Delta T1 [K]'])/np.log(data['Delta T2 [K]']/data['Delta T1 [K]'])
        data['U [W/m^2-K]'] = kw_to_w(data['Hot Side Duty Cycle [kW]'])/(np.multiply(data['Log mean delta T [K]'], A))
        data['Average U'] = np.average(data['U [W/m^2-K]'])
        U = "{:.3f}".format(float(data['Average U'][1]))


    # export_data = int(input("If you want to export the data to the analysis file enter 1, if not enter 0"))
        export_data = 1
        start_time = pd.to_datetime(data['Time'].iloc[1])
        end_time = pd.to_datetime(data['Time'].iloc[-1])
    # test_time = pd.Timedelta([t2, t1], unit='hr')
    # print(test_time, type(test_time))
        if export_data == 1:
            dir = r"C:\Users\jcurry\OneDrive - Janicki Industries\Automations\GitHubRepository\Preheater_Analysis\PreheaterAnalysis.csv"
            units = 'W/m^2-K'
            file_exists = os.path.exists(dir)
            if file_exists == 0:
                data_new = pd.DataFrame({'Start Time': start_time, 'End Time': end_time, 'Heat Transfer Coefficient': U, 'Units': units}, index=[0])
                new = data_new
            else:
                new = pd.read_csv(dir, index_col=0)
                my_dict = {'Start Time': start_time, 'End Time': end_time, 'Heat Transfer Coefficient': U, 'Units': units}
                additional = pd.DataFrame(my_dict, index=[0])
                new = pd.concat([new, additional], ignore_index=True)
                new['Start Time'] = pd.to_datetime(new['Start Time'])
                new.sort_values(by=['Start Time', 'End Time'], inplace=True, ignore_index=True, ascending=True)
            new = new.drop_duplicates(subset=['Start Time', 'End Time'], ignore_index=True)
            new.to_csv(dir)

dataset = pd.read_csv('C:/Users/jcurry/OneDrive - Janicki Industries/Automations/GitHubRepository/Preheater_Analysis/PreheaterAnalysis.csv')
plt.plot(dataset['Start Time'], dataset['Heat Transfer Coefficient'], '*-r')
plt.title('Preheater Heat Transfer Coefficient vs. Time')
plt.xlabel('Start Time')
plt.ylabel('U [W/m^2-K]')
plt.show()


print('Script has finished')