# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 02:00:58 2020
"""
#pip install msvc-runtime
import selectivesearch
import numpy as np
import tensorflow as tf
from PIL import Image
import argparse
from xml.etree.ElementTree import ElementTree

import slidingWindow as sw
import augmentation
import dataSet as ds
import utils
import model
import solver
import blackPercent as bp
import os

import streamlit as st

#################################STREAMLIT APPLICATION
st.write("""
         # 전동킥보드 안전 주차 확인 시스템
         """)

st.write("보행자들의 안전을 위해 갓길에 주차 후 사진을 찍어 올려주시기 바랍니다.")

file = st.file_uploader("이미지 파일 업로드", type=["jpg", "png"])

if file is None:
    st.write("주차된 전동킥보드의 사진을 올려주세요")
else: 
    image = Image.open(file)
    img_dir = os.getcwd() + '\\' + 'test_image' + '\\'+file.name
    # st.write(img_dir)
    image.save(img_dir)
    st.image(image, caption = '주차된 전동킥보드', use_column_width=True)
    # prediction = import_and_predict(image, model)

 							

#################################################
parser = argparse.ArgumentParser()
parser.add_argument("-training", "--training", type=bool, default=False)
parser.add_argument("-epochs", "--epochs", type=int, default=100)
args = parser.parse_args()

print("Phase 0 : Load data")
data = ds.dataSet()
j = ds.jsonObject('para.json')
param = j.para
print(param)

target_index = []
for cl in param['label_dic']:
    if cl in param['target_list']:
        target_index.append(param['label_dic'][cl])

training = args.training

if training:
    data_dir = 'image'
else:
    data_dir = None
    
data.load_data(dir=data_dir, test_dir='test_image')

#data.grayscale()
data.augmentation()
#data.edge()

if training:
    data.sep_train_test()
_, *model_input_size = data.img_set.shape

sess = tf.Session()
model = model.four_layer_CNN(sess=sess, input_shape=data.img_set.shape, n_class=len(param['label_dic']))
sv = solver.Solver(sess=sess, name='op', model=model, dataset=data, optimizer=tf.train.AdamOptimizer)

epochs = args.epochs
batch_size = param['batch_size']
learning_rate = param['lr']
path = '/home/paperspace/Dropbox/krlee/easy-yolo/devkit/2017/Images'

sess.run(tf.global_variables_initializer())

if not training:
    print("Phase 1 : Load model")
    sv.model_load('braille_segment.h5')

else:
    print("Phase 1 : Train model")
    sv.train(epoch=epochs, batch_size=batch_size, lr=learning_rate, print_frequency=100)
    sv.model_save('braille_segment.h5')

def cf(x):
    return sv.predict(x)[0] in target_index

def score_cf(imag):
    scores = np.array(sv.predict_softmax_score(imag))
    return (np.argmax(scores) in target_index) and (np.max(scores) > param['score_bottom_line'])


for i, img in enumerate(data.test_img):
    print("{}th image in progress".format(i))
    temp_img, matrix = sw.sliding_window(img, score_cf, window_size=param['ss_dic']['window_size'], stride=16, boundary=param['sw_dic']['boundary'])
    check = bp.bpercent(temp_img)
    if check : 
        print(i+1,"번째 사진: ","점자블록이 없는 곳으로 이동해주세요")
        st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
        st.markdown("""
            <style>
            body {
                color:white;
                background-color:red;
                font-size:30;
            }
            </style>
            점자블록이 없는 곳에 킥보드를 주차해 주세요
                """, unsafe_allow_html=True)
        os.remove(img_dir)
    else: 
        st.write("전동 킥보드가 반납되었습니다")
        os.remove(img_dir)
    temp_img.save('./test_result/sw'+str(i)+'.jpg', 'jpeg')
    img.save('./Images/sw'+str(i)+'.jpg', 'jpeg')
    print()