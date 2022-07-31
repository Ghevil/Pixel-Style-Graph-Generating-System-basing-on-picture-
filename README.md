#基于图片的像素画生成系统
系统致力于生成现实中的图片的像素画（将像素颗粒以肉眼可见的明显大小呈现在画布上，结合成一幅完整的图画）素材，从而作为艺术资源可以在日后使用——游戏布景等。

运行环境：python3.8.10

Requirement：
  numpy
  tkinter
  opencv-python
  TensorFlow==2.9.1

VGG19模型获取：
  https://www.vlfeat.org/matconvnet/pretrained/#downloading-the-pre-trained-models    imagenet-vgg-verydeep-19.mat
  下载完模型后需要放入   code   文件夹并在neural_style.py文件中设置  NETWORK  为模型的绝对路径


系统运行：
  进入  code  文件夹，打开命令行，输入指令  python SystemUI.py 便可以打开前端界面
  在设置好图片所在文件夹路径后便可以选择对应功能生成图片
