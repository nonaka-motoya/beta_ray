import serial
import struct 
from serial.tools import list_ports
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import time

start = time.time()

devices = [info.device for info in list_ports.comports()]

ser_texio = None
dev_name = None
for dev in devices:
    
    # @added by motoya
    if dev != '/dev/cu.usbmodemGJV8700871':
        continue
    
    ser = serial.Serial(dev, 9600)
    ser.timeout=0.1
    ser.write("*IDN?\r\n".encode())
    ans = ser.readline()
    if(len(ans)!=0):
        ans = ans.decode().replace("\n", "")
        ans_split = ans.split(",")
        if(ans_split[0]=="TEXIO"):
            ser_texio = ser
            print("Found TEXIO at {0}:{1}".format(dev, ans.replace(",", " ")))
            dev_name = dev
            break
        else:
            ser.close()
    else:
        ser.close()

if(ser_texio==None):
    print("TEXIO oscilloscope was not found!")
    exit(1)

argv = sys.argv
if(len(argv)!=2):
    print("Error: You need to specify the save directory!")
    exit(1)


c = 0
dirname = argv[1]
if(not os.path.exists(dirname)):
    os.mkdir(dirname)

 
ser_texio.write(":RUN\n".encode())
ser_texio.write(":ACQ:RECO 1000\n".encode())
ser_texio.write(":ACQ:RECO?\n".encode())
ans_head = ser_texio.readline()
ser_texio.write(":TRIG:SOUR?\n".encode())
ans_trg = ser_texio.readline().decode().replace("\n", "")


def GetWfm(ch):
    while(1):
        ser_texio.write(":ACQ{0}:MEM?\n".format(ch).encode())
        ans_head = ser_texio.readline().decode().split(";")
        if(len(ans_head)>2):
            break

    leng = int(ans_head[1].split(",")[-1])
    vtrig = float(ans_head[4].split(",")[-1])
    v_div = float(ans_head[12].split(",")[-1])
    v_pos = float(ans_head[13].split(",")[-1])
    s_div = float(ans_head[15].split(",")[-1])
    s_pos = float(ans_head[16].split(",")[-1])

    source_ch = int(ans_head[5].split(",")[-1].replace("CH", ""))
    # print(leng, vtrig, v_div, v_pos, s_div, s_pos)
    #print(ans_head)

    if(source_ch!=ch):
        raise ValueError("channel swap occurred!")

    ans_body_head = ser_texio.read(2)
    fst_bits = struct.unpack("<h",ans_body_head[:2])[0]
    conv = fst_bits&0xff
    endian = None
    # 35 is # (sharp)
    if(conv==35):
        endian = ">"
    else:
        endian = "<"
         
    Ndigit = int(ans_body_head.decode()[1])
    head_leng = ser_texio.read(Ndigit)

    ans_body = ser_texio.read(leng*2+1)[:-1]

    t0 = s_pos
    conv = np.array(struct.unpack("{0}{1}h".format(endian,leng),ans_body), dtype=np.float32)*v_div/25
    t = np.linspace(t0-s_div*5, t0+s_div*5, leng)

    return t, conv, (leng, vtrig, v_div, v_pos, s_div, s_pos)



        
fig, ax1 = plt.subplots()
subc = 0
while(1):

    if(c>=10000):
        end_time = time.time() - start
        print("Good bye!\nproccessing time: {}".format(end_time))
        break

    filename = "{0}/wfm_{1}.txt".format(dirname, c)
    fout = open(filename, "w")
    if(c%10==0):
        print("Progress:", c, " To stop data acquisition, type ctrl+c")

    try:
        

        ser_texio.write(":SING\n".encode())
        while(True):
            ser_texio.write(":ACQ1:STAT?\n".encode())
            ans_head = ser_texio.readline().decode().replace("\n", "")
            if(ans_head=="1"):
                break
            
            subc +=1
            if(subc==10):
                ser_texio.write(":RUN\n".encode())
                subc = 0
        
        t, ch1, info  = GetWfm(1)
        t, ch2, info2 = GetWfm(2)

        leng  = info[0]
        vtrig = info[1]
        v_div_1 = info[2]
        v_pos_1 = info[3]
        s_div_1 = info[4]
        s_pos_1 = info[5]

        v_div_2 = info2[2]
        v_pos_2 = info2[3]
        s_div_2 = info2[4]
        s_pos_2 = info2[5]

        t0 = s_pos_1
    
        vm1, vM1 = v_div_1*(-v_pos_1/v_div_1-4), v_div_1*(-v_pos_1/v_div_1+4)
        vm2, vM2 = v_div_2*(-v_pos_2/v_div_2-4), v_div_2*(-v_pos_2/v_div_2+4)

        for i in range(leng):
            if(i!=leng-1):
                fout.write("{0:.3f}\t{1:.1f}\t{2:.1f}\n".format(t[i]*1e11, ch1[i]*1e3, ch2[i]*1e3))
            else:
                fout.write("{0:.3f}\t{1:.1f}\t{2:.1f}".format(t[i]*1e11, ch1[i]*1e3, ch2[i]*1e3))

        fout.close()

        if(c%10==0):

            ax1.set_title("TEXIO oscilloscope monitor")
            ax1.grid()
            ax1.plot(t*1e11, ch1, color="orange") # @changed by motoya
            ax1.set_ylim(vm1, vM1)
            ax1.set_xlim((t0-s_div_1*5)*1e9, (t0+s_div_1*5)*1e9) # @changed by motoya
            ax1.set_xlabel("time [ns]", fontsize=10)
            ax1.set_ylabel("Ch1 voltage [V]", fontsize=10)
            # ax1.axvline(color="black", linewidth=2)

            if(ans_trg=="CH1"):
                ax1.text((t0+s_div_1*5)*1e9, vtrig, "  trig({0})".format(ans_trg), color="orange")
                ax1.axhline(vtrig, color="orange")

            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            if(ans_trg=="CH2"):
                ax2.text((t0+s_div_2*5)*1e9, vtrig, "  trig({0})".format(ans_trg), color="blue")
                ax2.axhline(vtrig, color="lightblue")
            ax2.set_ylabel('Ch2 voltage [V]') 
            ax2.plot(t*1e9, ch2, color="blue")
            ax2.set_ylim(vm2, vM2)
            #ax2.tick_params(axis='y', labelcolor=color)
            fig.tight_layout()
            plt.pause(0.15)
            ax1.clear()
            ax2.clear()
            ax2.set_visible(False)

        c += 1

    except KeyboardInterrupt:
        fout.close()
        end_time = time.time() - start
        print("Good bye!\nproccessing time: {}".format(end_time))
        if(os.path.exists(filename)):
            os.remove(filename)
        time.sleep(0.1)
        ser_texio.close()
        time.sleep(0.1)
        exit(1)
    except:
        if(not plt.fignum_exists(1)):
            fig, ax1 = plt.subplots()

        print("Reconnect..")
        ser_texio.close()
        time.sleep(1)
        ser_texio = serial.Serial(dev_name, 9600)
        ser_texio.timeout = 0.1
        while(1):
            buf = ser_texio.readline()
            if(len(buf)<2):
                break
        ser_texio.write(":RUN\n".encode())
        ser_texio.write(":TRIG:SOUR?\n".encode())
        ans_trg = ser_texio.readline().decode().replace("\n", "")