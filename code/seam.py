import cv2
import numpy as np

# 计算得出能量图
def energy_map(Image):
    b, g, r = cv2.split(Image)
    b_energy = np.absolute(cv2.Sobel(b, -1, 1, 0)) + np.absolute(cv2.Sobel(b, -1, 0, 1))
    g_energy = np.absolute(cv2.Sobel(g, -1, 1, 0)) + np.absolute(cv2.Sobel(g, -1, 0, 1))
    r_energy = np.absolute(cv2.Sobel(r, -1, 1, 0)) + np.absolute(cv2.Sobel(r, -1, 0, 1))
    return b_energy + g_energy + r_energy

# 动态规划找到水平方向最小能量的接缝
def find_seam_w(energy):
    h, w = energy.shape
    seam = np.zeros(energy.shape)
    for i in range(1, h):
        for j in range(0, w):
            if j == 0:
                min_index = np.argmin(energy[i - 1, j:j + 1]) + j
                energy[i, j] += int(energy[i - 1, min_index])
                seam[i, j] = min_index
            else:
                min_index = np.argmin(energy[i - 1, j - 1:j + 1]) + j - 1
                energy[i, j] += int(energy[i - 1, min_index])
                seam[i, j] = min_index            
    return energy, seam

# 删除水平方向的接缝
def delete_seam_w(Image, seam, Energy):
    h, w = Image.shape[0:2]
    output = np.zeros((h, w - 1, 3))
    j = np.argmin(Energy[-1])
    for i in range(h - 1, 0, -1):
        for k in range(3):
            output[i, :, k] = np.delete(Image[i, :, k], [j])  
            j = int(seam[i][j])
    return output

# 动态规划找到垂直方向最小能量的接缝 
def find_seam_h(energy):
    h, w = energy.shape
    seam = np.zeros(energy.shape)   
    for j in range(1, w):
        for i in range(0, h):
            if i ==0:
                min_index=np.argmin(energy[i:i+1,j-1])+i
                energy[i, j] += int(energy[min_index, j-1])
                seam[i, j] = min_index
            else:
                min_index=np.argmin(energy[i-1:i+1,j-1])+i-1
                energy[i, j] += int(energy[min_index, j-1])
                seam[i, j] = min_index       
    return energy, seam

# 删除垂直方向的接缝
def delete_seam_h(Image, seam, Energy):
    h, w = Image.shape[0:2]
    output = np.zeros((h-1, w , 3))
    i = np.argmin(Energy[:,w-1])
    for j in range(w - 1, 0, -1):
        for k in range(3):
            output[:, j, k] = np.delete(Image[:, j, k], [i])  
            i = int(seam[i][j])
    return output

def seam_carving(Image, delta, dire):
    for t in range(delta):
        energy = energy_map(Image)
        if dire=='w':
            Energy, seam = find_seam_w(energy)
            Image = delete_seam_w(Image, seam, Energy)
        elif dire=='h':
            Energy, seam = find_seam_h(energy)
            Image = delete_seam_h(Image, seam, Energy)
    return Image


# if __name__ == '__main__':
#     path="D:\\ProgrammingWorking\\VScode_Python\\OpenCV_DIP\\Final task\\source\\"
#     image = cv2.imread(path+'SeamCarvingA.png')
#     output_image = seam_carving(image, 30,'w')
#     cv2.imwrite(path+'outw.png', output_image)

