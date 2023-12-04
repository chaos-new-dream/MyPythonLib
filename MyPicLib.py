
import cv2
import os
import sys
from PIL import Image

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

def my_SimpleStitch(images, direction):
    """
    
    """
    widths, heights = zip(*(i.size for i in images))

    if direction == 'x':
        total_width = sum(widths)
        max_height = max(heights)
        new_image = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for img in images:
            new_image.paste(img, (x_offset, 0))
            x_offset += img.width
    elif direction == 'y':
        total_height = sum(heights)
        max_width = max(widths)
        new_image = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for img in images:
            new_image.paste(img, (0, y_offset))
            y_offset += img.height

    return new_image

def my_GaussianBlur(srcPath, destPath, ksize,sigmaX,sigmaY):
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

