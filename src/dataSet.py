import pickle
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
#pip install msvc-runtime
from skimage import feature

import json
import augmentation
import utils

class jsonObject():
	def __init__(self, dir):
		with open(dir, 'r') as f:
			self.para = json.load(f)

class dataSet():
	'''
	 - Data 원본을 저장하고, 매번 필요한 경우 리사이징을 하자?
	'''
	def __init__(self, para_filename='para.json'):
		self.train_image = np.empty(0)
		self.train_label = np.empty(0)
		self.test_image = np.empty(0)
		self.test_label = np.empty(0)
		self.label_dic = {}
		self.ori_img_set = []
		self.img_set = []
		self.label_set = []
		self.width, self.height, self.color = 0, 0, 0

		self.batch_size = 32
		self.batch_index = []
		self.n_example = 0
		self.n_class = 0
		self.load_para(para_filename)

	def load_para(self, filename='para.json'):
		j = jsonObject(filename)
		js = j.para
		self.label_dic = js['label_dic']
		self.resizing = js['resizing']
		self.target_list = js['target_list']
		self.score_bottom_line = js['score_bottom_line']
		self.test_rate = js['test_rate']
		self.width, self.height = self.resizing
		self.n_size_reset()

	def n_size_reset(self):
		self.test_size = int(self.n_example * self.test_rate)
		self.train_size = self.n_example - self.test_size
		print(self.test_size, self.train_size)

	def load_data(self, dir, test_dir): # 현경
		sys_file = []
		self.img_set = np.empty((0,) + tuple(self.resizing) + (3,))

		# 만약 label_dic이 비어있으면, 폴더 이름을 불러옴
		if self.label_dic == {}:
			for i, filename in enumerate(os.listdir(os.getcwd() + '/' + dir)):
				self.label_dic[filename] = i

		if dir is not None:
			for label in self.label_dic:
				img_dir = os.getcwd()+ '/' + dir + '/' + label
				print(img_dir)

				for path, _, files in os.walk(img_dir):
					for file in files:
						img_dir = path + '/' + file
						try:
							img = Image.open(img_dir)
						except OSError as e:
							sys_file.append(e)
						else:
							# 만약 image가 RGB 포맷이 아닐경우, RGB로 변경
							if not img.format == "RGB":
								img = img.convert("RGB")

							self.ori_img_set.append(img)
							self.img_set = np.append(self.img_set, np.array([np.array(img.resize(self.resizing))]), axis=0)
							#print(self.img_set)
							self.label_set = np.append(self.label_set, self.label_dic[label])


			self.n_example, self.width, self.height, self.color = self.img_set.shape
			print(self.img_set.shape)
			self.n_size_reset()
			self.n_class = len(self.label_dic)

			
		else:
			self.img_set = np.empty((0,) + tuple(self.resizing) + (3,))

		if test_dir is not None:
			self.test_img = []
			img_dir = os.getcwd() + '/' + test_dir
			print(img_dir)

			for path, _, files in os.walk(img_dir):
				#print(len(files))
				for file in files:
					img_dir = path + '/' + file
					#print(img_dir)
					#print("test사진")
					try:
						img = Image.open(img_dir)
						#print("try")
						# 사이즈 일괄조정을 위해 하드코딩함
					except OSError as e:
						sys_file.append(e)
						#print("except")
					else:
						# 만약 image가 RGB 포맷이 아닐경우, RGB로 변경
						if not img.format == "RGB":
							img = img.convert("RGB")

						# 만약 image가 정사각형이 아닐경우, 정사각형 두 개로 자른다.
						if img.size[0] > img.size[1]:
							img1 = img.crop((0,0,img.size[1],img.size[1]))
							img2 = img.crop((img.size[0]-img.size[1],0,img.size[0],img.size[1]))
							img1 = img1.resize((416,416))
							img2 = img2.resize((416,416))
							self.test_img.append(img1)
							self.test_img.append(img2)
							#print("가로가 길다~")
						elif img.size[0] < img.size[1]:
							img1 = img.crop((0,0,img.size[0],img.size[0]))
							img2 = img.crop((0,img.size[1]-img.size[0],img.size[0],img.size[1]))
							img1 = img1.resize((416,416))
							img2 = img2.resize((416,416))
							self.test_img.append(img1)
							self.test_img.append(img2)
							#print("세로가 길다~")
						else:
							img = img.resize((416,416))
							self.test_img.append(img)
							#print("정사각형이다~")
						print(len(self.test_img))

	def sep_train_test(self):
		'''
			train / test로 분할 함, size는 para.json에 저장된 값 부름
		:return:
		'''
		print('debug : ', self.img_set.shape)
		ind = np.random.randint(self.n_example, size=self.train_size+self.test_size)
		self.train_image = self.img_set[ind[:self.train_size]]
		self.train_label = self.label_set[ind[:self.train_size]]
		self.test_image = self.img_set[ind[self.train_size:]]
		self.test_label = self.label_set[ind[self.train_size:]]

	def _resize(self, size=None):
		# size를 따로 받지 않았을 경우, para.json에 저장되어 있는 값으로 resizing
		if size is None:
			size = self.resizing
		resizing_size = tuple(size) + (self.img_set[0].shape[2],)
		self.img_set = np.empty((0,) + resizing_size)
		for img in self.ori_img_set:
			temp = np.array(img.resize(size)).reshape(((-1,) + resizing_size))
			self.img_set = np.append(self.img_set, temp, axis=0)

	def save(self, dir): # 현경
		temp_dataset = {
			'train_image' : self.train_image,
			'train_label' : self.train_label,
			'test_image' : self.test_image,
			'test_label' : self.test_label
		}
		with(open(dir, 'wb')) as f:
			pickle.dump(temp_dataset, f)

	def one_hot_encoding(self):  # 현경
		temp_list = np.zeros((self.n_example, self.n_class))
		temp_list[np.arange(self.n_example), np.array(self.label_set)] = 1
		self.label_set = temp_list

	def one_hot_decoding(self):
		self.label_set = [np.where(i==1)[0][0] for i in self.label_set]

	def print_informaton(self): # 광록
		print('train_data : {}, test_data : {}'.format(self.train_size, self.test_size))
		print('image_size : ({}, {})'.format(self.width, self.height))
		for i in np.unique(self.train_label):
			print('sample image : {}'.format(i))
			ind = np.where(self.train_label == i)
			self.sample_image(ind[0][0])

	def mini_batch(self, batch_size): # 광록
		pass

	def _make_batch_index(self):
		self.batch_index = np.split(np.random.permutation(self.train_size), np.arange(1, int(self.train_size // self.batch_size) + 1) * self.batch_size)
		if self.batch_index[-1] == []:
			self.batch_index = self.batch_index[:-1]

	def next_batch(self): # 광록
		if len(self.batch_index) == 0:
			self._make_batch_index()
		ind = self.batch_index[0]
		self.batch_index = self.batch_index[1:]
		return self.train_image[ind], self.train_label[ind]

	def grayscale(self):
		print('---grayscale---')
		RGB_to_L = np.array([[[[0.299,0.587,0.114]]]])
		self.img_set = np.sum(self.img_set * RGB_to_L, axis=3, keepdims=True)
		_, self.width, self.height, self.color = self.img_set.shape

	def augmentation(self):
		print('---Image augmentation---')
		print(self.img_set.shape)
		self.img_set = augmentation.augmentation(self.img_set,50,50,50)
		print('debug : ', self.img_set.shape)
		_, self.width, self.height, self.color = self.img_set.shape
		self.n_size_reset()

	def hog(self):
		print('---HOG---')
		img_to_hog = lambda img: utils.hog(img)
		self.img_set = np.array(list(map(img_to_hog, self.img_set)))
		with open('para.json', 'r') as f:
			js = json.load(f)
			block_wid = js['hog_dic']['block_width']
			block_hei = js['hog_dic']['block_height']
			n_ori = js['hog_dic']['n_orient']
		self.img_set = self.img_set.reshape((-1, n_ori, int(self.width / block_wid + 0.5), int(self.height / block_hei + 0.5)))
		self.img_set = np.transpose(self.img_set, (0,2,3,1))
		self.n_example, self.width, self.height, self.color = self.img_set.shape
		self.n_size_reset()

	def edge(self):
		print('---EDGE---')
		self.img_set = np.sum(self.img_set, axis=3, keepdims=False)
		self.img_set = np.array(list(map(feature.canny, self.img_set)))
		self.img_set = self.img_set.reshape(self.img_set.shape+(1,))
		self.n_example, self.width, self.height, self.color = self.img_set.shape
		self.n_size_reset()

	def sample_image(self, index=0):
		if self.train_image.shape[3] == 3:
			plt.imshow(self.train_image[index]/255)
		elif self.train_image.shape[3] == 1:
			plt.imshow(self.train_image[index].reshape((self.width, self.height))/255)
		plt.show()

	def object_detect(self):
		pass