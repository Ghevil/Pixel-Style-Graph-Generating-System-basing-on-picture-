# 文件说明
  **code**文件夹中为本系统的源码  
  
  **report**文件夹中为项目报告  
  
  **example**文件夹中为一些原图，以及经过处理后的输出图片

# 运行环境：
  python3.8.10

# Requirement：
  numpy
  
  
  tkinter
  
  
  opencv-python
  
  
  TensorFlow==2.9.1

# VGG19模型获取：
  https://www.vlfeat.org/matconvnet/pretrained/#downloading-the-pre-trained-models  
  
  imagenet-vgg-verydeep-19.mat  
  
  下载完模型后需要放入   **code**   文件夹并在**neural_style.py**文件中设置  **NETWORK**  为模型的绝对路径


# 系统运行：
  将仓库下载到本地  
  
  进入 **code**  文件夹，打开命令行，输入指令  **python SystemUI.py** 便可以打开前端界面  
  
  在设置好图片所在文件夹路径后便可以选择对应功能生成图片
