import serial #导入模块
import os
import threading
import serial.tools.list_ports
import sqlapi
import time

BOOL=True  #读取标志位

#读数据
def ReadData(ser):
    info=""
    i=0
    global BOOL
    # 循环接收数据，此为死循环，可用线程实现
    while BOOL:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting).decode("gbk")
            if(data=="T"):
                if(i==1):
                    i=0
                    info=info.split(',')
                    print(info)
                    sqlapi.insert_log(str(int(time.time())),info[0].split(":")[1],info[1].split(":")[1],info[2].split(":")[1],info[3].split(":")[1])
                    sqlapi.insert_elog(str(int(time.time())),info[4],info[5],info[6],info[7],info[8])
                info = ""
                i=i+1
            info = info +data

#打开串口
# 端口，Windows上的 COM2
# 波特率，9600
# 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
def DOpenPort(portx,bps,timeout):
    ret=False
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timeout)
        #print(ser)
        #判断是否打开成功
        if(ser.is_open):
           ret=True
           threading.Thread(target=ReadData, args=(ser,)).start()
           #ReadData(ser)
    except Exception as e:
        pass
        print("---异常---：", e)
    else:
        return ser,ret

#关闭串口
def DClosePort(ser):
    global BOOL
    BOOL=False
    ser.close()

#写数据
def DWritePort(ser,text):
    result = ser.write(text.encode("gbk"))  # 写数据
    return result

def main():
    global BOOL
    BOOL=True
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list)==0 :
        print("not find serial port!")
        return;
    ser,rect=DOpenPort("COM2",9600,None)
    if(rect==True):
        print("Runing in COM2")
    return ser

if __name__=="__main__":
    print(main())
