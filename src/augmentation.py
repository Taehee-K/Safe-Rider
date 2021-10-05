import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import array_to_img, img_to_array, load_img
import numpy as np

def augmentation(images_array,rotate=30,shift=30,shear=30,gray=True):
	
	# count : image 생성 갯수
	#print(rotate, shift, shear)
	print("이미지 array shape: ",images_array.shape)
	#print(images_array)
	counts_set = [rotate, shift, shear]

	# 함수 정의 
	gen_rotation = ImageDataGenerator(rotation_range=180)
	gen_shift = ImageDataGenerator(featurewise_center=True, width_shift_range=0.25, height_shift_range=0.25)
	gen_shear = ImageDataGenerator(shear_range=0.5) # 0.8이면 더 길어짐

	# create infinite flow of images
	images_flow_set = []
	images_flow_set.append(gen_rotation.flow(images_array, batch_size=1)) 
	#print("rotation flow: ", len(images_flow_set), images_flow_set)
	images_flow_set.append(gen_shift.flow(images_array, batch_size=1))
	#print("shift flow: ", len(images_flow_set), images_flow_set)
	images_flow_set.append(gen_shear.flow(images_array, batch_size=1)) 
	#print("shear flow: ", len(images_flow_set), images_flow_set)

	#aug_result = np.empty((0,) + images_array.shape[1:])
	aug_result = np.empty((0,) + images_array.shape[1:])

	for j,images_flow in enumerate(images_flow_set):
        #counts_set = [3,3,3]
		#print("얘가 j:", j)
		count = counts_set[j]
		for i, new_images in enumerate(images_flow):
	    # we access only first image because of batch_size=1
			#print("aug shape: ",aug_result.shape)
			#print("new shape: ",new_images.shape)
			#print("얘가 i: ", i)
			#print("얘가 new_images: ", new_images)
			#new_image = array_to_img(new_images[0], scale=True)
			aug_result = np.append(aug_result, new_images, axis = 0)
			#new_image.save(output_path.format(30*(j)+i + 1))
			if i >= count:
				break

	aug_result = np.append(images_array, aug_result, axis = 0)
	print("최종 aug: ", aug_result.shape)
	return aug_result

#augmentation('sohee.jpg',gray=False)