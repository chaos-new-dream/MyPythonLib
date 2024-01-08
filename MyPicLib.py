
import cv2
import os
import sys
from PIL import Image,ImageDraw,ImageFont
import shutil

def my_Videos2Images(video_path, save_path):
    """
    返回帧率
    """
    video_path = os.path.abspath(video_path)
    save_path = os.path.abspath(save_path)
    print(f"SRC路径{video_path}")
    print(f"DST路径{save_path}")
    # 1.检测读取文件路径是否正确
    if not os.path.exists(video_path):
        raise IOError('SRC不存在')
    if not os.path.exists(save_path):
        print("DST不存在,创建:" + save_path)
        os.mkdir(save_path)
    if not os.path.exists(save_path):
        raise IOError('DST还是不存在')

    cap = cv2.VideoCapture(video_path)
    flag = cap.isOpened()
    if not flag:
        cap.release()
        raise IOError("打开：" + video_path + "失败!")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    totalFrame=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = os.get_terminal_size().columns - 20
    for i in range(totalFrame):
        flag, frame = cap.read()
        if not flag:  # 如果已经读取到最后一帧则退出
            print("***这里不可能执行的***")
            break
        willSavePath=save_path + '/' +  str(i) + '.png'
        if os.path.exists(willSavePath):  # 在源视频不变的情况下，如果已经创建，则跳过
            cap.release()
            raise IOError("已经存在："+ willSavePath)
        if not cv2.imwrite(willSavePath, frame):
            cap.release()
            raise IOError("保存：" + willSavePath + "失败!")


        left = int(i*width/totalFrame)
        right = width-left
        print("\r进度:[", "▓" * left," "*right, f"]{i}/{totalFrame}", end="")

    cap.release()
    print('\n')
    print(f'一共{totalFrame}帧，保存至{save_path}')  # 表示一个视频片段已经转换完成
    return fps
def my_2DStitch(images,x,y,deltaLen=0,bgColor=0):
    nowIndex = 0
    colPics=[]
    for row in range(y):
        rowPics=[]
        for col in range(x):
            pic = images[nowIndex]
            rowPics.append(pic)
            nowIndex=nowIndex+1
        colPics.append(my_SimpleStitch(rowPics,'x',deltaLen,bgColor))
    return my_SimpleStitch(colPics,'y',deltaLen,bgColor)

def my_SimpleStitch(images, direction, deltaLen=0,bgColor=0):
    """
    输入图片数组
    输入'x'或者'y'
    输出拼接好的图片
    """
    widths, heights = zip(*(i.size for i in images))

    if direction == 'x':
        total_width = sum(widths) + (len(images)-1)*deltaLen
        max_height = max(heights)
        new_image = Image.new('RGB', (total_width, max_height),color=bgColor)
        x_offset = 0
        for img in images:
            new_image.paste(img, (x_offset, 0))
            x_offset += img.width
            x_offset += deltaLen
    elif direction == 'y':
        total_height = sum(heights)+ (len(images)-1)*deltaLen
        max_width = max(widths)
        new_image = Image.new('RGB', (max_width, total_height),color=bgColor)
        y_offset = 0
        for img in images:
            new_image.paste(img, (0, y_offset))
            y_offset += img.height
            y_offset += deltaLen

    return new_image

def my_GaussianBlur(srcPath, destPath, ksize,sigmaX,sigmaY):
    """
    将文件夹内所有的图片进行高斯模糊
    """
    srcPath = os.path.abspath(srcPath)
    destPath = os.path.abspath(destPath)
    if not os.path.exists(srcPath):
        raise IOError(f"无法打开{srcPath}")
    if not os.path.exists(destPath):
        os.mkdir(destPath)
        print(f"创建:{destPath}")
    if not os.path.exists(destPath):
        raise IOError(f"无法打开{destPath}")
    files = os.listdir(srcPath)
    num=len(files)
    now=0
    width = os.get_terminal_size().columns - 20
    for f in files:
        f = os.path.abspath(f)
        f = os.path.basename(f)
        srcFile = srcPath + '/' + f
        destFile = destPath + '/' + f


        if os.path.exists(destFile):
            raise IOError(f"已经存在{destPath}")
        img = cv2.imread(srcFile)
        img = cv2.GaussianBlur(img,ksize,sigmaX=sigmaX,sigmaY=sigmaY)
        if not cv2.imwrite(destFile,img):
            raise IOError(f"无法写入{destFile}")
        


        left = int(now*width/num)
        right = width-left
        print("\r进度:[", "▓" * left," "*right, f"]{now}/{num}", end="")
        now=now+1

    print('\nOKK')

def myExample_AddText(image,text,pos,colorRGB,ttfPath,fontSize=50):

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(ttfPath, fontSize)
    draw.text(pos, text, colorRGB, font=font,anchor='mm',
            stroke_width=5,
            stroke_fill=(0, 0, 0))
    
def myExample_AddRect(image,xyxy):
    draw = ImageDraw.Draw(image)
    draw.rectangle(xyxy, fill=(127,127,127),outline=(0,0,0),width=10)



def my_move_files(source_dir,hz, destination_dir):  
    # 确保目标目录存在  
    if not os.path.exists(destination_dir):  
        print("创建："+destination_dir)
        os.makedirs(destination_dir)  
  
    # 遍历源目录下的所有文件  
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            # base = os.path.splitext(filename)[0]  # 这会返回文件名（不带扩展名）  
            extension = os.path.splitext(filename)[1]  # 这会返回扩展名（带点.） 
            if(extension == hz):
                srcFile = os.path.join(dirpath, filename)  # 构造完整路径
                exPath = os.path.relpath(srcFile,source_dir)
                dstFile = os.path.join(destination_dir, exPath)  # 构造完整路径

                dstDir = os.path.dirname(dstFile)
                if not os.path.exists(dstDir):
                    os.makedirs(dstDir)  
                shutil.move(srcFile, dstFile)
                print(srcFile+"->"+dstFile)
            # 构造完整的文件路径
            # source_file_path = os.path.join(source_dir, filename)
            # source_file_path = os.path.abspath(source_file_path)
            # destination_file_path = os.path.join(destination_dir, filename)  
            # destination_file_path = os.path.abspath(destination_file_path)
            
            # # 检查是否为文件（而不是文件夹）  
            # if os.path.isfile(source_file_path):  
            #     # 移动文件  
            #     # shutil.move(source_file_path, destination_file_path) 
            #     print(source_file_path+"\n\t"+destination_file_path) 

def my_rename_files(source_dir,function):  
    # 遍历源目录下的所有文件  
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            srcFile = os.path.join(dirpath, filename)  # 构造完整路径
            dstFile = function(filename)
            # shutil.move(srcFile, dstFile)
            print(srcFile+"->"+dstFile)

def my_remove_empty_folders(path, remove_root=False):  
    # 递归函数，从底层开始删除空文件夹  
    if not os.path.isdir(path):  
        return  
  
    # 遍历文件夹内容  
    files = os.listdir(path)  
    if len(files):  
        for f in files:  
            full_path = os.path.join(path, f)  
            if os.path.isdir(full_path):  
                my_remove_empty_folders(full_path)  
  
    # 再次检查文件夹是否为空，如果是则删除  
    files = os.listdir(path)  
    if len(files) == 0 and not remove_root:  
        print(f"Removing empty directory: {path}")  
        os.rmdir(path)  
    elif len(files) == 0 and remove_root:  
        print(f"Removing empty root directory: {path}")  
        os.rmdir(path)  