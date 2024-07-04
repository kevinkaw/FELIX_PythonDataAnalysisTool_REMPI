import h5py
import numpy as np
import pandas as pd
'''
This section contains functions necessary to perform single peak and multipeak integration. 
'''

__all__ = ['depletion']

class depletion:

    def __init__(self, mass_complex = None, scan_width = None, wavenumber = None, column_withoutIR = None, column_withIR = None, data_withoutIR = None, data_withIR = None, target_mass = None):
        self.mass_complex = mass_complex
        self.scan_width = scan_width
        self.wavenumber = wavenumber
        self.column_withoutIR = column_withoutIR
        self.column_withIR = column_withIR
        self.data_withoutIR = data_withoutIR
        self.data_withIR = data_withIR
        self.mass = target_mass
    
        self.scan_width_range_indices = []
        self.actual_mass_peak = 0
        self.signal_withoutIR = 0
        self.signal_withIR = 0
        self.data_interval = 0
        self.depletion = 0
        self.depletion_ln = 0
        self.new_table = pd.DataFrame()
        self.depletion_spectra = pd.DataFrame()

        self.list_mass_isotope = []
        self.list_scanwidth_isotope = []
        
    def get_range_scan_width(self, mass_input):
        '''
        This function gets the range of the scan width
        '''
        scan_width_min = 0
        scan_width_max = 0
        mass_isotope = 0
        mass_isotope = mass_input
        scan_width_min = mass_isotope - self.scan_width
        scan_width_max = mass_isotope + self.scan_width
        self.scan_width_range_indices = np.where((self.mass >= scan_width_min)&(self.mass <=scan_width_max))[0]
        # x_mass is the calibrated x-range of the plot.
        # It was declared just after the Part2 heading.
        # print(mass_isotope, scan_width_min, scan_width_max)
        return self.scan_width_range_indices

    def get_actual_mass_peak(self, mass_input=None):
        '''
        This function determines the peak mass of the complex based on the expected mass
        '''
        # mass_input=self.mass_complex assigns the default value of user enters none
        if mass_input is None:
            mass_input = self.mass_complex
        # run function to get the scan width indices
        self.get_range_scan_width(mass_input)
        # initialize variables
        range_x = []
        range_y1 = []
        range_y1 = []
        peak1 = 0
        peak2 = 0
        # define the range of x values where the peak is
        range_x = self.mass[self.scan_width_range_indices]
        # define the range of y values where the peak is
        range_y1 = self.data_withoutIR[self.scan_width_range_indices]
        # range_y2 = self.data_withIR[self.scan_width_range_indices]
        # take the index of range_y1 which has the highest value
        # apply this index to range_x to get the corresponding mass value for the peak
        peak1 = range_x[np.argmax(range_y1)]
        # peak2 = range_x[np.argmax(range_y2)]
        # get the mean value between both peaks and set that as the optimal peak
        # self.actual_mass_peak = np.mean([peak1,peak2])
        self.actual_mass_peak = peak1
        # shift the value of mass_complex to the maximum of the peak
        # then get an updated range for the scan width.
        # self.mass_complex = self.actual_mass_peak
        New_Mass = self.actual_mass_peak
        New_ScanWidth = self.get_range_scan_width(New_Mass)
        self.signal_withoutIR = self.data_withoutIR[New_ScanWidth]
        # self.signal_withIR = self.data_withIR[New_ScanWidth]
        # calculate the spacing between datapoints
        self.data_interval = np.mean(np.diff(range_x))
        return New_Mass,New_ScanWidth

    def get_depletion_single_peak(self):
        '''
        This function calculates the following from your scan width:
        1. sum
        2. depletion
        3. ln(depletion)

        '''
        #initialize variables
        signal_withoutIR = []
        signal_withIR = []
        signal_withoutIR = self.signal_withoutIR
        # signal_withIR = self.signal_withIR
        # sum
        signal_withoutIR =signal_withoutIR.sum()*self.data_interval
        # signal_withIR = signal_withIR.sum()*self.data_interval
        # double check the sum
        # for value in self.signal_withoutIR:
        #     print(f"{value}")
        # print(f"\n {signal_withoutIR}")
        # depletion
        self.depletion = signal_withIR/signal_withoutIR
        self.depletion_ln = -np.log(self.depletion)
        self.new_table = pd.DataFrame({
            "wavenumber": [self.wavenumber],
            "sum_withoutIR": [signal_withoutIR],
            # "sum_withIR":[signal_withIR],
            # "depletion": [self.depletion],
            # "-ln(depletion)":[self.depletion_ln]
        })

        return self.new_table

    def make_depletion_spectra_single_peak(self):
        '''
        creates a depletion spectra based on the `get_depletion_single_peak` method.
        '''
        self.get_depletion_single_peak()
        self.depletion_spectra = pd.concat([self.depletion_spectra, self.new_table], axis=0)
        return self.depletion_spectra


    def get_depletion_multi_peak(self):
        '''
        This function does the following calculations:
        1. iterate through the list of mass peaks to get actual peaks and scan widths.
        2. sum up the data within the scan width for both without and with IR.
        3. result is multiplied by the average interval between x points to get a better integration.
        4. calculate depletion and -ln(depletion)
        5. output everything to a dataframe.
        '''

        # initialize local variables
        newlist_mass_isotope = []
        newlist_scanwidth_isotope = []
        
        # get the optimized peak locations & their respective indices along the x-axis
        for isotope in self.mass_complex:
            output1, output2 = self.get_actual_mass_peak(isotope)
            newlist_mass_isotope.append(output1)
            newlist_scanwidth_isotope.append(output2)

        # assign to global variable
        self.list_mass_isotope = newlist_mass_isotope
        self.list_scanwidth_isotope = newlist_scanwidth_isotope
        
        # initialize local variables
        signal_withoutIR = 0
        signal_withIR = 0

        # for all isotopes, sum all the y-data corresponding to the peak
        for index, mass_isotope in enumerate(newlist_mass_isotope):
            signal_withoutIR += (self.data_withoutIR[newlist_scanwidth_isotope[index]].sum())
            # signal_withIR += (self.data_withIR[newlist_scanwidth_isotope[index]].sum())
        
        # multiply by data interval between x-points to get a better integration / riemann sum.
        signal_withoutIR = signal_withoutIR #*self.data_interval        
        # signal_withIR = signal_withIR #*self.data_interval

        # calculate depletion and -ln(depletion)
        # self.depletion = signal_withIR / signal_withoutIR
        # self.depletion_ln = -np.log(self.depletion)

        # save everything to a dataframe.
        self.new_table = pd.DataFrame({
            "wavenumber": [self.wavenumber],
            "sum_withoutIR": [signal_withoutIR],
            # "sum_withIR":[signal_withIR],
            # "depletion": [self.depletion],
            # r"-ln(depletion)":[self.depletion_ln]
        })
        return self.new_table

    def make_depletion_spectra_multi_peak(self):
        '''
        creates a depletion spectra based on the `get_depletion_multiple_peak` method.
        '''
        self.get_depletion_multi_peak()
        self.depletion_spectra = pd.concat([self.depletion_spectra, self.new_table], axis=0)
        return self.depletion_spectra
