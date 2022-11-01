import numpy as np
import cv2
import matplotlib.colors as colors

class MColorMap:
    N = 256
    def __init__(self) -> None:
        self._colormap_idx = 0
        self.setup()
        self.cmap = self.colormap
    
    def applyColorMap(self, img: np.array) -> np.array:
        cmap = self.cmap
        r = cv2.applyColorMap(img, cmap[:,0])
        g = cv2.applyColorMap(img, cmap[:,1])
        b = cv2.applyColorMap(img, cmap[:,2])
        return np.stack([r,g,b], axis=-1)

    def _list2map(self, colorlist: list) -> np.array:
        cmap = colors.LinearSegmentedColormap.from_list('CBFcmap', colorlist, N=self.N)
        color_list = [[cmap(i)[0],cmap(i)[1],cmap(i)[2] ]for i in range(self.N)]
        cmp = np.array(color_list)*255
        return cmp.astype(np.uint8)

    @property
    def colormap(self) -> np.array:
        colorlist = self.colorlists[self.idx]
        return self._list2map(colorlist)

    @property
    def idx(self) -> int:
        return self._colormap_idx

    @idx.setter
    def idx(self, i: int) -> None:
        if i < 0 or i > len(self.colorlists) - 1:
            raise ValueError('ColorMap: index of colormap out of reasonable range!')
        self._colormap_idx = i
        self.cmap = self.colormap

    def setup(self) -> None:
        self.colorlists = [
            ['black','#0D8BF3','#34F065','#F6E43C','#EE1A26'],
            ['black','#0D0003','#34F005','#F6E43C','#EE1A26'],
            ['black','#0D8BF3','#34F065','#F6E43C','#EE1A26'],

        ]







