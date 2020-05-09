#!/usr/bin/env python3
""" HNGN001 Created on Tue Jun 11 08:34:11 2019
(two days before 190613) (1month before 190711)"""


s1="""HNGN1,澄江さんが亡くなる2日前に書いたもの。輻射伝熱について勉強しようとしていた。（4乗則でどれくらい熱が逃げるかPythonのプログラムで計算して知りたかった。）ここで作ったものは外とつながなければ、仏像を1000体彫る事と同じことはできないだろう。コミニケーションをとることが、つながることが、大きな目的の1つだから。\n """

s2="""
2020年4月の517号室での最初の加熱実験では、加熱の入力が340ワット。それで200度から640度まで20秒で上がった。

HNGN82 から、温度上昇のモデルを引き継ぐ。
"""

s3="""
時間刻みの中で全てのストーリーが成り立つように組み上げる。
"""

print(s1+"\n"+s2+"\n"+s3+"\n")

s4="""
t = i*dt
T=Treal-Ttarget

T += dt*(Q/H)

W_heat=Input_of_Control_Loop=heater_power_input

W_heat += Kp*(T) + Kd*(Q/H) + Ki*(T*dt)
Q=W_heat-W_cool
"""

s5="""
{200502}
x <=> T
w <=> (Tdt)
v <=> (Q/H)

	for i in range(int(50/dt)):
		t = i*dt
		x += dt*v
		w += dt*x
		F = -x*Kp -v*Kd -w*Ki
		v += dt*F/m
"""

def W_cool():
	s=""" Cooling power (J/sec)
	refer HNGN82_200427
	H=heat capasiry(J/K)
	Troom=20
	Q=stored heat(J)
	"""
	Troom=20
	Hcond=0.2
	W=Hcond*(dT+Ttarget-Troom)
	return W

from matplotlib import pyplot as plt
from matplotlib import animation as animation
import numpy as np
import serial
import time
import sys
import re

# strPort = '/dev/tty.usbserial-A7006Yqh'
print ("pls input port name = M5Stck, ARDUINO, file_name.csv")
print ("use LS command to find port name") 

# plot parameters
#analogData = AnalogData(100)
#analogPlot = AnalogPlot(analogData)

#tc1 = [0] * 100
#tc2 = [0] * 100
#cnv = [0]*100
t=np.linspace(0.0,10.0,100)
# open serial port
strPort1 = sys.argv[1];
strPort2 = sys.argv[2];
file1=sys.argv[3];
ser1 = serial.Serial(strPort1, 115200) # M5Stack Serial Speed
ser2 = serial.Serial(strPort2, 115200) # Arduino Serial Speed
f=open(file1,"w+")
#
#
#fig, ax = plt.subplots()
ims = []
dt = 0.1
Kp = 0.0			
Kd = 0.0
Ki = 0.0	

regex = re.compile('\d+')
data=[]
flag=0
while 1:
  dT_list = []
  t_list = []
  if Kp < 0.0:		#比例ゲイン
    Kp += 0.01
  elif Ki < 0.001:	#積分ゲイン
    Ki += 0.001
  elif Kd < 0.5:		#微分ゲイン
    Kd += 0.01

#### ###				
  Q=Initial_heat=2000 #initial condition
  W_heat_max=300 #heater power at 100V (MAX)
  rCp=3.36  # =(J/K)from H of HNGN82
  T=Q/rCp-273.15
#  print("T=Treal=",T)
	
  Ttarget=T_target_degC=600 #Target
  TtargetK=Ttarget+273.15 
  W_heat=50 #=280,(J/sec) initial condition
  dQ=0
	
	#    data=[]
  line = ser1.readline()
  match = regex.findall(str(line))
  data.append(float(match[1])*60.0+float(match[2])+float(match[3])*0.1)
  data.append(float(match[4]+"."+match[5]))
  data.append(float(match[6]+"."+match[7]))
  data.append(float(match[8]+"."+match[9]))
  data.append(float(match[10]+"."+match[11]))
  data.append(float(match[12]+"."+match[13]))
  data.append(float(match[14]+"."+match[15]))
  data.append(float(match[16]+"."+match[17]))
  data.append(float(match[18]+"."+match[19]))
  data.append(float(match[20]+"."+match[21]))
  data.append(float(match[22]+"."+match[23]))
  print(data[2],data[4],data[5])
  for val in data:
    flag+=1
    f.write(str(val)); 
    if(flag<11): 
      f.write(", ")
  f.write("\n")
  flag=0

  #for i in range(int(50/dt)):
  #  t = i*dt
#Tc thermo-couple-reading
  T=data[5] #unit=Cdegree) reading from Tc
  data=[]
#  print("T=",f'{T:.4f}')
  dT=error_T=T-Ttarget
#  print("dT=",f'{dT:.4f}')
#  print("Q=",f'{Q:.4f}')
#  print("W_cool=",f'{W_cool():.4f}')
#  print("W_heat=",f'{W_heat:.4f}')
  Kp=0.1; Kd=0.5; Ki=0.0
  W_heat+= -Kp*(rCp*dT)*dt -Kd*(dQ/dt)*dt -Ki*(dT*dt)
#  print("W_heat=",f'{W_heat:.4f}')
  dQ=dt*(W_heat-W_cool())
#  print("dQ=",f'{dQ:.4f}'+"\n")
  Q +=dQ
  T=Q/rCp-273.15
#++++++ endof target system +++++

f.close()
ser1.flush()
ser1.close()
ser2.flush()
ser2.close()
