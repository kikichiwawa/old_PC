import os

# スクリプトのあるディレクトリを取得
dir_path = os.path.dirname(os.path.realpath(__file__))

# カレントディレクトリを設定
os.chdir(dir_path)

from PIL import Image
import numpy as np
class Animation:
    """
    図形のデータ，カメラの位置を元に3Dアニメーションを作成する
    図形データ  ：面の座標を面ごとに指定
    カメラの位置：現時点では，原点に固定
    
    現在のゴール
    ・カラーのみに対応
    ・奥行による色の変化(影)無し

    現状
    ・スクリーン上で回転する面を描画
    """
    #背景の初期値(黒)
    BG = (0,0,0)

    @staticmethod
    def rotation_square(n):
        surf_list = []
        theta_list = [(a+n/60) * np.pi for a in [0,-1/2,-1,-3/2]]
        surface = [[300*np.cos(theta), 300*np.sin(theta)] for theta in theta_list]
        surf_list.append(surface)
        return surf_list

    def __init__(self, size, background=BG, get_surf_func=rotation_square):
        self.size = size
        self.background = background
        self.get_surf_func = get_surf_func
    
    def _mask(self, surface):
        """
        surfaceは凸平面の各店を時計回りに指定
        """
        x,y = np.indices(self.size)
        x -= self.size[0]//2
        y -= self.size[1]//2
        X = np.stack((x,y,np.ones(self.size)), axis=2)
        #ずっと使いまわすので，どこかに保管したほうが効率がよさそう?

        p_N = len(surface)
        k_list = np.zeros((3, p_N))
        for i in range(p_N):
            #p1,p2の座標からax+by+c>0の形にする
            p1, p2 = surface[i], surface[(i+1)%p_N]
            a = p2[1] - p1[1]
            b = p1[0] - p2[0]
            c = p2[0] * p1[1] - p1[0] * p2[1]
            k = np.array([a,b,c])
            k_list[:,i] = k
        mask = (X@k_list>0).all(2)
        return mask
        
    def draw_image(self, surf_list):
        im = np.full(self.size + (3,), self.background, dtype=np.uint8)
        z_array = np.full(self.size, np.inf)
        for surface in surf_list:
            mask = self._mask(surface)
            z = np.fromfunction(lambda i, j:i+j, self.size, dtype=int)
            overwrite_mask = np.logical_and(mask, z_array>mask)
            z_array[overwrite_mask] = z[mask]
            im[overwrite_mask] = [255,255,255]
        return im

    def export(self, path, N, duration=100):
        images = np.zeros((N,)+self.size+(3,), dtype=np.uint8)
        for n in range(N):
            surf_list = self.get_surf_func(n)
            im = self.draw_image(surf_list)
            images[n] = im
            if(n%10==0):
                print(str(n) + " times end")
        PIL_images = [Image.fromarray(im) for im in images]
        PIL_images[0].save(path, save_all=True, append_images=PIL_images[1:], optimize=False, duration=duration, loop=0)
if __name__ == "__main__":
    def make_rotation_polygon(n):
        def rotate_polygon(time):
            surf_list = []
            A = [-2/n*a for a in range(n)]
            theta_list = [(a+time/60) * np.pi for a in A]
            surface = [[300*np.cos(theta), 300*np.sin(theta)] for theta in theta_list]
            surf_list.append(surface)
            return surf_list
        return rotate_polygon

    anime = Animation((1000,1000), get_surf_func=make_rotation_polygon(6))
    path = "./output/anime1.gif"
    anime.export(path, 300, 1000/60)