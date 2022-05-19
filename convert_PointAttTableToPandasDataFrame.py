# importing libraries
import arcpy,os
import numpy as np
import pandas as pd


def conv_att_to_pd(fc):
    """
    this method converts all the attribute table field data from feature class
    data to pandas dataframe disregarding shape attributes
    """
    fields = [[x.name for x in arcpy.ListFields(fc)][0]] + ["SHAPE@X","SHAPE@Y"] + [x.name for x in arcpy.ListFields(fc)][2:]
    df = pd.DataFrame(arcpy.da.TableToNumPyArray(fc,fields,null_value=-999999))
    return df