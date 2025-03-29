"""
Author: HECE - University of Liege, Pierre Archambeau, Christophe Dessers
Date: 2024

Copyright (c) 2024 University of Liege. All rights reserved.

This script and its content are protected by copyright law. Unauthorized
copying or distribution of this file, via any medium, is strictly prohibited.
"""

from . import constant as cst
# Constants representing the exchanges - Fortran

exchange_parameters_VHM_Umax   = 20 #Paramètre modèle VHM
exchange_parameters_VHM_Uevap  = 21 #Paramètre modèle VHM
exchange_parameters_VHM_au1    = 22 #Paramètre modèle VHM
exchange_parameters_VHM_au2    = 23 #Paramètre modèle VHM
exchange_parameters_VHM_au3    = 24 #Paramètre modèle VHM
exchange_parameters_VHM_aof1   = 25 #Paramètre modèle VHM
exchange_parameters_VHM_aof2   = 26 #Paramètre modèle VHM
exchange_parameters_VHM_aif1   = 27 #Paramètre modèle VHM
exchange_parameters_VHM_aif2   = 28 #Paramètre modèle VHM
exchange_parameters_VHM_kof    = 29 #Paramètre modèle VHM
exchange_parameters_VHM_kif    = 30 #Paramètre modèle VHM
exchange_parameters_VHM_kbf    = 31 #Paramètre modèle VHM
exchange_parameters_GR4_x1     = 32 #Paramètre modèle GR4
exchange_parameters_GR4_x2     = 33 #Paramètre modèle GR4
exchange_parameters_GR4_x3     = 34 #Paramètre modèle GR4
exchange_parameters_GR4_x4     = 35 #Paramètre modèle GR4
exchange_parameters_VHM_UH_kif = 36 #Paramètre modèle VHM_UH
exchange_parameters_VHM_UH_kbf = 37 #Paramètre modèle VHM_UH
exchange_parameters_Froude_min_riv     = 101 #Paramètre modèle VHM_UH méthode de Froude
exchange_parameters_Froude_max_riv     = 102 #Paramètre modèle VHM_UH méthode de Froude
exchange_parameters_Froude_min_bas     = 103 #Paramètre modèle VHM_UH méthode de Froude
exchange_parameters_Froude_max_bas     = 104 #Paramètre modèle VHM_UH méthode de Froude
exchange_parameters_Froude_discharge   = 105 #Paramètre modèle VHM_UH méthode de Froude
exchange_parameters_Nash_pt            = 106 #Paramètre modèle VHM_UH méthode de Nash (peak time)
exchange_parameters_Nash_nb            = 107 #Paramètre modèle VHM_UH méthode de Nash (nb reservoirs)
exchange_parameters_AsymTri_totTime    = 108 #Paramètre modèle VHM_UH méthode de HU triangulaire asymétrique (temps total)
exchange_parameters_AsymTri_pt         = 109 #Paramètre modèle VHM_UH méthode de HU triangulaire asymétrique (peak time)

exchange_parameters_Dist_RS_Hs         = 110 #Paramètre modèle distribué Réservoir de stockage
exchange_parameters_Dist_RS_TS         = 111 #Paramètre modèle distribué Réservoir de stockage
exchange_parameters_Dist_Soil_Umax     = 112 #Paramètre modèle distribué Soil
exchange_parameters_Dist_Soil_TSPAN    = 113 #Paramètre modèle distribué Soil
exchange_parameters_Dist_Horton_F0     = 114 #Paramètre modèle distribué Horton
exchange_parameters_Dist_Horton_FC     = 115 #Paramètre modèle distribué Horton
exchange_parameters_Dist_Horton_K      = 116 #Paramètre modèle distribué Horton
exchange_parameters_Dist_kif           = 117 #Paramètre modèle distribué pour réservoir linéaire couche épidermique (if)
exchange_parameters_Dist_qlif          = 118 #Paramètre modèle distribué pour réservoir linéaire couche épidermique (if)


# Constants representing the exchanges - Python
exchange_parameters_py_timeDelay    = -11


