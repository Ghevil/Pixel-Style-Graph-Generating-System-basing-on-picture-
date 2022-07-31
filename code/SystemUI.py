import tkinter.messagebox as tm
from tkinter import*
from tkinter import ttk  
import seam
import topixel
import neural_style
import cv2

global file_path

ITERATION=1000


def showhelp():
    tm.showinfo("功能说明",
    "本系统用于生成像素风格的图片") 

def controlButton():
    but0.grid(row=0,pady=10)
    but1.grid(row=3,pady=10)
    but2.grid(row=1,pady=10)
    but3.grid(row=2,pady=10)

def hideCB():
    global but0,but1,but2,but3
    but0.grid_forget() 
    but1.grid_forget()
    but2.grid_forget()
    but3.grid_forget()

def backmain1():
    global File,setfile,backm,but0,but1,but2,but3
    File.grid_forget()
    setfile.grid_forget()
    backm.grid_forget()
    controlButton()

def set_():
    global file_path
    file_path=File.get()

def setpath():
    global win,File,setfile,backm
    hideCB()
    File=Entry(win,width=30)
    File.grid(row=1,column=0,pady=5)
    setfile=Button(win,text='设置', height=1,command=set_)
    setfile.grid(row=3,column=0,pady=10)
    backm=Button(win,text='返回',command=backmain1)
    backm.grid(row=3,column=3,pady=10)
    
def backmain2():
    intext.grid_forget()
    imagein.grid_forget()
    outtext.grid_forget()
    imageout.grid_forget()
    ratio_label.grid_forget()
    ratio_list.grid_forget()
    npc_label.grid_forget()
    npc_list.grid_forget()
    action1.grid_forget()
    backp.grid_forget()
    controlButton()

