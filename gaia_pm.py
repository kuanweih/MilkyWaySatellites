import numpy as np
import pandas as pd

from src.tools import dist2
from wsdb import HOST, USER, PASSWORD
from src.classPatchMWSatellite import PatchMWSatellite




def savetxt_gaia_pm_nstar(dict_joint):
    pmra, pmdec, nrh, nbg = [], [], [], []
    pmra2rh, pmdec2rh, n2rh = [], [], []
    for i, name in enumerate(dict_joint['GalaxyName']):
        ra, dec = dict_joint['RA_deg'][i], dict_joint['Dec_deg'][i]
        dist = dict_joint['Distance_pc'][i]
        rh = dict_joint['rh(arcmins)'][i] / 60.
        width = 4. * rh
        database = 'gaia_dr2.gaia_source'
        cat_str = """ ra, dec, pmra, pmdec,
                      phot_g_mean_mag, astrometric_excess_noise """

        Patch = PatchMWSatellite(name, ra, dec, dist, width, database, cat_str)
        Patch.sql_get(HOST, USER, PASSWORD)
        Patch.mask_cut("phot_g_mean_mag", 17, 21)
        Patch.mask_g_mag_astro_noise_cut()

        mask2rh = dist2(Patch.datas['ra'], Patch.datas['dec'], ra, dec) <= (2.*rh)**2
        Patch.cut_datas(mask2rh)
        _n2rh = len(Patch.datas['pmra'])
        _pmra = np.nanmean(Patch.datas['pmra'])
        _pmdec = np.nanmean(Patch.datas['pmdec'])
        n2rh.append(_n2rh)
        pmra2rh.append(_pmra)
        pmdec2rh.append(_pmdec)

        maskrh = dist2(Patch.datas['ra'], Patch.datas['dec'], ra, dec) <= rh**2
        Patch.cut_datas(maskrh)
        _nrh = len(Patch.datas['pmra'])
        _pmra = np.nanmean(Patch.datas['pmra'])
        _pmdec = np.nanmean(Patch.datas['pmdec'])

        nrh.append(_nrh)
        pmra.append(_pmra)
        pmdec.append(_pmdec)

        _den = (_n2rh - _nrh) / np.pi / 3. / rh**2
        nbg.append(_den)    # Nbg / deg^2

    dict_joint['Nstar_rh'] = np.array(nrh)
    dict_joint['pmra_rh'] = np.array(pmra)
    dict_joint['pmdec_rh'] = np.array(pmdec)
    dict_joint['Nstar_2rh'] = np.array(n2rh)
    dict_joint['pmra_2rh'] = np.array(pmra2rh)
    dict_joint['pmdec_2rh'] = np.array(pmdec2rh)

    df = pd.DataFrame(dict_joint)
    df.to_csv('dwarf-csvs/dwarfs_pms.csv')



    dict_joint['Nbg_per_deg2'] = np.array(nbg)
    dict_joint['rh_deg'] = dict_joint['rh(arcmins)'] / 60.
    dict_joint['Nstar_per_rhdeg3'] = dict_joint['Nstar_rh'] / dict_joint['rh_deg']**3

    df = pd.DataFrame(dict_joint)
    df.to_csv('dwarf-csvs/dwarfs_detail.csv')



if __name__ == '__main__':

    print('Loading the original dwarf csv file...\n')
    dict_joint = pd.read_csv('ori-dwarfs/ori-dwarfs.csv')
    dict_joint = dict_joint.drop(columns=['Unnamed: 0'])

    savetxt_gaia_pm_nstar(dict_joint)
