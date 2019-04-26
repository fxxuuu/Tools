# -- coding: utf-8 --
import os
import cv2
import numpy as np


cvt_mat = np.array(
    ([0.114, 0.587, 0.299],  #bgr转yuv的转换矩阵
    [0.5, -0.3313, -0.1678],
    [-0.0813, -0.4187, 0.5])
)


def cvt_rgb2yuv(img, yuv_type='YUV444'):
    '''
    可选模式：YUV444、YUV422、YUV420, YUVGray
    '''
    if yuv_type not in ['YUV444', 'YUV422', 'YUV420', 'YUVGray']:
        raise ValueError('unknown yuv type')

    height, width, channels = img.shape
    yuv_img = np.zeros(img.shape)
    B,G,R = img[:,:,0], img[:,:,1], img[:,:,2]
    Y = 0.299*R+0.587*G+0.114*B
    U = (B-Y)/1.772 + 128
    V = (R-Y)/1.402 + 128

    if yuv_type == 'YUV422' or yuv_type == 'YUV420':
        for i in range(width-width%2):
            if i%2==0:
                U[:,i] = (U[:,i]+U[:,i+1])/2
                V[:,i] = (V[:,i]+V[:,i+1])/2
            else:
                U[:,i] = U[:,i-1]
                V[:,i] = V[:,i-1]
    if yuv_type == 'YUV420':
        for j in range(height-height%2):
            if j%2==0:
                U[j,:] = (U[j,:]+U[j+1,:])/2
                V[j,:] = (V[j,:]+V[j+1,:])/2
            else:
                U[j,:] = U[j-1,:]
                V[j,:] = V[j-1,:]
    yuv_img[:,:,0], yuv_img[:,:,1], yuv_img[:,:,2] = Y,U,V
    return yuv_img


def main():
    pass


if __name__ == '__main__':
    i=0
    with open('/home/fangxin/h3_workspace/train_annotations/total_149838/Fisheye_fov180.list', 'r') as f:
        for line in f.readlines():
            try:
                img_name = line.strip()
                img_path = os.path.join('/share10/public/fangxin/train_images', img_name)
                jpg_img = cv2.imread(img_path)

                name = img_name.split('/')[-1]

                yuv444_path = os.path.join('/share10/public/yangzhenghao/RGB_TO_YUV/YUV444', name)
                if not os.path.exists(yuv444_path):
                # yuv422_path = os.path.join('/share10/public/yangzhenghao/RGB_TO_YUV/YUV422', name)
                # yuv420_path = os.path.join('/share10/public/yangzhenghao/RGB_TO_YUV/YUV420', name)
                    yuv_444 = cvt_rgb2yuv(jpg_img, yuv_type='YUV444')
                # yuv_422 = cvt_rgb2yuv(jpg_img, yuv_type='YUV422')
                # yuv_420 = cvt_rgb2yuv(jpg_img, yuv_type='YUV420')

                    cv2.imwrite(yuv444_path, yuv_444)
            except:
                pass
            # cv2.imwrite(yuv422_path, yuv_422)
            # cv2.imwrite(yuv420_path, yuv_420)
            print(name, 'Done', i)
            i += 1

