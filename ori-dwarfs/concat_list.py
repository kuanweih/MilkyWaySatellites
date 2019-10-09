import numpy as np
import pandas as pd

from typing import Dict



def get_dic_list_npy(path: str, quantitys: str) -> Dict:
    """ Select a dict from a numpy array based on keys as quantitys
    : path : path of the dict npy file
    : quantitys : target keys
    : return : needed dict
    """
    dwarfs_dict = np.load(path).item()
    dict_need = {q: dwarfs_dict[q] for q in quantitys}
    return  dict_need

def deg_to_pc_w_dist(x_deg, x_dist_pc):
    return  x_deg * 2. * np.pi / 360. * x_dist_pc


if __name__ == '__main__':
    print('--------------------------------------------------')
    print('Concatenating McConnachie list and the additional dwarfs:\n')

    path_mcconnachie = "McConnachie/dwarfs-McConnachie.npy"
    path_more = "more/dwarfs-more.npy"

    quantitys = ["GalaxyName", "RA_deg", "Dec_deg", "Distance_pc", "rh(arcmins)"]

    dict1 = get_dic_list_npy(path_mcconnachie, quantitys)
    dict2 = get_dic_list_npy(path_more, quantitys)

    dict_joint = {q: np.concatenate((dict1[q], dict2[q])) for q in quantitys}

    dict_joint['rh_deg'] = dict_joint['rh(arcmins)'] / 60.
    dict_joint['rh_pc'] = deg_to_pc_w_dist(dict_joint['rh_deg'],
                                           dict_joint['Distance_pc'])

    print('Saving txt files and npy files\n')
    np.save("dwarfs-joint", dict_joint)
    np.savetxt("dwarfs-names.txt", np.sort(dict_joint["GalaxyName"]), fmt="%s")

    print('Generating a csv file\n')
    df = pd.DataFrame(dict_joint).sort_values(by=['GalaxyName'])
    df.to_csv('ori-dwarfs.csv')

    print('Done concatenating the lists :)')
    print('--------------------------------------------------')
