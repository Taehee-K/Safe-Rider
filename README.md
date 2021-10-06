# Safe Rider
고은지 김민지 김태희 이수연 정희원<br>
(2020.12.17~2020.12.19)

## Overview
<img alt="overview1" src="https://user-images.githubusercontent.com/63901494/136033356-01f2865a-6d7e-45bf-bb1e-b3300a8daa7d.jpg" height="150">&nbsp;&nbsp;&nbsp;<img alt="overview2" src="https://user-images.githubusercontent.com/63901494/136032982-c6276f6d-bb04-4968-84e2-ab3351faec7a.jpg" height="150">&nbsp;&nbsp;&nbsp;<img alt="overview3" src="https://user-images.githubusercontent.com/63901494/136033503-2b438097-3436-41c5-9282-c963f91f0732.jpg" height="150"><br>
Safe Rider는 사용자와 보행자 모두가 안전한 전동킥보드 시스템입니다. 

공유 전동킥보드가 급격하게 늘어나 새로운 이동수단으로 인기를 얻는 반면, 관련 안전수칙 및 규율 부족으로 사용자와 지나가는 보행자의 안전에 위협을 가하고 있습니다. 전동킥보드를 보행에 방해되는 위치에 주차를 하는 경우, 한 손으로 운전하는 경우들이 빈번하게 이루어지고 있으며 특히 이들이 시각장애인들에게 방향의 지표가 되는 점자블록 위에 주차되어 있을 때 그 위험성은 더 커집니다. <!--실제로 전동 킥보드의 발판 높이는 시각 장애인들의 발목 높이와 비슷하기에 시각장애인들이 보행시 미리 인지하기가 어렵고, 치명적인 부상을 당할 확률도 높습니다.--> <br>
본 프로젝트는 시각장애인 보행자 안전을 고려한 주차 및 양손운전을 유도함으로써 보다 안전한 전동킥보드 시스템을 제안합니다.

## Implementation
### 안전주차
<img alt="braille-kickboard" src="https://user-images.githubusercontent.com/63901494/136039318-2591657f-6bab-46ac-9a47-791ff3d213b0.png" height="200"><br>
현재 전동킥보드 사용자는 반납 시 확인을 위해 전동킥보드 대여 앱에 사진을 찍어 인증해야 합니다. <br>
이미지 인식 기술을 활용해 시각장애를 가진 보행자들의 안전에 위협이 되는 위치, 즉 점자블록 근처에 킥보드가 주차된 경우를 식별해 주차 불가 장소임을 알립니다. <br>
<br>
점자블록 탐지 모델로는 [You Only Look Once: Unified, Real-Time Object Detection, 2015](https://arxiv.org/abs/1506.02640)의 YOLOv1을 사용하였습니다. 

### 양손운전
<img alt="handle1" src="https://user-images.githubusercontent.com/63901494/136038534-8e0d2b33-03f1-429d-b704-914f92d42bdc.png" height="200">&nbsp;&nbsp;<img alt="handle2" src="https://user-images.githubusercontent.com/63901494/136038854-4f657831-4aab-4c16-86a5-472729f615b2.png" height="200"><br>
손잡이의 아두이노 센서를  전동킥보드 운전자가 양손을 손잡이에 올려둔 채 주행하고 있는지 확인 합니다.<br> 
한 손만 이용하여 주행 중인 것이 확인되면 경고 알람을 울려 사용자의 안전한 운전을 유도합니다.

## Usage
Clone Repository
```
git clone https://github.com/Taehee-K/Safe-Rider.git
cd Safe-Rider/src
```
**안전주차**<br>
```
// Train
python main.py --training True

// Demo
streamlit run app.py
```

**양손운전**<br>
```
// run on Arduino IDE
handle.ino
```

## Demo
### 안전주차
https://user-images.githubusercontent.com/63901494/136041302-2d9c9faf-9a94-4517-9a52-0c9572072317.mov 

### 양손운전
https://user-images.githubusercontent.com/63901494/136041767-e52aa982-0350-428f-8fa0-133120e88502.mp4 

## Reference
* [krlee407/Braille-Blocks](https://github.com/krlee407/Braille-Blocks)