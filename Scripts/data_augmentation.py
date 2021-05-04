import numpy as np
import cv2
import sys
import random
import os
import imgaug
import pickle
import imgaug.augmenters as iaa
from random import seed
from shutil import copyfile


i = 0
random.seed()
name = 20869
seed(1)
classes = 51
percentual = 0.5
CHUNK_SIZE = 1436
classes_use = np.zeros(classes)
valid = [[] for _ in range(classes)]

_train_list = []
_valid_list = []
_test_list = []


path = '/Users/rafaelandradedasilva/Desktop/grabber project/Datasets/regulamentacao/'
folder_dest = '/Users/rafaelandradedasilva/Desktop/grabber project/DA/'

def get_num_files(folder):
    num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])
    return num_files

def get_num_files2(folder):
    return len(os.listdir(folder))

def load_images(self, images_path, extensions):
        all_images = []
        for ext in extensions:
            for path in Path(images_path).rglob('*' + ext):
                all_images.append(path.as_posix())
        all_images.sort()
        print("Images loaded: {0}".format(len(all_images)))
        return all_images

def progress(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    fmt = '[%s] %s%s ...%s' % (bar, percents, '%', status)
    print('\b' * len(fmt), end='')  # clears the line
    sys.stdout.write(fmt)
    sys.stdout.flush()
    if percents == 100:
        print('Job Done =*')

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def shinny_day(image, gamma=1.5):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def dark_day(image, gamma=0.5):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def distortion(image, kernel=3):
    median = cv2.medianBlur(image, kernel)
    return median

def snow(image, severity=2):    
    aug = iaa.imgcorruptlike.Frost(severity)
    img = aug(image=image)
    return img

def saltAndPepper(image, p=0.2):
    aug = iaa.SaltAndPepper(p)
    img = aug(image=image)
    return img

def contrast(image, severity=2):
    aug = iaa.imgcorruptlike.Contrast(severity)
    img = aug(image=image)
    return img

def rain(image, severity=2):
    aug = iaa.imgcorruptlike.Spatter(severity)
    img = aug(image=image)
    return img

def zoom(image, severity=2):
    aug = iaa.imgcorruptlike.ZoomBlur(severity)
    img = aug(image=image)
    return img

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

qtd = 0

while (i < 51):
    count = get_num_files2(folder=path + str(i) + '/') - 1
    for o in range(count):
        _img = cv2.imread(path + str(i) + '/' + str(o + 1) + '.png')
        _frm = cv2.resize(_img, (32,32))
        cv2.imwrite(os.path.join('/Users/rafaelandradedasilva/Desktop/grabber project/DA/' + str(i) + '/', str(o + 1)) + '.png', _frm)
        #copyfile(path + str(i) + '/' + str(o + 1) + '.png', folder_dest + str(i) + '/' + str(o + 1) + '.png')

    if count < 310:
        num_transforms = int(450 / count)
        for m in range(count):
            progress(m, count, status='Making the Data Augmentation. Sample  No: ' + str(m + 1) + ' for class ' + str(i) + '. Trans: ' + str(num_transforms))
            fr = cv2.imread(path + str(i) + '/' + str(m + 1) + '.png')
            frame = cv2.resize(fr, (32,32))
            for n in range(num_transforms):
                r_im = rotate_image(frame, random.randint(1, 15))
                selector = random.randint(0, 8)
                if selector == 0:
                    r_im2 = shinny_day(r_im)
                elif selector == 1:
                    r_im2 = dark_day(r_im)
                elif selector == 2:
                    r_im2 = distortion(r_im)
                elif selector == 3:
                    r_im2 = snow(r_im)
                elif selector == 4:
                    r_im2 = saltAndPepper(r_im)
                elif selector == 5:
                    r_im2 = contrast(r_im)
                elif selector == 6:
                    r_im2 = rain(r_im)
                elif selector == 7:
                    r_im2 = rain(r_im, severity=3)
                else:
                    r_im2 = zoom(r_im)
                #print(n)
                name = (count + (n + 1)) + (num_transforms * m)
                cv2.imwrite(os.path.join('/Users/rafaelandradedasilva/Desktop/grabber project/DA/' + str(i) + '/', str(name)) + '.png', r_im2)
    qtd += get_num_files2(folder=folder_dest + str(i) + '/') - 1            
    i += 1
    
i = 0
cnt = 0
print('\nTotal of traffic signs: ' + str(qtd))
npy_test_file = []

while (i < 51):
    count = get_num_files2(folder=folder_dest + str(i) + '/') - 1
    for k in range(count):
        progress(k, count, status='Making the Dataset. Sample  No: ' + str(k + 1) + ' for class ' + str(i))
        im = cv2.imread(folder_dest + str(i) + '/' + str(k + 1) + '.png')
        b = im[:,:,0].flatten()
        g = im[:,:,1].flatten()
        r = im[:,:,2].flatten()
        if k <= int(count * (0.5)):
            out = np.array([str(i)] + list(r) + list(g) + list (b), np.uint8)
            _train_list.append(out)
        elif int(count * 0.5) < k <= int(count * 0.75):
            out = np.array([str(i)] + list(r) + list(g) + list (b), np.uint8)
            _valid_list.append(out)
        else :
            npy_test_file.append(i)
            copyfile(folder_dest + str(i) + '/' + str(k + 1) + '.png', folder_dest + '/test_images/' + str(cnt) + '.png')
            out = np.array([str(i)] + list(r) + list(g) + list (b), np.uint8)
            _test_list.append(out)
            cnt += 1
    i += 1

print('\nTrain list size: ' + str(len(_train_list)))
print('\nValid list size: ' + str(len(_valid_list)))
print('\nTest list size: ' + str(len(_test_list)))


batchs = list(chunks(_train_list, CHUNK_SIZE))
for i in range(len(batchs)):
    with open(folder_dest + 'training_batch_' + str(i+1), 'wb') as fp:
        pickle.dump(batchs[i], fp)

with open(folder_dest + 'training_unique_batch', 'wb') as fp:
    pickle.dump(_train_list, fp)

with open(folder_dest + 'validation_batch', 'wb') as fp:
    pickle.dump(_valid_list, fp)

with open(folder_dest + 'testing_batch', 'wb') as fp:
    pickle.dump(_test_list, fp)

np.save(folder_dest + 'true_Y', npy_test_file)
