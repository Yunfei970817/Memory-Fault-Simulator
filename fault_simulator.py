# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 23:22:38 2020

@author: boxuanl
"""

from march_test import March_test

memory = []
for i in range(4):
    memory.append("")
print("Initial Memory : ",memory)
i_m=memory.copy()

import csv
csv_file=csv.reader(open(r'fault_list_ULF2_cc.csv','r'))
fault_list = []
temp = []
for line in csv_file:
    temp.append(line)
for i in range(1, len(temp), 2):
    fault_list.append([temp[i], temp[i+1]])

#fault_list = [[['TFs', '0', '0', '1', 'w0', '1', 'NA', 'NA', '0','0'], ['SAFs',	'0', '0', 'NA',	'w1', '0', 'NA', 'NA', '0', '0']]]
#fault_list = fault_list[0:5]

fault_report = open('fault_report.txt', 'w')  
fault_coverage = []
filereader = open('march_test.txt', 'r')
f=filereader.readlines()
for (line_num,line) in enumerate(f):
    current_type1 = ''
    current_subtype1 = ''
    current_type2 = ''
    current_subtype2 = ''
    count = 1
    f_count = 0
    f_count_p = 0
    for fault in fault_list:
        fault[0][2] = int(fault[0][2])
        fault[0][5] = int(fault[0][5])
        fault[1][2] = int(fault[1][2])
        fault[1][5] = int(fault[1][5])
        print("fault is now", fault)
        memory = i_m.copy()
        march_line = line.strip().split(",")
        if ((fault[0][0] != current_type1) or (fault[0][1] != current_subtype1) or (fault[1][0] != current_type2) or (fault[1][1] != current_subtype2)):
            if (current_type1 != ''):
                print("============fault coverage for subtype", current_type1, current_subtype1, " ", current_type2, current_subtype2, "is", f_count, "/", count, "============")
                fault_report.write("============fault coverage for subtype" + current_type1 + current_subtype1 + " " + current_type2 + current_subtype2 + "is" + str(f_count) + "/" + str(count) + "============\n")
                fault_coverage.append([current_type1 + current_subtype1, current_type2 + current_subtype2, f_count, count])
            count = 1
            f_count = 0
            f_count_p = 0
            current_type1 = fault[0][0]
            current_subtype1 = fault[0][1]
            current_type2 = fault[1][0]
            current_subtype2 = fault[1][1]
        else:
            count = count + 1
        print("------------------ fault introduced: ", fault[0][0], fault[0][1], " and ", fault[1][0], fault[1][1], "------------------")
        for march_element in march_line:
            print("march element is : ", march_element)
            f_count = March_test(march_element,memory,fault,line_num, f_count)
            if(f_count != f_count_p):
                f_count_p = f_count_p + 1
                break
            print("memory is now: ", memory)
        if (fault == fault_list[-1]):       #print fault coverage for last fault in the list 
            print("============fault coverage for subtype", current_type1, current_subtype1, " ", current_type2, current_subtype2, "is", f_count, "/", count, "============")
            fault_report.write("============fault coverage for subtype" + current_type1 + current_subtype1 + " " + current_type2 + current_subtype2 + "is" + str(f_count) + "/" + str(count) + "============\n")
            fault_coverage.append([current_type1 + current_subtype1, current_type2 + current_subtype2, f_count, count])
fault_report.close()
print (fault_coverage)
with open('coverage_ULF2_cc.csv', 'w', newline='') as cover_table:
    csv_write = csv.writer(cover_table)
    fp1 = "CFidUP0"
    temp = 0
    line = []
    line.append("FP1/FP2")
    line.append(fp1)
    for comb in fault_coverage[1:]:
        if (comb[0] == "CFidUP1"):           
            csv_write.writerow(line)
            line.clear()
            break
        else:
            line.append(comb[1])
                
    line.append(fp1)
    for comb in fault_coverage:
        if (comb[0] == fp1):           
            line.append(str(comb[2])+"%"+str(comb[3]))           
        else:           
            csv_write.writerow(line)
            temp = temp + 1
            line.clear()
            fp1 = comb[0]
            line.append(fp1)
            for i in range (temp):
                line.append("")
            line.append(str(comb[2])+"%"+str(comb[3]))

    
        


