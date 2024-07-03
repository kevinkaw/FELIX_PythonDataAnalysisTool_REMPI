
import h5py
import numpy as np
import pandas as pd


'''
This section contains functions necessary to perform a baseline calibration.
'''
__all__ = ['mass_range', 'baseline']

def mass_range(n,m, mass_element, mass_messenger, x_mass):

    #initialize variables
    mass_complex = 0
    mass_range_indices = 0
    # n == size of iron cluster
    # m == number of argon atoms attached
    complex = f"Fe{n}-Ar{m}"
    mass_complex = mass_element*n + mass_messenger*m
    

    # define a minimum and maximum mass range, based on an interval
    interval = 20
    mass_range_min = mass_complex - interval
    mass_range_max = mass_complex + interval

    # get the range of values that are approximately on the same mass
    mass_range_indices = np.where((x_mass >= mass_range_min) & (x_mass <= mass_range_max))[0]

    return complex, mass_complex, mass_range_indices


class baseline:

    def __init__(self, baseline_reference = None, interval = None, wavenumber = None, column_withoutIR = None, column_withIR = None, data_withoutIR = None, data_withIR = None, target_mass = None):
        self.baseline_reference = baseline_reference
        # define a minimum and maximum mass range, based on the interval
        self.interval = interval
    
        self.wavenumber = wavenumber
        self.column_withoutIR = column_withoutIR
        self.column_withIR = column_withIR
        
        self.data_withoutIR = data_withoutIR
        self.data_withIR = data_withIR

        self.baseline_range_indices = 0
        self.mean_value_withoutIR = 0
        self.mean_value_withIR = 0
        self.baseline_corrected = {}
        self.compiled_data = {}
        self.compiled_data2 = {}

        self.mass = target_mass

    def baseline_range(self):
        self.wavenumber = self.wavenumber
        
        self.baseline_range_min = self.baseline_reference
        self.baseline_range_max = self.baseline_reference + self.interval
        # get the range of values corresponding to the baseline ranges
        self.baseline_range_indices = np.where((self.mass >= self.baseline_range_min) & (self.mass <= self.baseline_range_max))[0]
        return self.baseline_range_indices


    def baseline_mean(self):
        
        # self.baseline_range()
        self.mean_value_withoutIR = np.mean(self.data_withoutIR[self.baseline_range_indices])
        # self.mean_value_withIR = np.mean(self.data_withIR[self.baseline_range_indices])

        '''
        CAUTION! The y-axis values are still inverted!
        Remember to convert negative to positive values when plotting
        '''

        # check if the average makes sense 
        # print(type(self.data_withoutIR[self.baseline_range_indices]))
        # print(self.data_withoutIR[self.baseline_range_indices], self.mean_value_withoutIR)
        # print(f"mean:  {self.mean_value_withoutIR}")
        # for value in self.data_withoutIR[self.baseline_range_indices]:
        #     print(value)

        return self.mean_value_withoutIR, self.mean_value_withIR

    def baseline_correction(self):
        self.baseline_corrected = pd.DataFrame({
            # "baseline_corrected_"+self.column_withoutIR: abs(self.data_withoutIR)-abs(self.mean_value_withoutIR),
            # "baseline_corrected_"+self.column_withIR: abs(self.data_withIR)-abs(self.mean_value_withIR)
            "baseline_corrected_"+self.column_withoutIR: (-self.data_withoutIR +abs(self.mean_value_withoutIR)),
            # "baseline_corrected_"+self.column_withIR: (-self.data_withIR-abs(self.mean_value_withIR))
        })
        return self.baseline_corrected

    def baseline_compile(self):
        # check if key already exists in dictionary

        if self.wavenumber in self.compiled_data:
            
            self.compiled_data[self.wavenumber] = pd.concat([self.compiled_data[self.wavenumber], self.baseline_corrected], axis=1, ignore_index=False)
            return self.compiled_data[self.wavenumber]

            # I will disable this part because some wavenumbers are measured more than once per file
            # # if key exists but the last 2 columns are the same, overwrite the columns
            # if self.compiled_data[self.wavenumber].columns[-1] == self.baseline_corrected.columns[-1]:
            #     self.compiled_data[self.wavenumber] = pd.concat([self.compiled_data[self.wavenumber].iloc[:,:-2], self.baseline_corrected], axis=1, ignore_index=False)
            #     return self.compiled_data[self.wavenumber]
            # else:
            #     # if key exists, but the last 2 columns are NOT the same, append the column to the main data
            #     self.compiled_data[self.wavenumber] = pd.concat([self.compiled_data[self.wavenumber], self.baseline_corrected], axis=1, ignore_index=False)
            #     return self.compiled_data[self.wavenumber]
        
        else:
            # if key does not exist, make a new one
            self.compiled_data[self.wavenumber] = self.baseline_corrected
            return self.compiled_data[self.wavenumber]
        
    def baseline_sum(self):

        dataset = self.compiled_data[self.wavenumber]
        end_column_withoutIR = 0
        end_column_withIR = 0
        new_table = {}
        sum_withoutIR = {}
        sum_withIR = {}
        
        if any(dataset.columns.str.contains("sum")):
            print("Sums already exist, overwriting")
            end_column_withoutIR = -2
            # end_column_withIR = -1
        else:
            # print("else statement triggered",len(dataset.columns))
            end_column_withoutIR = len(dataset.columns)
            # end_column_withIR = len(dataset.columns)

        sum_withoutIR = dataset.iloc[:,0:end_column_withoutIR].sum(axis=1)
        # sum_withIR = dataset.iloc[:,1:end_column_withIR:2].sum(axis=1)
        

        new_table = pd.DataFrame({
            "sum_baseline_corrected_"+str(self.wavenumber)+"_withoutIR":sum_withoutIR,
            # "sum_baseline_corrected_"+str(self.wavenumber)+"_withIR":sum_withIR
        })
        self.compiled_data[self.wavenumber] = pd.concat([dataset.iloc[:,0:end_column_withoutIR], new_table],axis=1)
        return self.compiled_data[self.wavenumber]
    

    def baseline_sum_correction(self):
        
        new_table = {}
        
        signal_withoutIR = self.compiled_data[self.wavenumber].iloc[:,-1]
        # signal_withIR = self.compiled_data[self.wavenumber].iloc[:,-1]
        mean_value_withoutIR = np.mean(signal_withoutIR[self.baseline_range_indices])
        # mean_value_withIR = np.mean(signal_withIR[self.baseline_range_indices])
        corrected_signal_withoutIR = signal_withoutIR - abs(mean_value_withoutIR)
        # corrected_signal_withIR = signal_withIR - abs(mean_value_withIR)

        new_table = pd.DataFrame({
            "sum_baseline_corrected2_"+str(self.wavenumber)+"_withoutIR": corrected_signal_withoutIR,
            # "sum_baseline_corrected2_"+str(self.wavenumber)+"_withIR": corrected_signal_withIR
        })
        
        self.compiled_data2[self.wavenumber] = pd.concat([self.compiled_data[self.wavenumber], new_table], axis=1)
        return self.compiled_data2[self.wavenumber]
    