"""
Quantification of FAIR-ASL (CBF ml/100g/min)
Author: Benny Zhang
date: 2022-09
"""
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pydicom import dcmread
import SimpleITK as sitk
from scipy.optimize import curve_fit
from tqdm import tqdm

CWD = os.getcwd()
colorslist = ['black', '#0D8BF3', '#34F065', '#F6E43C', '#EE1A26', ]
CBF_cmap = colors.LinearSegmentedColormap.from_list('CBFcmap', colorslist, N=256)


def check_path(path_to_check: str) -> str:
    if not os.path.exists(path_to_check):
        os.mkdir(path_to_check)
    return path_to_check


def to_255(img: np.array) -> np.array:
    max = img.max()
    min = img.min()
    img_out = ((img-min)/(max-min)*255).astype(np.uint8)
    return img_out


def to_RGB(img: np.array) -> np.array:
    img = np.expand_dims(img, axis=2)
    img_out = np.concatenate([img,img,img], axis=2)
    return img_out

# Msel model
def Msel_abs(TI: float, T1app: float, M0: float) -> float:
    return np.abs(M0*(1-2*np.exp(-TI/T1app)))


def Msel(TI: float, T1app: float, M0: float) -> float:
    return M0*(1-2*np.exp(-TI/T1app))


def _fig_FAIR_Images(dss: tuple) -> Figure:
    dss_sel, dss_non = dss
    TI_num = len(dss_sel)
    fig, (axes_sel, axes_non, axes_diff) = plt.subplots(nrows=3, ncols=TI_num, figsize=(15,5), facecolor='black')
    fig.canvas.manager.set_window_title('FAIR Images')
    for ax, idx in zip(axes_sel, range(TI_num)):
        ds = dss_sel[idx]
        img = ds.pixel_array
        if idx == 0:
            ax.set_ylabel('Selective', color='w', fontsize=10)
        ax.set_title('{} ms'.format(dss_sel[idx].InversionTime), color='w', fontsize=10)
        im = ax.imshow(img, cmap='gray', vmin=500, vmax=20000)
        ax.tick_params(direction='in')
        for i in ['top', 'bottom', 'left', 'right']:
            ax.spines[i].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        if idx == TI_num-1:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cb = fig.colorbar(im, cax=cax)
            cb.ax.tick_params(color='w')
            cb.outline.set_visible(False)
            cb.update_ticks()
            labels = cb.ax.get_yticklabels()
            for label in labels:
                label.set_color('w')
                label.set_fontsize(7)
    for ax, idx in zip(axes_non, range(TI_num)):
        ds = dss_non[idx]
        img = ds.pixel_array
        if idx == 0:
            ax.set_ylabel('Non-Selective', color='w', fontsize=10)
        im = ax.imshow(img, cmap='gray', vmin=500, vmax=20000)
        ax.tick_params(direction='in')
        for i in ['top', 'bottom', 'left', 'right']:
            ax.spines[i].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        if idx == TI_num-1:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cb = fig.colorbar(im, cax=cax)
            cb.ax.tick_params(color='w')
            cb.outline.set_visible(False)
            cb.update_ticks()
            labels = cb.ax.get_yticklabels()
            for label in labels:
                label.set_color('w')
                label.set_fontsize(7)
    for ax, idx in zip(axes_diff, range(TI_num)):
        if idx == 0:
            ax.set_ylabel('Difference', color='w', fontsize=10)
        im = ax.imshow(dss_sel[idx].pixel_array - dss_non[idx].pixel_array, cmap='gray', vmin=-1000, vmax=1000)
        ax.tick_params(direction='in')
        for i in ['top', 'bottom', 'left', 'right']:
            ax.spines[i].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        if idx == TI_num-1:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cb = fig.colorbar(im, cax=cax)
            cb.ax.tick_params(color='w')
            cb.outline.set_visible(False)
            cb.update_ticks()
            labels = cb.ax.get_yticklabels()
            for label in labels:
                label.set_color('w')
                label.set_fontsize(7)
    fig.tight_layout(w_pad=0, h_pad=0.5)
    return fig