#图片转换成像素图功能
def g2pixel():
    global intext,imagein,outtext,imageout,ratio_label,ratio_list,npc_label,npc_list,action1,backp
    hideCB()
    intext=Label(win,text='输入图片名')
    imagein=Entry(win,width=20)
    intext.grid(row=1,column=0,pady=5)
    imagein.grid(row=1,column=1,pady=5)

    outtext=Label(win,text='输出图片名')
    imageout=Entry(win,width=20)
    outtext.grid(row=2,column=0,pady=5)
    imageout.grid(row=2,column=1,pady=5)

    value1=IntVar()
    value2=IntVar()
    ratio_label=Label(win,text='ratio')
    ratio_list=ttk.Combobox(win,width=8,textvariable=value1)
    ratio_list['values']=(2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
    ratio_label.grid(row=3,column=0,pady=5)
    ratio_list.grid(row=3,column=1,pady=5)
    
    npc_label=Label(win,text='npc')
    npc_list=ttk.Combobox(win,width=8,textvariable=value2)
    npc_list['values']=(5,6,7,8,9,10)
    npc_label.grid(row=4,column=0,pady=5)
    npc_list.grid(row=4,column=1,pady=5)

    action1=Button(win,text='生成图片',command=showimg1)
    action1.grid(row=5,column=0,pady=10)
    backp=Button(win,text='返回',command=backmain2)
    backp.grid(row=5,column=1,pady=10)

def showimg1():
    global label_img1, label_img2,img_in,img_out
    filein=file_path+'\\'+imagein.get()
    fileout=file_path+'\\'+imageout.get()
    ratio=int(ratio_list.get())
    depth=int(npc_list.get())
    rgb=topixel.set_rgb(depth)
    img =cv2.imread(filein)
    boxes,size=topixel.partition(img,ratio,rgb)
    _img=topixel.gen_image(boxes,size)
    _img=cv2.medianBlur(_img,1)
    cv2.imwrite(fileout,_img)

    if _img.shape[0]<540 or _img.shape[1]<960:
        d=(min(540//_img.shape[0],980//_img.shape[1]))
        _img_=cv2.resize(_img,(_img.shape[1]*d,_img.shape[0]*d))
    else:
        _img_=_img
    cv2.imshow('result',_img_)
    cv2.waitKey(0)

def backmain3():
    intext.grid_forget()
    imagein.grid_forget()
    outtext.grid_forget()
    imageout.grid_forget()
    w_label.grid_forget()
    w_list.grid_forget()
    h_label.grid_forget()
    h_list.grid_forget()
    action2.grid_forget()
    backq.grid_forget()
    controlButton()

#图片缩小功能
def gsc():
    global win,intext,imagein,outtext,imageout,h_label,h_list,w_label,w_list,action2,backq,h_value,w_value
    hideCB()
    
    intext=Label(win,text='输入图片名')
    imagein=Entry(win,width=20)
    intext.grid(row=1,column=0,pady=5)
    imagein.grid(row=1,column=1,pady=5,padx=2)

    outtext=Label(win,text='输出图片名')
    imageout=Entry(win,width=20)
    outtext.grid(row=2,column=0,pady=5)
    imageout.grid(row=2,column=1,pady=5,padx=2)

    def getw(v):
        global w_value
        w_value=v
        print(w_value)


    w_label=Label(win,text='宽(缩小比例 %)')
    w_list=Scale(win,label='',
             from_=0, to=100,
             orient=HORIZONTAL,   # 设置Scale控件平方向显示
             length=100,command=getw)  # 调用执行函数，是数值显示在 Label控件中
    w_label.grid(row=3,column=0,pady=5)
    w_list.grid(row=3,column=1,pady=5)
    
    def geth(v):
        global h_value
        h_value=v
        print(h_value)

    h_label=Label(win,text='高(缩小比例 %)')
    h_list=Scale(win,label='',
             from_=0, to=100,
             orient=HORIZONTAL,   # 设置Scale控件平方向显示
             length=100,command=geth)  # 调用执行函数，是数值显示在 Label控件中
    h_label.grid(row=4,column=0,pady=5)
    h_list.grid(row=4,column=1,pady=5)

    action2=Button(win,text='生成图片',command=showimg2)
    action2.grid(row=5,column=0,pady=10)
    backq=Button(win,text='返回',command=backmain3)
    backq.grid(row=5,column=1,pady=10)

def showimg2():
    filein=file_path+'\\'+imagein.get()
    fileout=file_path+'\\'+imageout.get()
    img =cv2.imread(filein)
    delta_w=int(w_list.get()/100.0*img.shape[1])
    delta_h=int(h_list.get()/100.0*img.shape[0])
    
    _img=seam.seam_carving(img,delta_w,'w')
    _img=seam.seam_carving(_img,delta_h,'h')    

    cv2.imwrite(fileout,_img)
    if _img.shape[0]<540 or _img.shape[1]<960:
        d=(min(540//_img.shape[0],980//_img.shape[1]))
        _img_=cv2.resize(_img,(_img.shape[1]*d,_img.shape[0]*d))
    else:
        _img_=_img
    
    cv2.imshow('result',_img_)
    cv2.waitKey(0)   


def backmain4():
    con_text.grid_forget()
    content_image.grid_forget()
    style_text.grid_forget()
    style_image.grid_forget()
    outtext.grid_forget()
    imageout.grid_forget()
    action3.grid_forget()
    backn.grid_forget()
    controlButton() 

#图片风格迁移功能
def style_transfer():
    global con_text,content_image,style_text,style_image,outtext,imageout,action3,backn
    hideCB()

    con_text=Label(win,text='内容图片名')
    content_image=Entry(win,width=20)
    con_text.grid(row=1,column=0,pady=5,padx=5)
    content_image.grid(row=1,column=1,pady=5,padx=5)

    style_text=Label(win,text='风格图片名')
    style_image=Entry(win,width=20)
    style_text.grid(row=2,column=0,pady=5,padx=5)
    style_image.grid(row=2,column=1,pady=5,padx=5)

    outtext=Label(win,text='输出图片名')
    imageout=Entry(win,width=20)
    outtext.grid(row=3,column=0,pady=5,padx=5)
    imageout.grid(row=3,column=1,pady=5,padx=5)
   

    action3=Button(win,text='生成图片',command=showimg3)
    action3.grid(row=4,column=0,pady=10)
    backn=Button(win,text='返回',command=backmain4)
    backn.grid(row=4,column=1,pady=10)

def showimg3():
    global label_img1, label_img1_, label_img2
    filein1=file_path+'\\'+content_image.get()
    filein2=file_path+'\\'+style_image.get() 
    fileout=file_path+'\\'+imageout.get()
    content_img =cv2.imread(filein1)
    style_img=cv2.imread(filein2)

    _img=neural_style.stylize(content_img,style_img,ITERATION)
    cv2.imwrite(fileout,_img)

    if _img.shape[0]<540 or _img.shape[1]<960:
        d=(min(540//_img.shape[0],980//_img.shape[1]))
        _img_=cv2.resize(_img,(_img.shape[1]*d,_img.shape[0]*d))
    else:
        _img_=_img
    cv2.imshow('result',_img_)
    cv2.waitKey(0)


def main():
    global win,but0,but1,but2,but3
    win=Tk()
    win.geometry('380x210')
    win.title("基于图片的像素画生成系统")
    #目录
    exp_me=Menu(win)
    help=Menu(exp_me)
    help.add_command(label='系统介绍',command=showhelp)
    exp_me.add_cascade(label="帮助",menu=help)
    win.config(menu=exp_me)

    but0=Button(win,text='设置文件路径',font=('Helvetica', 12),width=15,command=setpath)
    but1=Button(win,text='图片像素化',font=('Helvetica', 12),command=g2pixel)
    but2=Button(win,text='图片缩小',font=('Helvetica', 12),command=gsc)
    but3=Button(win,text='图片风格迁移',font=('Helvetica', 12),command=style_transfer)
    
    # k1=Label(imgs_play,text="7888")
    # k1.grid(row=0,column=0)
    controlButton()

    win.mainloop()

if __name__ == "__main__":
    main()


