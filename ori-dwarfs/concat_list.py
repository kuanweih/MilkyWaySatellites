import numpy as np
import pandas as pd

from typing import Dict
# from src.tools import get_dic_list_npy, dist2
# from src.param_patch_candidate import PATCH_DIST, N_PATCH_MAX


def get_dic_list_npy(path: str, quantitys: str):
    """ Select a dict from a numpy array based on keys as quantitys
    : path : path of the dict npy file
    : quantitys : target keys
    : return : needed dict
    """
    dwarfs_dict = np.load(path).item()
    dict_need = {q: dwarfs_dict[q] for q in quantitys}
    return  dict_need



if __name__ == '__main__':
    print('--------------------------------------------------')
    print('Concatenating McConnachie list and the additional dwarfs:\n')

    path_mcconnachie = "McConnachie/dwarfs-McConnachie.npy"
    path_more = "more/dwarfs-more.npy"

    quantitys = ["GalaxyName", "RA_deg", "Dec_deg", "Distance_pc", "rh(arcmins)"]

    dict1 = get_dic_list_npy(path_mcconnachie, quantitys)
    dict2 = get_dic_list_npy(path_more, quantitys)

    dict_joint = {q: np.concatenate((dict1[q], dict2[q])) for q in quantitys}

    print('Saving txt files and npy files\n')
    np.save("dwarfs-joint", dict_joint)
    np.savetxt("dwarfs-names.txt", np.sort(dict_joint["GalaxyName"]), fmt="%s")

    print('Generating a csv file\n')
    df = pd.DataFrame(dict_joint).sort_values(by=['GalaxyName'])
    df.to_csv('ori-dwarfs.csv')

    print('Done concatenating the lists :)')
    print('--------------------------------------------------')