def _fig_Fitting(T1app_map: np.array, M0_map: np.array, cbf_map: np.array, xdata: np.array, img: tuple) -> Figure:
    img_sel, img_non = img
    index = [(22, 43), (35, 55), (40, 86), (18, 77)]
    fig, (axes_img, axes_cur) = plt.subplots(2, 4, figsize=(16,5), facecolor='black')
    fig.canvas.manager.set_window_title('Fitting')

    T1app_map[T1app_map>2000] = 2000
    T1app_map[T1app_map<1000] = 1000
    for ax_cur, ax_img, idx in zip(axes_cur, axes_img, index):
        x, y = idx
        T1app = T1app_map[x, y]
        M0 = M0_map[x, y]
        def Mnon(TI, f):
            T1b = 2800
            Ms = Msel(TI, T1app, M0)
            M_diff = 2*M0*f/0.9 * ((np.exp(-TI/T1app)- np.exp(-TI/T1b))/(1/T1b-1/T1app))
            return np.abs(Ms - M_diff)
        img = to_RGB(to_255(T1app_map))
        rgb = [255, 0, 255]
        img[x-1, y] = rgb
        img[x, y+1] = rgb
        img[x, y]   = rgb
        img[x, y-1] = rgb
        img[x+1, y] = rgb
        ax_img.imshow(img)
        ax_img.axis('off')
        ax_img.set_title('row:{} col:{} CBF:{:.2f}'.format(x+1, y+1, cbf_map[x, y]), color='w', fontsize=10)
        ax_cur.plot(np.arange(0,10000, 2), Msel_abs(np.arange(0, 10000, 2), T1app, M0), color='red', label='Sel', linewidth=1)
        ax_cur.plot(np.arange(0,10000, 2), Mnon(np.arange(0, 10000, 2), cbf_map[x, y]/60000/100), color='yellow', label='Non', linestyle='--', linewidth=1)
        ax_cur.plot(xdata, img_sel[x, y], '*', color='red', label='measured Sel')
        ax_cur.plot(xdata, img_non[x, y], '*', color='yellow', label='measured Non')
        ax_cur.legend(loc='lower right', fontsize=7, labelcolor='w', facecolor='black', frameon=False)

        ax_cur.tick_params('both', colors='w', labelsize=8)
        ax_cur.set_facecolor('black')
        for i in ['top', 'bottom', 'left', 'right']:
            ax_cur.spines[i].set_color('w')
    fig.tight_layout(w_pad=0)
    return fig


def _fig_Results(T1app_map: np.array, M0_map: np.array, cbf_map: np.array) -> Figure:
    fig, axes = plt.subplots(1, 3, figsize=(10,3), facecolor='black')
    fig.canvas.manager.set_window_title('Results')

    T1app_map_paras = {'X':T1app_map, 'cmap':'gray', 'vmin':1000, 'vmax':2000}
    M0_map_paras    = {'X':M0_map, 'cmap':'gray', 'vmin':5000, 'vmax':20000}
    cbf_map_paras   = {'X':cbf_map, 'cmap':CBF_cmap, 'vmin':0, 'vmax':400}

    paras_list = [T1app_map_paras, M0_map_paras, cbf_map_paras]
    title_list = ['T1 selective', 'M0', 'CBF']
    for ax, title, paras in zip(axes, title_list, paras_list):
        ax.set_title(title, color='w')
        im = ax.imshow(**paras)
        ax.axis('off')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = fig.colorbar(im, cax=cax)
        cb.ax.tick_params(color='w')
        cb.outline.set_visible(False)
        cb.update_ticks()
        labels = cb.ax.get_yticklabels()
        for label in labels:
            label.set_color('w')
            label.set_fontsize(8)

    fig.tight_layout()
    return fig


def read_dicom_FAIR(dcm_path: str) -> tuple:
    dcm_files = next(os.walk(dcm_path))[2]
    os.chdir(dcm_path)
    dss = []
    dcm_files.sort()
    for dcm_file in dcm_files:
        ds = dcmread(dcm_file)
        dss.append(ds)
    os.chdir(CWD)
    dss_sel = dss[0::2]
    dss_non = dss[1::2]
    return (dss_sel, dss_non)


def FAIR_CBF_Calc(dss: tuple) -> tuple:
    dss_sel, dss_non = dss

    # 提取image array 和 TIs
    img_sel = []
    img_non = []
    xdata = []
    for ds_sel, ds_non in zip(dss_sel, dss_non):
        xdata.append(ds_sel.InversionTime)
        img_sel.append(np.expand_dims(ds_sel.pixel_array, axis=2))
        img_non.append(np.expand_dims(ds_non.pixel_array, axis=2))
    img_sel = np.concatenate(img_sel, axis=2)
    img_non = np.concatenate(img_non, axis=2)
    xdata = np.array(xdata)

    # CBF
    x, y, _ = img_sel.shape
    cbf_map = np.zeros((x, y), dtype=np.float32)
    T1app_map = np.zeros((x, y), dtype=np.float32)
    M0_map = np.zeros((x, y), dtype=np.float32)
    for i in tqdm(range(x), desc='Fitting by Rows'):
        for j in range(y):
            ydata_sel = img_sel[i, j]
            ydata_non = img_non[i, j]
            popt_sel, pcov_sel = curve_fit(Msel_abs, xdata, ydata_sel, p0=(1500,10000))
            T1app, M0 = popt_sel
            M0_map[i, j] = M0
            if M0 < 3000:
                cbf_map[i, j] = 0
                T1app_map[i, j] = 0
                continue

            def Mnon(TI, f):
                T1b = 2800
                Ms = Msel(TI, T1app, M0)
                M_diff = 2*M0*f/0.9 * ((np.exp(-TI/T1app)- np.exp(-TI/T1b))/(1/T1b-1/T1app))
                return np.abs(Ms - M_diff)
            popt_non, pcov_non = curve_fit(Mnon, xdata, ydata_non, p0=(1/60000), bounds=(0, 2000/60000/100))
            cbf_map[i, j] = popt_non*60000*100
            T1app_map[i, j] = T1app

    return (img_sel, img_non), xdata, T1app_map, M0_map, cbf_map


