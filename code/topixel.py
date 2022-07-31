import numpy as np
from collections import defaultdict

# 根据npc(number per channel)生成rgb列表
def set_rgb(npc):
    rgb=[]
    for i in range(npc+1):
        rgb.append(int(255*i/npc))
    return rgb

# 从rgb列表中选出与当前颜色最接近(基于绝对距离)的颜色
def get_similar(ori_color,rgb):
    sim_color=[0,0,0]
    for i in range(3):
        sim_color[i]=min(rgb,key=lambda x:abs(x-ori_color[i]))
    return sim_color

# 获取每一个像素块中出现次数最多的颜色
def get_color(img_part,rgb):
    counter = defaultdict(int)
    for y in img_part:
        for x in y:
            counter[tuple(x[:3])] += 1
    color = max(counter, key=counter.get)
    return get_similar(color,rgb)

# 将原图按照ratio进行分块
def partition(img, ratio,rgb):
    h,w=img.shape[0:2]
    pre = []
    size=[0,0]
    for y in range(0, img.shape[0], ratio):
        for x in range(0, img.shape[1], ratio):
            one =img[y:y+ratio, x:x+ratio]
            pre.append(get_color(one,rgb))
            size[1]+=1
        size[0]+=1
    size[1]=size[1]//size[0]
    return pre,size

# 生成像素图
def gen_image(box,size):
    img = np.zeros([size[0], size[1], 3], np.uint8)
    for i in range(size[0]):
        for j in range(size[1]):
            img[i,j,0]=box[i*size[1]+j][0]
            img[i,j,1]=box[i*size[1]+j][1]
            img[i,j,2]=box[i*size[1]+j][2]
    return img

# def main(path,ratio,rgb):
#     img =cv2.imread(path)
    
#     boxes,size=partition(img,ratio,rgb)
#     img=gen_image(boxes,size)
#     img=cv2.medianBlur(img,1)
#     cv2.imwrite("F:\\img10_6.png",img)
#     cv2.waitKey(0)


# if __name__ == "__main__":
#     path="F:\\0001.png"
#     ratio=10
#     npc=4
#     rgb=set_rgb(npc)
#     main(path,ratio,rgb)
