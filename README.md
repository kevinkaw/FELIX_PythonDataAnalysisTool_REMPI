### Date: 2024 July 3 (Wednesday)
# FELIX_PythonDataAnalysisTool_REMPI
### Author: Kevin Anthony Kaw
python program that loads multiple h5 files and creates a REMPI spectrum

This program is a quickly modified code to make REMPI spectra. The original code is made for IRMPD spectroscopy where we have signals with and without IR irradiation.
It is a bit messy but here are the important variables for the user
1. `element` == the target molecule
2. `mass_element` == mass of target molecule in amu
3. `alpha` and `t_off` == your mass spectra calibration parameters
4. `check_wavenumber` == set the particular wavelength where you want to see the mass spectra
5. `baseline_reference` == mass point where you want consider the baseline
6. baseline - `interval` == width of the baseline in amu
7. `list_mass_isotope` == peaks you want to integrate over
8. `scan_width` == integration width in amu
8. `temp` folder == your data folder should have a folder named `temp`, this program will save all outputs there.


### old README for version 6

* This program is an improved and cleaned-up version of FELIX_H5_MultiFile5.ipynb.
* For debugging purposes, I recommend a code-editor that can simultaneously open the same file at once and present it side-by-side. 
    * This is because the functions are grouped together in one codeblock 
    * I am using VScode
* I have documented it quite extensively and hopefully it is as descriptive as possible. 
    * You should be able to follow everything if you sit on it for some hours (within a day) and have intermediate proficiency in python programming
* Quickly summarizing, the program does the following:

#### Part 1:
1. Load multiple HDF5 files.
2. Extracts wavenumber and signal data from all HDF5 files.
3. Organizes the signal data on a per wavenumber basis.
#### Part 2:
4. Generate and calibrate an x-axis for the signal data.
5. Perform baseline correction on individual plots and full range basis
6. Sum up the baseline corrected signal
#### Part 3:
7. generate a depletion spectra with single and multiple mass peaks, and at single or full set of wavenumbers
8. plot and export the data

<style>
/* Reduce spacing between sections */
h1, h2, h3, h4, h5, h6 {
    margin-bottom: 0.0em;
}

p {
    margin-top: 0.0em;
    margin-bottom: 0.0em;
}

ul, ol {
    margin-top: 0.0em;
    margin-bottom: 0.0em;
}
</style>