def FAIR_Postprocessing(dcm_path: str, out_path: str) -> None:
    out_path = check_path(out_path)
    dss = read_dicom_FAIR(dcm_path)
    img, xdata, T1app_map, M0_map, cbf_map = FAIR_CBF_Calc(dss)
    Fig_FAIR_Images = _fig_FAIR_Images(dss)
    Fig_Fitting = _fig_Fitting(T1app_map.copy(), M0_map.copy(), cbf_map.copy(), xdata.copy(), img)
    Fig_Results = _fig_Results(T1app_map.copy(), M0_map.copy(), cbf_map.copy())

    Fig_FAIR_Images.savefig('{}/FAIR_Images.jpg'.format(out_path), dpi=300)
    Fig_Fitting.savefig('{}/Fitting.jpg'.format(out_path), dpi=300)
    Fig_Results.savefig('{}/Results.jpg'.format(out_path), dpi=300)

    image = sitk.GetImageFromArray(cbf_map)
    sitk.WriteImage(image, '{}/CBF.nii.gz'.format(out_path))


def read_dicom_FAIR_MS(dcm_path: str) -> tuple:
    '''Bruker 11.7T
        \n read Dicom images of Perfusion_FAIR 
    '''
    dcm_files = next(os.walk(dcm_path))[2]
    cwd = os.getcwd()
    os.chdir(dcm_path)
    dcm_files.sort()
    SliceLocation = []
    # check number of slices
    for dcm_file in dcm_files:
        ds = dcmread(dcm_file)
        if ds.SliceLocation not in SliceLocation:
            SliceLocation.append(ds.SliceLocation)
    # read dicom files
    slice_num = SliceLocation.__len__()
    dss_slices = []
    for slice in range(slice_num):
        dss = []
        dcm_files_perslice = dcm_files[slice::slice_num]
        for dcm_file in dcm_files_perslice:
            ds = dcmread(dcm_file)
            dss.append(ds)
            dss_sel = dss[0::2]
            dss_non = dss[1::2]
        dss_slices.append((dss_sel, dss_non))
    os.chdir(cwd)
    return dss_slices, slice_num


def FAIR_Postprocessing_MS(dcm_path: str, out_path: str) -> None:
    '''Multi-Slice version'''
    out_path = check_path(out_path)
    dss_slices, slice_num = read_dicom_FAIR_MS(dcm_path)
    for dss, idx in zip(dss_slices, range(slice_num)):
        print('Processing Slice {:>2}/{}'.format(idx+1, slice_num))
        img, xdata, T1app_map, M0_map, cbf_map = FAIR_CBF_Calc(dss)
        Fig_FAIR_Images = _fig_FAIR_Images(dss)
        Fig_Fitting = _fig_Fitting(T1app_map.copy(), M0_map.copy(), cbf_map.copy(), xdata.copy(), img)
        Fig_Results = _fig_Results(T1app_map.copy(), M0_map.copy(), cbf_map.copy())

        Fig_FAIR_Images.savefig('{}/{}_FAIR_Images.jpg'.format(out_path, idx+1), dpi=300)
        Fig_Fitting.savefig('{}/{}_Fitting.jpg'.format(out_path, idx+1), dpi=300)
        Fig_Results.savefig('{}/{}_Results.jpg'.format(out_path, idx+1), dpi=300)
        plt.close('all')


if __name__ == '__main__':
    dcm_path = r'E:\mridata\A30\20220923_173808_A3562_A30_CAD03\E5_Perfusion_FAIR_RARE\pdata\1\dicom'
    out_path = r'E:\mridata\CAD03'
    out_path = check_path(out_path)

    dss = read_dicom_FAIR(dcm_path)
    img, xdata, T1app_map, M0_map, cbf_map = FAIR_CBF_Calc(dss)
    Fig_FAIR_Images = _fig_FAIR_Images(dss)
    Fig_Fitting = _fig_Fitting(T1app_map.copy(), M0_map.copy(), cbf_map.copy(), xdata.copy(), img)
    Fig_Results = _fig_Results(T1app_map.copy(), M0_map.copy(), cbf_map.copy())

    Fig_FAIR_Images.savefig('{}/FAIR_Images.jpg'.format(out_path), dpi=300)
    Fig_Fitting.savefig('{}/Fitting.jpg'.format(out_path), dpi=300)
    Fig_Results.savefig('{}/Results.jpg'.format(out_path), dpi=300)

    image = sitk.GetImageFromArray(cbf_map)
    sitk.WriteImage(image, '{}/CBF.nii.gz'.format(out_path))
    plt.show(block=True)