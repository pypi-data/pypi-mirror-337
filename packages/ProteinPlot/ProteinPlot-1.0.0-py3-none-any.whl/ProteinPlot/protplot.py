"""
Created on Sat Mar 29 11:17:15 2025


----------------------------------------------------------------------------------------------------
THIS IS THE MAIN FILE FOR PROTPLOT PROJECT

The aim of this project is to create a universal way to deal with the '.pdb' extension
and to manage the protein files with pandas.
There are multiple functions regarding to the demonstration of the protein structure.


This file contains the functions given by the package. 
Be aware that this package was made for a University project in Hungary, PPKE ITK.

----------------------------------------------------------------------------------------------------


@authors: domedenes, viktoriaracz, maxilimianpoku
"""

#-------------------------------------DEPENDENCIES--------------------------------------------------

#Importing the dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import urllib.request as urllib2
import io


#-------------------------------------FUNCTIONS-----------------------------------------------------

#---------------------------------------------------------------------------------------------------
#Function - read_pdb()

def read_pdb(pdb_code, chain = None):
    """
    

    Parameters
    ----------
    pdb_code : TYPE str
        The pdb entry ID under which a protein is annoted in the databank rcsb.org
        
    chain : TYPE str, optional
        The given chain identifier which should be returned. Important in alignements. The default is None, when all of the chains are returned.

    Returns
    -------
    out : Pandas df
        An easily managable form of the given protein structure file.
        
    NOTE THAT INTERNET CONNECTION IS NEEDED!

    """
    

    response = urllib2.urlopen(f'https://files.rcsb.org/download/{pdb_code}.pdb') #defining the url where the pdb file is located
    read_response = response.read()
    workable = io.BytesIO(read_response).readlines()
    what = [workable[i].decode('utf-8') for  i in range(len(workable))]
    
    

    temporary_outcome = list()
    for i in range(len(what)):
        temp = what[i]
        temp = temp[0:4]
        
        if temp == 'ATOM':
            
            temporary_outcome.append(what[i]) # if it is an atom then we load it
            
    
    #defining a dictionary based on the character places in the string
    data = {'atom_index':[temporary_outcome[i][6:11].replace(' ', '') for i in range(len(temporary_outcome))],
            'atom_type':[temporary_outcome[i][12:16].replace(' ', '')  for i in range(len(temporary_outcome))],
            'amino_type':[temporary_outcome[i][17:20].replace(' ', '') for i in range(len(temporary_outcome))],
            'chain_index':[temporary_outcome[i][21].replace(' ', '') for i in range(len(temporary_outcome))],
            'amino_index':[temporary_outcome[i][22:26].replace(' ', '') for i in range(len(temporary_outcome))],
            'x':[temporary_outcome[i][31:38].replace(' ', '') for i in range(len(temporary_outcome))],
            'y':[temporary_outcome[i][39:46].replace(' ', '') for i in range(len(temporary_outcome))],
            'z':[temporary_outcome[i][47:54].replace(' ', '') for i in range(len(temporary_outcome))],
            'b_factor':[temporary_outcome[i][61:67].replace(' ', '') for i in range(len(temporary_outcome))]
            }
    
    
    #defining the dataframe
    out = pd.DataFrame(data)
    
    #adjusting the desired format
    numeric_columns = ['atom_index', 'amino_index', 'x', 'y', 'z', 'b_factor']
    out[numeric_columns] = out[numeric_columns].astype('float64')
        
    if chain:
        out = out[out.chain_index == chain]
    
    else:
        print(f'No chain was defined, note that all posibble chains in the entry {pdb_code} is returned')
        
    return out

#example = read_pdb('6vxx', chain = 'A')
#example2 = read_pdb('6vxx')

#---------------------------------------------------------------------------------------------------
#Function - plot_projection()

def plot_projection(protein_df, colorcode = 'default', atoms = 'all',
                    aminos = 'all', alpha = 1, marker = 'x', Title = None, figsave = None):
    
    plot_df = protein_df.copy() # no modification to be made
    
    if atoms != 'all':
        plot_df = plot_df[plot_df.atom_type.isin(atoms)] #filter for the given atoms
        
    if aminos != 'all':
        plot_df = plot_df[plot_df.amino_type.isin(aminos)] #filter for the given amino acids
        
    if colorcode == 'default':
        ccode = {'C' : 'black', 'N' : 'blue', 'O' : 'red', 'S' : 'yellow'} #dict for coloring
    
    #Defining the main type of the atoms for coloring
    defined_atoms = plot_df.atom_type.values
    defined_atoms = [element[0] for element in defined_atoms]
    plot_df['defined_atoms'] = defined_atoms
    datoms = np.unique(plot_df.defined_atoms)
    
    
    dpg = plot_df.groupby('defined_atoms')
    
    fig, axes = plt.subplots(nrows = 1, ncols = 3,figsize = (18,6)) #opening the figure
    for dat, plotter in dpg:
        
        axes[0].scatter(plotter.x.values[0], plotter.y.values[0], alpha = 1,
                        marker = marker, color = ccode[dat], label = dat) #just because the meaningful legend

        axes[0].scatter(plotter.x.values, plotter.y.values, alpha = alpha,
                        marker = marker, color = ccode[dat])
        axes[0].set_xlabel('X', fontsize = 14)
        axes[0].set_ylabel('Y', fontsize = 14)
        
        
        axes[1].scatter(plotter.x.values, plotter.z.values, alpha = alpha,
                        marker = marker, color = ccode[dat])
        axes[1].set_xlabel('X', fontsize = 14)
        axes[1].set_ylabel('Z', fontsize = 14)
        
        
        axes[2].scatter(plotter.z.values, plotter.y.values, alpha = alpha,
                        marker = marker, color = ccode[dat])
        axes[2].set_xlabel('Z', fontsize = 14)
        axes[2].set_ylabel('Y', fontsize = 14)
    
    
    
    fig.legend(fontsize = 16)
    
    if Title:
        fig.suptitle(Title, fontsize = 22)
    
    if figsave:
        plt.savefig(figsave, dpi = 200)
        
    plt.show()
        
        
        
        
    
#plot_projection(example2, alpha = 0.55,aminos = ['CYS'], atoms = ['CA', 'SG'], 
                #Title = 'Test projection plot', figsave = 'test.jpg')
    
    
    
    
    
    
        
    
