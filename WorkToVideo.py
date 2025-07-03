import cv2
import os
from shutil import copyfile
import csv
import imageio

img_location = '/home/markv7/Документы/ЗЕБРА'
filename_in = 'тест/3_1.MOV'
dir_out = 'Dataset/images/train'
dir_out1 = 'DetectionYOLOv11/Dataset/predict'

def split_into_frames(img_location,filename_in,dir_out): # разбираем видео на кадры
    file_name = os.path.join(img_location,filename_in)
    cap = cv2.VideoCapture(file_name) # apiPreference = 3 -  исследовать этот аргумент
    # dir_out = filename_in.split('.')[0]
    pathbase = os.path.join(img_location, dir_out)
    if not os.path.exists(pathbase):
        os.makedirs(pathbase)
        print(f'Создаем каталог {pathbase}')
    print(f'Кадрируем видео... -> из файла {filename_in} в каталог {dir_out}')
    i = 0
    ItemKadr = 0
    flag = True
    while (cap.isOpened()):
        ItemKadr += 1
        ret , frame = cap.read()
        if ret == True:
            if (ItemKadr % 20 == 0) or flag:
                # frame_000000.png
                path = os.path.join(pathbase,f'frame_{str(i).rjust(6,"0")}.png')
                cv2.imwrite(path, frame)
                i += 1
        else:
            break
    # When everything done, release the video capture object
    cap.release()
    # Closes all the frames
    # cv2.destroyAllWindows()

def rotate_image(dir_input,dir_output):
    dir_input = os.path.join(img_location, dir_input)
    dir_output = os.path.join(img_location, dir_output)
    FilesList = sorted(os.listdir(dir_input))
    for frame in FilesList:
        print(frame)
        # Загрузка изображения
        img = cv2.imread(os.path.join(dir_input,frame))
        # Поворот на 180 градусов
        rotated_img = cv2.rotate(img, cv2.ROTATE_180)
        # Сохранение повернутого изображения
        cv2.imwrite(os.path.join(dir_output,frame), rotated_img)


def join_frames(img_location, filename):
    video_file = os.path.join(img_location, filename)
    out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (512, 512))
    # Write the frame into the file filename в цикле пробежаться
    FilesList = sorted(os.listdir(img_location))
    for frame in FilesList:
        path = os.path.join(img_location, frame)
        image = cv2.imread(path)
        #image = frame.array
        cv2.imshow("Frame", image)
        out.write(image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    out.release()
    cv2.destroyAllWindows()

def join_frames2(img_location, filename):
    video_file = os.path.join(img_location, filename)
    fnames = sorted(os.listdir(img_location))
    with imageio.get_writer(video_file, mode='I', fps=24) as writer:
        for fname in fnames:
            fname_full = os.path.join(img_location,fname)
            print(fname_full)
            frame = imageio.imread(fname_full)
            writer.append_data(frame)

def rename_files(img_location, str_sub='results', digit=4):
    fnames = os.listdir(img_location)
    for item in fnames:
        from_file = os.path.join(img_location,item)
        filename, file_extension = os.path.splitext(item)  # f'frame_{str(i).rjust(6,"0")}.png'
        to_outfile = str_sub + filename.split(str_sub)[1].rjust(digit,"0") + file_extension
        to_outfile = os.path.join(img_location,to_outfile)
        # print(f'Rename {from_file} into {to_outfile}')
        os.rename(from_file, to_outfile)


def allocation_samples(size_train=500, size_val=100, size_test=100): # разбиваем на выборки
    list_dir = ('images','labels')
    shift = 1500
    for item_dir in list_dir:
        dir_base = os.path.join('DetectionYOLOv11/Dataset',item_dir)
        dir_output1 = os.path.join(img_location,dir_base,'train')
        dir_output2 = os.path.join(img_location,dir_base,'val')
        dir_output3 = os.path.join(img_location,dir_base,'test')
        dir_output = dir_output1
        dir_input = os.path.join(img_location,'train_all',item_dir)
        FilesList = sorted(os.listdir(dir_input))[shift:size_train+size_val+size_test+shift]
        for item,frame in enumerate(FilesList):
            print(frame)
            if (item >= size_train):
                if (item < size_val+size_train):
                    dir_output = dir_output2
                else:
                    dir_output = dir_output3
            copyfile(os.path.join(dir_input, frame),os.path.join(dir_output, frame))

# записывает список текстовых строк в файл
def SaveTextFile(datatxt,filename):
    # FILE_NAME = os.path.join(DIR_FILE,filename)
    with open(filename, 'w', newline='\n', encoding='utf8') as file:
        writer = csv.writer(file)
        for item in datatxt:
            writer.writerow([item])

def create_discription_files():
    dir_base = os.path.join(img_location, 'Dataset')
    item_dir = 'images'
    list_dir = ('train','val','test')
    for item in list_dir:
        dir_input = os.path.join(dir_base, item_dir, item)
        # print(dir_input,dir_base)
        filesList = [os.path.join(item_dir,item,item_f) for item_f in sorted(os.listdir(dir_input))]
        file_input = os.path.join(dir_base, item+'.txt')
        print('Формируем файл',file_input)
        SaveTextFile(filesList, file_input)

if __name__ == '__main__':
    # pass
    # create_discription_files()
    # allocation_samples()
    # rotate_image('Dataset/images/train1', 'Dataset/images/train')
    # split_into_frames(img_location,filename_in,dir_out)
    # rename_files(os.path.join(img_location,dir_out1))
    join_frames2(os.path.join(img_location,dir_out1), 'video_out.mp4')