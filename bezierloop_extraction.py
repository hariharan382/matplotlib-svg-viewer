import xml.etree.ElementTree as ET
import re
import numpy as np
from tkinter import *
from sympy import symbols
import matplotlib.pyplot as plt

plt.axis([0,1000,0,1000])
plt.axis('on')
plt.grid(True)
dy,dx=50,50
for x in np.arange(0,1000,dx):
    for y in np.arange(0,1000,dy):
        plt.scatter(x,y,s=1,color='lightgray')

with open('absolute.svg') as f:
    content=f.read()

tree = ET.parse('absolute.svg')
root=tree.getroot()
arr=[]

for child in root.iter():
    arr.append(child.attrib)
line=arr[4]['d']



def discretize(m):
    m = re.split(r'([A-Y])', m)
    temp_arr = []
    for i in np.arange(-1, len(m), 2):

        temp = str(m[i]) + str(m[i + 1])
        temp_arr.append(temp)
    del (temp_arr[0])
    return  temp_arr



def M_splitter(main_arr):
    empty_list = []

    for i in main_arr:
        if 'M' in i:
            empty_list.append(i)
        else:
            empty_list[-1]=str(empty_list[-1])+" " +str(i)
    return empty_list

def bezier(p):
    #print("bezier---- invoked")
    #print("===============================")
    #print(p)

    t=symbols('t')
    x = (float(p[0][0]) * (1 - t) ** 3 + float(p[1][0]) * 3 * t * (1 - t) ** 2 + float(p[2][0]) * 3 * t ** 2 * (1 - t) + float(p[3][0]) * t ** 3)
    y = (float(p[0][1]) * (1 - t) ** 3 + float(p[1][1]) * 3 * t * (1 - t) ** 2 + float(p[2][1]) * 3 * t ** 2 * (1 - t) + float(p[3][1]) * t ** 3)
    #print("-------------")
    step=0.05
    for i in np.arange(0,1,step):
        plt.plot([x.subs(t,i),x.subs(t,i+step)],[y.subs(t,i),y.subs(t,i+step)])

        #print("x1,y1:",x.subs(t,i),"  ",y.subs(t,i),"   ","x2,y2:",x.subs(t,i+step),"  ",y.subs(t,i+step),"   ")

main_arr=discretize(line)

final_array=M_splitter(main_arr)
#c=code_splitter(final_array[0])


