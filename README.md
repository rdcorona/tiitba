# TIITBA based-software

Tiitba it's a Python3 open-source graphical user interface (GUI), developed to vectorize, to analyze and to correct historical seismograms on smoked paper.  

The functions for basic corrections are codes developed by the authors based on the theory that describes the operation and characteristics of Wiechert mechanical instruments.  

Users can check the R.D. Corona-Fernandez [GitLab](https://gitlab.com/rdcorona/tiitba) or look up for the lastes version at zenodo repository.  

For more information contact the authors by email:  
 ***rdcorona@igeofisica.unam.mx / santoyo@igeofisica.unam.mx***  

The use of the GUI it's under user risk, please cite this code of terms of the related technical paper:  

- Corona- Fernández, R.D. & Santoyo, M.Á. **(2022)** Re- examination of the 1928 Parral, Mexico earthquake (M6.3) using a new multiplatform graphical vectorization and correction software for legacy seismic data. Geoscience Data Journal, 00, 1– 15. Available from: [https://doi.org/10.1002/gdj3.159](https://doi.org/10.1002/gdj3.159)  
And with this associated repository DOI:  

- **DOI: 10.5281/zenodo.6272823**

## Last modified September 2022, version 1.0.2  

### Note: This SOFTWARE may be used by any individual or corporation for any purpose except for re-selling or re-distributing the SOFTWARE  

TERMS FOR USE THIS GUI  

1) This SOFTWARE may be used by any individual or corporation for any purpose with the exception of re-selling or re-distributing the SOFTWARE.  

2) The AUTHORS must be acknowledged in any resulting publications or presentations  

3) We make no warranties to its accuracy or completeness for any use. The results mostly reside on the user's inputs images and time series.  

4) The use of the GUI it's under user risk.  

Tiitba is a new interactive portable multi-platform software developed to vectorize smoked paper seismograms from, but not limited to, Wiechert seismographs. It is completely coded in Python as an open-source Graphical User Interface (GUI).

This software aims for the preservation of historical seismograms, mainly those from the early 20th century recorded on smoked paper, and the use of the vectorized time-series for a modern seismological re-analysis.

## DOWNLOAD

Download all the files from the zenodo repository. DOI: 10.5281/zenodo.6272823  
Unpack the bin.tar and Pictures.tar files, the resulting folders should be placed in the same directory as the rest of the files.  

## INSTALATION

Tiitba is coded on Python3, we recommend Python by Anaconda for running the program.  

For Linux and MacOS operating systems run the bash **file install_??.sh**  
This file checks if Anaconda3 is installed and creates the tiitba virtual environment.  
This also creates a directory that contains the Python source code of Tiitba GUI on a given local directory and a desktop shortcut.  

If you have Anaconda3 installed, you just need to create the virtual environment.  

 `$ conda activate`

 `$ conda env create -f tiitba_env.yml`

If you do not have an Anaconda3 and you do not want to install it, the following libraries must be installed on your local python to execute Tiitba GUI: OpenCV V4.5.3, ObsPy, Pillow, numpy, and matplotlib.  

Every time you want to use Tiitba GUI, you have to activate the tiitba python environment  

 `$ conda activate tiitba`

You can add the Tiitba installation path on your bash to run the GUI from any directory. To start the GUI just type in a terminal tiitbaGUI.py in any directory.  

For Windows operating system, there is a beta version ***Setup Installer***.  

### Any failure, comment, and recommendation are very well received by the authors