# %% All model dictionnaries
VHM = {}
VHM["Nb"] = 12
VHM["Parameters"] = {}
VHM["Parameters"][exchange_parameters_VHM_aif1] = {}
VHM["Parameters"][exchange_parameters_VHM_aif1]["Name"] = "Coeff aif1"
VHM["Parameters"][exchange_parameters_VHM_aif1]["File"] = "simul_soil.param"
VHM["Parameters"][exchange_parameters_VHM_aif1]["Group"] = "Flow fraction parameters"
VHM["Parameters"][exchange_parameters_VHM_aif1]["Key"] = "Coeff aif1"
VHM["Parameters"][exchange_parameters_VHM_aif1]["Unit"] = "[-]"
VHM["Parameters"][exchange_parameters_VHM_aif2] = {}
VHM["Parameters"][exchange_parameters_VHM_aif2]["Name"] = "Coeff aif2"
VHM["Parameters"][exchange_parameters_VHM_aif2]["File"] = "simul_soil.param"
VHM["Parameters"][exchange_parameters_VHM_aif2]["Group"] = "Flow fraction parameters"
VHM["Parameters"][exchange_parameters_VHM_aif2]["Key"] = "Coeff aif2"
VHM["Parameters"][exchange_parameters_VHM_aif2]["Unit"] = "[-]"
VHM["Parameters"][exchange_parameters_VHM_aof1] = {}
VHM["Parameters"][exchange_parameters_VHM_aof1]["Name"] = "Coeff aof1"
VHM["Parameters"][exchange_parameters_VHM_aof1]["File"] = "simul_soil.param"
VHM["Parameters"][exchange_parameters_VHM_aof1]["Group"] = "Flow fraction parameters"
VHM["Parameters"][exchange_parameters_VHM_aof1]["Key"] = "Coeff aof1"
VHM["Parameters"][exchange_parameters_VHM_aof1]["Unit"] = "[-]"
VHM["Parameters"][exchange_parameters_VHM_aof2] = {}
VHM["Parameters"][exchange_parameters_VHM_aof2]["Name"] = "Coeff aof2"
VHM["Parameters"][exchange_parameters_VHM_aof2]["File"] = "simul_soil.param"
VHM["Parameters"][exchange_parameters_VHM_aof2]["Group"] = "Flow fraction parameters"
VHM["Parameters"][exchange_parameters_VHM_aof2]["Key"] = "Coeff aof2"
VHM["Parameters"][exchange_parameters_VHM_aof2]["Unit"] = "[-]"
VHM["Parameters"][exchange_parameters_VHM_au1] = {}
VHM["Parameters"][exchange_parameters_VHM_au1]["Name"] = "Coeff au1"
VHM["Parameters"][exchange_parameters_VHM_au1]["File"] = "simul_soil.param" 
VHM["Parameters"][exchange_parameters_VHM_au1]["Group"] = "Flow fraction parameters"
VHM["Parameters"][exchange_parameters_VHM_au1]["Key"] = "Coeff au1"
VHM["Parameters"][exchange_parameters_VHM_au1]["Unit"] = "[-]"
VHM["Parameters"][exchange_parameters_VHM_au2] = {}
VHM["Parameters"][exchange_parameters_VHM_au2]["Name"] = "Coeff au2"
VHM["Parameters"][exchange_parameters_VHM_au2]["File"] = "simul_soil.param"
VHM["Parameters"][exchange_parameters_VHM_au2]["Group"] = "Flow fraction parameters"
VHM["Parameters"][exchange_parameters_VHM_au2]["Key"] = "Coeff au2"
VHM["Parameters"][exchange_parameters_VHM_au2]["Unit"] = "[-]"
VHM["Parameters"][exchange_parameters_VHM_au3] = {}
VHM["Parameters"][exchange_parameters_VHM_au3]["Name"] = "Coeff au3"
VHM["Parameters"][exchange_parameters_VHM_au3]["File"] = "simul_soil.param"
VHM["Parameters"][exchange_parameters_VHM_au3]["Group"] = "Flow fraction parameters"
VHM["Parameters"][exchange_parameters_VHM_au3]["Key"] = "Coeff au3"
VHM["Parameters"][exchange_parameters_VHM_au3]["Unit"] = "[-]"
VHM["Parameters"][exchange_parameters_VHM_Umax] = {}
VHM["Parameters"][exchange_parameters_VHM_Umax]["Name"] = "Umax"
VHM["Parameters"][exchange_parameters_VHM_Umax]["File"] = "simul_soil.param"
VHM["Parameters"][exchange_parameters_VHM_Umax]["Group"] = "Soil characteristics"
VHM["Parameters"][exchange_parameters_VHM_Umax]["Key"] = "Umax"
VHM["Parameters"][exchange_parameters_VHM_Umax]["Unit"] = "[mm]"
VHM["Parameters"][exchange_parameters_VHM_Uevap] = {}
VHM["Parameters"][exchange_parameters_VHM_Uevap]["Name"] = "Uevap"
VHM["Parameters"][exchange_parameters_VHM_Uevap]["File"] = "simul_soil.param"
VHM["Parameters"][exchange_parameters_VHM_Uevap]["Group"] = "Soil characteristics"
VHM["Parameters"][exchange_parameters_VHM_Uevap]["Key"] = "Uevap"
VHM["Parameters"][exchange_parameters_VHM_Uevap]["Unit"] = "[mm]"
VHM["Parameters"][exchange_parameters_VHM_kof] = {}
VHM["Parameters"][exchange_parameters_VHM_kof]["Name"] = "kof"
VHM["Parameters"][exchange_parameters_VHM_kof]["File"] = "simul_of.param"
VHM["Parameters"][exchange_parameters_VHM_kof]["Group"] = "Time Parameters"
VHM["Parameters"][exchange_parameters_VHM_kof]["Key"] = "Lagtime"
VHM["Parameters"][exchange_parameters_VHM_kof]["Unit"] = "[sec]"
VHM["Parameters"][exchange_parameters_VHM_kof]["Convertion Factor"] = 1/3600.0    # [sec] -> [h]
VHM["Parameters"][exchange_parameters_VHM_kif] = {}
VHM["Parameters"][exchange_parameters_VHM_kif]["Name"] = "kif"
VHM["Parameters"][exchange_parameters_VHM_kif]["File"] = "simul_if.param"
VHM["Parameters"][exchange_parameters_VHM_kif]["Group"] = "Time Parameters"
VHM["Parameters"][exchange_parameters_VHM_kif]["Key"] = "Lagtime"
VHM["Parameters"][exchange_parameters_VHM_kif]["Unit"] = "[sec]"
VHM["Parameters"][exchange_parameters_VHM_kif]["Convertion Factor"] = 1/3600.0    # [sec] -> [h]
VHM["Parameters"][exchange_parameters_VHM_kbf] = {}
VHM["Parameters"][exchange_parameters_VHM_kbf]["Name"] = "kbf"
VHM["Parameters"][exchange_parameters_VHM_kbf]["File"] = "simul_bf.param"
VHM["Parameters"][exchange_parameters_VHM_kbf]["Group"] = "Time Parameters"
VHM["Parameters"][exchange_parameters_VHM_kbf]["Key"] = "Lagtime"
VHM["Parameters"][exchange_parameters_VHM_kbf]["Unit"] = "[sec]"
VHM["Parameters"][exchange_parameters_VHM_kbf]["Convertion Factor"] = 1/3600.0    # [sec] -> [h]
GR4 = {}
GR4["Parameters"] = {}
GR4["Nb"] = 4
GR4["Parameters"][exchange_parameters_GR4_x1] = {}
GR4["Parameters"][exchange_parameters_GR4_x1]["Name"] = "X1"
GR4["Parameters"][exchange_parameters_GR4_x1]["File"] = "simul_GR4.param"
GR4["Parameters"][exchange_parameters_GR4_x1]["Group"] = "GR4 Parameters"
GR4["Parameters"][exchange_parameters_GR4_x1]["Key"] = "X1"
GR4["Parameters"][exchange_parameters_GR4_x1]["Unit"] = "[mm]"
GR4["Parameters"][exchange_parameters_GR4_x2] = {}
GR4["Parameters"][exchange_parameters_GR4_x2]["Name"] = "X2"
GR4["Parameters"][exchange_parameters_GR4_x2]["File"] = "simul_GR4.param"
GR4["Parameters"][exchange_parameters_GR4_x2]["Group"] = "GR4 Parameters"
GR4["Parameters"][exchange_parameters_GR4_x2]["Key"] = "X2"
GR4["Parameters"][exchange_parameters_GR4_x2]["Unit"] = "[mm]"
GR4["Parameters"][exchange_parameters_GR4_x3] = {}
GR4["Parameters"][exchange_parameters_GR4_x3]["Name"] = "X3"
GR4["Parameters"][exchange_parameters_GR4_x3]["File"] = "simul_GR4.param"
GR4["Parameters"][exchange_parameters_GR4_x3]["Group"] = "GR4 Parameters"
GR4["Parameters"][exchange_parameters_GR4_x3]["Key"] = "X3"
GR4["Parameters"][exchange_parameters_GR4_x3]["Unit"] = "[mm]"
GR4["Parameters"][exchange_parameters_GR4_x4] = {}
GR4["Parameters"][exchange_parameters_GR4_x4]["Name"] = "X4"
GR4["Parameters"][exchange_parameters_GR4_x4]["File"] = "simul_GR4.param"
GR4["Parameters"][exchange_parameters_GR4_x4]["Group"] = "GR4 Parameters"
GR4["Parameters"][exchange_parameters_GR4_x4]["Key"] = "X4"
GR4["Parameters"][exchange_parameters_GR4_x4]["Unit"] = "[hours]"
VHM_UH = {}
UH = {}
# distributed model with 2 layers : 1 dist UH & 1 lumped linear reservoir
UHDIST_LINBF = {}
UHDIST_LINBF["Nb"] = 13
UHDIST_LINBF["Parameters"] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_Umax] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_Umax]["Name"] = "Umax"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_Umax]["File"] = "simul_soil.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_Umax]["Group"] = "Distributed production model parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_Umax]["Key"] = "Umax"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_Umax]["Unit"] = "[mm]"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_TSPAN] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_TSPAN]["Name"] = "Time span soil"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_TSPAN]["File"] = "simul_soil.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_TSPAN]["Group"] = "Distributed production model parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_TSPAN]["Key"] = "Time span soil"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_TSPAN]["Unit"] = "[sec]"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Soil_TSPAN]["Convertion Factor"] = 1/3600.0    # [sec] -> [h]
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_F0] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_F0]["Name"] = "Horton F0"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_F0]["File"] = "simul_soil.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_F0]["Group"] = "Horton parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_F0]["Key"] = "F0"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_FC] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_FC]["Name"] = "Horton Fc"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_FC]["File"] = "simul_soil.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_FC]["Group"] = "Horton parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_FC]["Key"] = "Fc"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_K] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_K]["Name"] = "Horton k"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_K]["File"] = "simul_soil.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_K]["Group"] = "Horton parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_Horton_K]["Key"] = "k"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_Hs] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_Hs]["Name"] = "Storage reservoir Hs"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_Hs]["File"] = "simul_soil.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_Hs]["Group"] = "Storage reservoir parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_Hs]["Key"] = "hs"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_Hs]["Unit"] = "[mm]"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_TS] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_TS]["Name"] = "Storage reservoir Ts"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_TS]["File"] = "simul_soil.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_TS]["Group"] = "Storage reservoir parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_TS]["Key"] = "Ts"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_RS_TS]["Unit"] = "[h]"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_kif] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_kif]["Name"] = "kif"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_kif]["File"] = "simul_if.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_kif]["Group"] = "Time Parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_kif]["Key"] = "Lagtime"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_kif]["Unit"] = "[sec]"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_kif]["Convertion Factor"] = 1/3600.0    # [sec] -> [h]
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_qlif] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_qlif]["Name"] = "Qlif"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_qlif]["File"] = "simul_if.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_qlif]["Group"] = "Time Parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_qlif]["Key"] = "Specific flow rate"
UHDIST_LINBF["Parameters"][exchange_parameters_Dist_qlif]["Unit"] = "[m^2/s]"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_riv] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_riv]["Name"] = "Froude min (river)"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_riv]["File"] = "..\\Characteristic_maps\\Drainage_basin.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_riv]["Group"] = "Froude parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_riv]["Key"] = "Froude min (river)"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_riv] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_riv]["Name"] = "Froude max (river)"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_riv]["File"] = "..\\Characteristic_maps\\Drainage_basin.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_riv]["Group"] = "Froude parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_riv]["Key"] = "Froude max (river)"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_bas] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_bas]["Name"] = "Froude min (basin)"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_bas]["File"] = "..\\Characteristic_maps\\Drainage_basin.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_bas]["Group"] = "Froude parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_min_bas]["Key"] = "Froude min (basin)"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_bas] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_bas]["Name"] = "Froude max (basin)"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_bas]["File"] = "..\\Characteristic_maps\\Drainage_basin.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_bas]["Group"] = "Froude parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_max_bas]["Key"] = "Froude max (basin)"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_discharge] = {}
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_discharge]["Name"] = "Froude discharge"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_discharge]["File"] = "..\\Characteristic_maps\\Drainage_basin.param"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_discharge]["Group"] = "Froude parameters"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_discharge]["Key"] = "Discharge"
UHDIST_LINBF["Parameters"][exchange_parameters_Froude_discharge]["Unit"] = "[m^3/s]"




# General model dictionnary 
modelParamsDict = {}
modelParamsDict[cst.tom_VHM] = VHM
modelParamsDict[cst.tom_GR4] = GR4
modelParamsDict[cst.tom_UH] = UH
modelParamsDict[cst.tom_2layers_linIF]= UHDIST_LINBF


# %% Python-Fortran exchange constants

ptr_params = 1
ptr_opti_factors = 2
ptr_q_all = 3
ptr_time_delays = 4

fptr_update = 1
fptr_get_cvg = 2