def bezier_array(arr):
    final_arr=[]
    start_arr=[]
    bezier_arr = []
    current_ptr = [0,0]
    temp=[]
    code=discretize(arr)
    #print(code)
    for i in code:
        if 'M' in i:
            #print(i)
            #print("move '''''''''''''''''''")
            start_arr=[float(i.split()[1].split(',')[0]),float(i.split()[1].split(',')[1])]
            current_ptr=[float(i.split()[1].split(',')[0]),float(i.split()[1].split(',')[1])]
            #print("currentpoint --->    first_point :   ", current_ptr[0], "   second point:   ", current_ptr[1])

            continue
        if 'V' in i:
            #print(i)
            #print("vertical=============")
            #plt.plot([current_ptr[0],current_ptr[0]],[current_ptr[1],float(current_ptr[1])+float(i.split()[1])])
            if 'Z' in i:
                final_arr = [ current_ptr[0],float(i.split()[-2])]
                temp.append([[current_ptr[0], current_ptr[1]],
                             [(3 * current_ptr[0] + 1 * current_ptr[0]) / 4,
                              (3 * current_ptr[1] + 1 * float(i.split()[-2])) / 4],
                             [(1 * current_ptr[0] + 3 * current_ptr[0]) / 4,
                              (1 * current_ptr[1] + 3 * float(i.split()[-2])) / 4],
                             [current_ptr[0], float(i.split()[-2])]])
                #current_ptr[1] = float(i.split()[-2])

            else:
                temp.append([[current_ptr[0],current_ptr[1]],
                         [(3*current_ptr[0]+1*current_ptr[0])/4,(3*current_ptr[1]+1*float(i.split()[-1]))/4],
                         [(1*current_ptr[0]+3*current_ptr[0])/4,(1*current_ptr[1]+3*float(i.split()[-1]))/4],
                         [current_ptr[0],float(i.split()[-1])]])
                current_ptr[1] = float(i.split()[-1])
            #print("currentpoint --->    first_point :   ", current_ptr[0], "   second point:   ", current_ptr[1])
        if 'H' in i:
            # print(i)
            # print("Horizontal ------")
            # plt.plot([current_ptr[0], float(current_ptr[0])+ float(i.split()[1])],[current_ptr[1], float(current_ptr[1])])
            if 'Z' in i:
                print(i.split())
                print("Z is present in the HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
                final_arr = [ float(i.split()[-2]),current_ptr[1]]
                temp.append([[current_ptr[0], current_ptr[1]],
                             [(3 * current_ptr[0] + 1 * float(i.split()[-2])) / 4,
                              (3 * current_ptr[1] + 1 * current_ptr[1]) / 4],
                             [(1 * current_ptr[0] + 3 * float(i.split()[-2])) / 4,
                              (1 * current_ptr[1] + 3 * current_ptr[1]) / 4],
                             [float(i.split()[-2]), current_ptr[1]]])
                #current_ptr[0] = float(i.split()[-2])
            else:
                temp.append([[current_ptr[0], current_ptr[1]],
                         [(3*current_ptr[0] + 1*float(i.split()[-1])) / 4, (3*current_ptr[1] + 1*current_ptr[1]) / 4],
                         [(1*current_ptr[0] + 3*float(i.split()[-1])) / 4, (1*current_ptr[1] + 3*current_ptr[1]) / 4],
                         [float(i.split()[-1]),current_ptr[1]]])
                current_ptr[0] = float(i.split()[-1])
            #print("currentpoint --->    first_point :   ", current_ptr[0], "   second point:   ", current_ptr[1])
        if 'L' in i:
            #print(i)
            #print("LIne ------")

            if 'Z' in i:
                final_arr = [float(i.split()[-2].split(',')[0]), float(i.split()[-2].split(',')[1])]
                print("Z is present in the Line")
                for j in range(len(i.split()) - 2):
                    temp.append([[current_ptr[0], current_ptr[1]],
                                    [(3*current_ptr[0] + 1*float(i.split()[1 + j].split(',')[0])) / 4,
                                     (3*current_ptr[1] + 1*float(i.split()[1 + j].split(',')[1])) / 4],
                                    [(1*current_ptr[0] + 3*float(i.split()[1 + j].split(',')[0])) / 4,
                                     (1*current_ptr[1] + 3*float(i.split()[1 + j].split(',')[1])) / 4],
                                    [float(i.split()[1 + j].split(',')[0]), float(i.split()[1 + j].split(',')[1])]])
                    current_ptr=[float(i.split()[1+j].split(',')[0]),float(i.split()[1+j].split(',')[1])]

                #print("currentpoint --->    first_point :   ", current_ptr[0], "   second point:   ", current_ptr[1])

            else:

                for j in range(len(i.split()) - 1):
                    temp.append([[current_ptr[0], current_ptr[1]],
                                [(3*current_ptr[0] + 1*float(i.split()[1 + j].split(',')[0])) / 4,
                                 (3*current_ptr[1] + 1*float(i.split()[1 + j].split(',')[1])) / 4],
                                [(1*current_ptr[0] + 3*float(i.split()[1 + j].split(',')[0])) / 4,
                                 (1*current_ptr[1] + 3*float(i.split()[1 + j].split(',')[1])) / 4],
                                [float(i.split()[1 + j].split(',')[0]), float(i.split()[1 + j].split(',')[1])]])
                    current_ptr = [float(i.split()[1+j].split(',')[0]), float(i.split()[1+j].split(',')[1])]

                current_ptr=[float(i.split()[-1].split(',')[0]), float(i.split()[-1].split(',')[1])]
                #print("currentpoint --->    first_point :   ", current_ptr[0], "   second point:   ", current_ptr[1])
        if 'C' in i:
           #print(i)
           #print("Bezier bezier bezier .............................")

           if 'Z' in i:
                final_arr = [float(i.split()[-2].split(',')[0]), float(i.split()[-2].split(',')[1])]

                for k in range(0, int(((len(i.split()) - 2) / 3))):
                    if k == 0:
                        temp.append([[current_ptr[0], current_ptr[1]],
                       [i.split()[k + 1].split(',')[0], i.split()[k + 1].split(',')[1]],
                       [i.split()[k + 2].split(',')[0], i.split()[k + 2].split(',')[1]],
                       [i.split()[k + 3].split(',')[0], i.split()[k + 3].split(',')[1]]])

                    if k != 0:
                        temp.append([[i.split()[3*k].split(',')[0], i.split()[3*k].split(',')[1]],
                       [i.split()[3 * k + 1].split(',')[0], i.split()[k + 1].split(',')[1]],
                       [i.split()[3 * k + 2].split(',')[0], i.split()[k + 2].split(',')[1]],
                       [i.split()[3 * k + 3].split(',')[0], i.split()[k + 3].split(',')[1]]])



                #print("currentpoint --->    first_point :   ", current_ptr[0], "   second point:   ", current_ptr[1])

           else:
                for k in range(0, int(((len(i.split()) - 1) / 3))):
                    if k == 0:
                        temp.append([[current_ptr[0], current_ptr[1]],
                             [i.split()[k + 1].split(',')[0], i.split()[k + 1].split(',')[1]],
                             [i.split()[k + 2].split(',')[0], i.split()[k + 2].split(',')[1]],
                             [i.split()[k + 3].split(',')[0], i.split()[k + 3].split(',')[1]]])

                    if k != 0:
                        temp.append([[i.split()[3*k].split(',')[0], i.split()[3*k].split(',')[1]],
                        [i.split()[3 * k + 1].split(',')[0], i.split()[3*k + 1].split(',')[1]],
                        [i.split()[3 * k + 2].split(',')[0], i.split()[3*k + 2].split(',')[1]],
                        [i.split()[3 * k + 3].split(',')[0], i.split()[3*k + 3].split(',')[1]]])
                #print("i is ----->   ",i)
                current_ptr = [float(i.split()[-1].split(',')[0]), float(i.split()[-1].split(',')[1])]
                #print("currentpoint --->    first_point :   ", current_ptr[0], "   second point:   ", current_ptr[1])
    print("final array is   ", final_arr)
    print("Start array is   ", start_arr)

    temp.append([[float(final_arr[0]),float(final_arr[1])],
                [(3*float(final_arr[0])+1*start_arr[0])/4,(3*float(final_arr[1])+1*start_arr[1])/4],
                [(1*float(final_arr[0])+3*start_arr[0])/4,(1*float(final_arr[1])+3*start_arr[1])/4],
                [start_arr[0],start_arr[1]]])



    bezier_arr.append(temp)
    return(bezier_arr)

#print(final_array[0])
#p=bezier_array(final_array[0])
#print(type(p))
#bezier(p[0][0])



for i in range(len(final_array)):
    print(final_array[i])
    q=bezier_array(final_array[i])


    #print(q[0][0])
    for j in q[0]:
        try:
            bezier(j)
            #print("+")
        except IndexError:
            print("------")
            continue
    q.clear()

#arr=[[0,0],[250,250],[500,500],[750,750]]
#bezier(arr)
plt.show()
#print(p[0][0][0])










