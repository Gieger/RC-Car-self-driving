import cv2, os
import numpy as np
import matplotlib.image as mpimg


IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 66, 200, 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)


def load_image(data_dir, image_file):
    return mpimg.imread(os.path.join(data_dir, image_file.strip()))


def crop(image):  
    return image[200:800, :, :]


def resize(image):
    return cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT), cv2.INTER_AREA)


def rgb2yuv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2YUV)


def preprocess(image):
    image = crop(image)
    image = resize(image)
    image = rgb2yuv(image)
    #cv2.imshow('image1',image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return image


def choose_image(data_dir, center, left, right, steering_angle):
    choice = np.random.choice(3)
    if choice == 0:
        return load_image(data_dir, left), steering_angle
    elif choice == 1:
        return load_image(data_dir, right), steering_angle
    return load_image(data_dir, center), steering_angle


def random_flip(image, steering_angle):
    if np.random.rand() < 0.5:
        image = cv2.flip(image, 1)
        steering_angle = -steering_angle
    return image, steering_angle


def random_shadow(image):
    x1, y1 = 320 * np.random.rand(), 0
    x2, y2 = 320 * np.random.rand(), 180
    xm, ym = np.mgrid[0:180, 0:320]

    mask = np.zeros_like(image[:, :, 1])
    mask[(ym - y1) * (x2 - x1) - (y2 - y1) * (xm - x1) > 0] = 1

    cond = mask == np.random.randint(2)
    s_ratio = np.random.uniform(low=0.6, high=0.9)

    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    hls[:, :, 1][cond] = hls[:, :, 1][cond] * s_ratio
    return cv2.cvtColor(hls, cv2.COLOR_HLS2RGB)


def random_brightness(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    ratio = 1.0 + 0.4 * (np.random.rand() - 0.5)
    hsv[:,:,2] =  hsv[:,:,2] * ratio
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)


def augument(data_dir, center, left, right, steering_angle, range_x=100, range_y=10):
    image, steering_angle = choose_image(data_dir, center, left, right, steering_angle)
    image, steering_angle = random_flip(image, steering_angle)
    #image = random_shadow(image)
    #image = random_brightness(image)
    return image, steering_angle


def batch_generator(data_dir, image_paths, steering_angles, batch_size, is_training):
    images = np.empty([batch_size, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
    steers = np.empty([batch_size, 2])

    while True:
        i = 0
        for index in np.random.permutation(image_paths.shape[0]):
            center = image_paths[index]
            steering_angle, throttle = steering_angles[index]
            image = load_image(data_dir, center)
            images[i] = preprocess(image)
            steers[i][0] = steering_angle
            steers[i][1] = throttle

            i += 1
            if i == batch_size:
                break
        yield images, steers
