import math
import numpy as np
#A simple script that solves the Q (MVAR) value for a 3 bus electronic system
#YBUS is your admittance matrix
#InvYBUS is the inverse of each element in YBUs, not to be confused with inverse of YBUS matrix
#we need to divide elements of YBUS for the bus voktage equation 
# this script simulates a 3 bus poer system where bus 1 is the slack  bus, bus 2 is a load bus, bus 3 is a generation bus
# https://www.quora.com/What-is-generator-bus
# https://www.intechopen.com/books/computational-models-in-engineering/power-flow-analysis  #for all equations 
x = -1
Varray = [1.0 + 0j,1+0j, 1.0+0j ] #V1 is slack bus, V2 is load bus, V3 is PV (generator) Bus. we start each bus at 1 pu as a base condition
YBus =  (  [   -12.5j,  10j, 2.5j ], # admittance matrix
		   [10j,   -15j, 5j],  
	   	   [ 2.5j,    5j,  -7.5j ])

YBusNum= np.array((  [   -12.5j,  10j, 2.5j ], # admittance matrix
					 [10j,   -15j, 5j],  
					 [ 2.5j,    5j,  -7.5j ]))

InvYBus = (  [   -12.5j,  10j, 2.5j ], # admittance matrix
			 [10j,   -15j, 5j],  
		     [ 2.5j,    5j,  -7.5j ])
LenYBus = len(YBus)
WidthYBus = len(YBus[0])
PlBus2 = 2+0.5j #P and Q absorbed by load bus 

for item in range(0,LenYBus):
	for item1 in range(0,WidthYBus):
		InvYBus[item][item1] = (YBus[item][item1])**-1 # divide elements of YBUS by 1 because V 
print(InvYBus)
print(YBus)


for num in range(0,5):
	Q3Init = 0
	Varray[x+2] = InvYBus[x+2][x+2]*((np.conj(-PlBus2)/np.conj(Varray[x+2]))-(YBus[x+2][x+1]*Varray[x+1]+YBus[x+3][x+2]*Varray[x+3]))
 #load bus voltage
	for numb in range(0,LenYBus):
		Q3Init = Q3Init + np.absolute(Varray[x+3])*np.absolute(Varray[numb])*np.absolute(YBusNum[numb, 2])*math.sin(np.angle(Varray[x+3])-np.angle(Varray[numb])-np.angle(YBusNum[numb,2]))
	#generation bus reactive power

	Varray[x+3] = InvYBus[x+3][x+3]*((1-Q3Init*1j)/np.conj(Varray[x+3])-(YBus[x+1][x+3]*Varray[x+1]+YBus[x+2][x+3]*Varray[x+2])) #V3 generation bus provides constant power of 1 pu
	
	Varray[x+3] = Varray[x+3]/(np.absolute(Varray[x+3])) #divide by absolute vslue because we are only solving for angle. generation bus maintains constant voltage but different angle (can supply reactive power)



print("The Q Value for Bus 2 is ", 100*Q3Init, "MVAR")
#reactive power absorbed by generation bus 
print("In polar form this is \n",  "V1:", np.absolute(Varray[x+1]), "<", np.angle(Varray[x+1])*180/3.14, "Volts pu", "\n V2", np.absolute(Varray[x+2]), "<", np.angle(Varray[x+2])*180/3.14, "Volts pu", "\n V3", np.absolute(Varray[x+3]), "<", np.angle(Varray[x+3])*180/3.14, "Volts pu")
#viltages of each bus and their angles 