# 智能大棚设计与实现

>HEU嵌入式课程设计==>基于Proteus，Arduino，Flask搭建的智能大棚管理系统

## 系统简介

1.主要内容	
- 硬件嵌入式系统：采用FreeRTOS实时系统和Arduino UNO平台，以及ATMEGA328P微控制器，进行控制，结合DHT11,BMP180等多种传感器进行数据监测，具有自动控制和监测警报功能，能通过前端切换工作模式
- 数据库：基于Python的pymsql库使用MYSQL数据库，能自动创建数据库，表以及存储和查找数据。
- 服务器：基于Python的Flask框架搭建，能控制串口读写
- 前端：具有登录检测，数据查询，远程控制功能

2.采用的工具方法
- Proteus 8.6
- Visual Studio Code
- Arduino
- Python3.8
- MySQL 8.0.15

## 我的报告(爆肝)

<div style="text-align: center;"><h1>智能大棚设计与实现</h1></div>

**摘要：**随着社会的不断发展，传统的农业生产活动方式，诸如农民亲自灌溉，施肥，搭棚保温的方式，这些落后的生产方式已经不能满足现代的经济发展需求，智能化，信息化的农业设计成为了农业发展的趋势。本文设计了一款简单易操作的智能大棚环境监测管理系统，能适用于温室大棚的数据监控和远程硬件操作功能，该系统基于嵌入式系统设计方法，使用了RTOS和Arduino UNO微处理器作为系统的主控芯片，使用了DHT11温湿度传感器，LDR光敏电阻，BMP180气压传感器作为外界环境监测模块，使用了COMPIM进行串口通信，结合Flask服务器框架和MySQL数据库，搭建了Web端和数据库，并优化了前端界面。实现了传感器对环境数据和设备数据进行收集分析处理后，通过串口存储于数据库中，用户通过前端网页实时监测环境数据，并可以控制硬件的状态。该智能大棚监测管理系统，简单易操作，智能化程度高，功能完备，十分适用于农业大棚的监测与管理。

**关键词：**嵌入式；智能大棚；传感器；服务器；Arduino

**一，系统简介**
	为了实现农业温室大棚的自动化，智能化管理，设计了智能大棚监测管理系统，该系统是基于嵌入式设计技术，利用了Arduino Uno平台，虚拟仿真实验环境Proteus软件，实时操作系统FreeRTOS，实现硬件及Arduino虚拟开发和仿真，根据传感器的检测值，进行判断处理，具有自动控制硬件调节功能和警报功能，再结合Python的Flask库搭建服务器端，serial库进行硬件和服务器端信息传输，以及MySQL进行数据存储，实现了对大棚内温度，湿度，光照，气压的监测和记录，以及对硬件设备，如风机，除湿器，照明，气泵的运行状态的监测和管理，能在Web端实时显示环境和设备运行数据和选择自动以及手动控制硬件的模式，能在前端控制硬件运行，能从数据库选择获取不同时间段的数据并以图表形式展示，并且具有登录登出功能。该系统操作简单，不需耗费大量人力物力学习掌握，能满足正常的数据监控和远程管理以及自动管理需要。

**二，需求分析和概要设计**

1.需求分析
在当今智能化的背景下，传统的管理方式已经无法满足对温室大棚的实时监测和控制，尤其是因为当今的温室大棚种植面积普遍较大的，因此，从用户的角度出发，对于大棚的管理，最重要的就是实时监测处理大棚内的温度，湿度，光照和棚内气压等数据，这就需要智能大棚管理系统具有对环境的敏感性和监测的实时性，对于用户而言，他可能还需要了解最近一段时间棚内环境的变换以对未来可能发生的情况进行提前预测，以及了解设备的运行情况做出相应更换等措施，因此需要保存环境和设备运行状况的历史数据。并且系统还应该具有智能处理的功能，当环境变量发生改变，处于不适宜大棚内作物生长的环境时，系统还应该自动控制设备进行相应操作。除此以外，系统需要具有简单易操作，低成本的特点，这样才能减少人工看护和操作的费用，降低成本。对于远程在外的用户，还可以通过云平台进行实时监测和设备控制，从而实现对大棚的智能化，自动化监测管理。

2.概要设计
通过上文对需求的分析，可以得出，智能大棚监测管理系统应该具有数据监控模块，数据传输模块，控制模块，警报模块，数据库模块，服务器模块以及前端模块，系统功能结构框图如图2.1所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624114845.png)
图2.1 系统功能结构框图

2.1 数据监控模块
数据监控是本系统最为重要的一环，数据的获取主要通过三种器件，包括DHT11温湿度传感器，LDR光敏电阻以及BMP180气压传感器，它们在Proteus软件示意图如图2.2所示。数据监控模块的逻辑控制流程图如图2.3所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624114924.png)
图2.2  DHT11(左上),LDR(左下),BMP180(右上)在Proteus中的示意图

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624114940.png)
图2.3 数据监控控制流程图

	由流程图可以看出，数据监控模块主要依靠不断读取三个传感器对温度，湿度，光照，气压的数据信息实现。

2.2 数据传输模块
	数据传输模块包括了，硬件端传输数据到数据库以及服务器端传输数据到硬件两个部分。

2.2.1 硬件到数据库
	硬件端到数据库之间的数据传输主要是为了进行数据存储，因此需要规定硬件写入到串口的格式，并传到服务器端接受，按照规定的格式解析并存储到数据库，硬件到数据库的数据传输流程图如图2.4所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115022.png)
图2.4 硬件到数据库的数据传输流程图

2.2.2 服务器到硬件
	服务器端到硬件的数据传输主要是为了传输前端的控制信息，包括控制选择自动与手动模式，是否开启或关闭相应硬件等控制信息，服务器到硬件的数据传输流程图如图2.5所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115155.png)
图2.5 服务器到硬件的数据传输流程图

2.3 控制模块
	控制模块包括了自动控制模块和手动控制模块。

2.3.1 自动控制模块
	当硬件第一次运行时，默认为自动模式，此时，数据监控时会根据设定的危险范围进行相应的操作，例如当温度超过某个值时，打开风机，否则关闭风机，当湿度超过某个值时，打开除湿器，否则关闭除湿器，自动控制流程图如图2.6所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115306.png)
图2.6 自动控制流程图

2.3.2 手动控制模块
	当服务器端传进来的数据为9时，关闭自动模式，此时硬件运行状态通过之后服务器端传来的数据控制，不同的数据对应不同的操作，手动控制流程图如图2.7所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115328.png)
图2.7 手动控制流程图

2.4 警示灯模块
	为了更好的提醒用户温室大棚内的环境是否正常，设置了警示灯模块，通过不断获取环境数据并和危险区间的上下界进行比较，执行相应的警示灯亮起或熄灭操作，警示灯流程图如图2.8所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115347.png)
图2.8 警示灯流程图

2.5 数据库模块
	数据库模块主要是编写成数据库相关的API，在前端点击，或者自动更新后将会向服务器端请求数据，然后服务器端调用数据库API执行相应的操作，包括：数据库和表的创建，初始用户数据导入，插入数据，按次数搜索最新数据，按时间搜索范围内的数据等等，数据库API结构图如图2.9所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115503.png)
图2.9 数据库模块API结构图

2.6 服务器模块
	对于智能大棚管理系统，服务器的作用主要用于响应前端的请求，以及对串口和数据库的连接和处理，当前端发来不同的请求后，服务器进行相应的操作，包括，返回HTML页面，调用数据库API以及对串口的读取和写入，打开和关闭操作，其具体的功能结构图如图2.10所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115452.png)
图2.10 服务器功能结构图

2.7 前端模块
	智能大棚系统的前端部分主要功能是展示环境数据和设备数据，通过向服务器端请求不同数据，实现对两种数据的最新一条数据和最近一小时数据，最近三小时数据，最近一天数据，最近两天数据的获取，并用折线图，柱状图和表格的形式展示，并且前端会像服务器请求登录状态，如果没有登陆则会自动跳转到登陆页面，保障了用户的信息安全，登录后用户可以通过前端监测数据，并且选择登出，打开或关闭自动模式，打开或关闭风机等硬件设备的功能，除此之外，前端还能每个一段时间自动更新，具体的功能结构图如图2.11所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115534.png)
图2.11 前端功能结构图

**三，系统设计与实现**

1.硬件设计与实现

1.1 硬件总体电路原理图
	硬件电路主要依靠Proteus软件，仿真实现，如图3.1所示。其中包括了DHTT11温湿度传感器用于获取大棚内的温度和湿度；LDR，其阻值随光照强度的增大而减小，将其与一个10K电阻组成分压电路，使得读取模拟IO的电压值可以用于监测大棚内的光照强度；BMP180，是一种高精度的气压传感器，用于监测大棚内气压。D2,D3,D4,D5为警示灯，D6,D7,D8,D9依次模拟风机，除湿器，照明，气泵设备。COMPIM用于串口通信。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115623.png)
图3.1 硬件总体设计

1.2 硬件系统设计
	硬件系统采用免费的实时系统FreeRTOS，其通过创建任务并调度实现系统的主要程序，在智能大棚系统中，硬件系统首先配置一系列IO口，定义了一些全局变量，如传感器的引脚，电压变量，所选择的智能模式，led端口等等，通过start_task()任务创建总任务zong_task()，在总任务内，不断读取串口传来的数据和传感器的数值，并写入串口，传递给服务器。

1.2.1 数据监控与传输
在zong_task()中，程序在延迟3秒后依次读取每个传感器的值，并通过串口传递固定格式的数据，最终传递的数据格式，如图3.2所示，依次分别代表温度，湿度，光强，气压，自动模式，风机状态，除湿器状态，照明状态，气泵状态。读取传感器的函数如下所示。

```cpp
delay(3000); //每隔3s更新一次数据
float h = dht.readHumidity();   //读取湿度
float t = dht.readTemperature(); //读取温度
var = analogRead(LDR_PIN);   //读取光照强度
Serial.print(bmp.readSealevelPressure());  //读取气压值
Serial.print(digitalRead(led_pin[4])); //读取并传输硬件（其一）运行状态
```

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624115737.png)
图3.2 数据传输格式

1.2.2 自动控制和手动控制
	程序定义了一个bool类型的全局变量MYBOOL，用于表示当前模式是自动还是手动，当模式是自动时，串口读入的数据将不能控制硬件状态改变，只能控制模式的改变，此时，硬件系统将根据传感器的值进行自动打开或关闭硬件设备，而当模式是手动时，则只能通过串口读入的值来控制硬件设备的开启与关闭。定义的读入手动控制操作的伪代码如下：

```
While(Serial.available()){
	读取data
	如果为自动模式{
		当data=9时，关闭自动模式
}
如果为手动模式{
	当data=1时，打开风机
当data=2时，关闭风机
当data=3时，打开除湿
当data=4时，关闭除湿
当data=5时，打开灯光
当data=6时，关闭灯光
当data=7时，打开气泵
当data=8时，关闭气泵
当data=0时，切换自动模式
}
}
```

定义的自动控制和警报操作伪代码如下：

```
If(自动模式){
	如果温度异常，警报灯亮，操作风机，否则关闭警报灯和风机
	如果湿度异常，警报灯亮，操作除湿器，否则关闭警报灯和除湿
	如果光强异常，警报灯亮，操作照明，否则关闭警报灯和照明
	如果气压异常，警报灯亮，操作气泵，否则关闭警报灯和气泵
}
```

2.数据库设计与实现
	数据库的连接与操作，主要使用了Python的pymysql库，以及MYSQL数据库，主要实现当服务器连接时，自动查找大棚数据库，如果不存在则自动创建数据库BigPeng和三张数据表users,logs,e_logs,分别记录用户，环境数据，设备数据，并且提供了基于SQL语句的数据插入，数据查询功能，并有良好的异常处理机制。其中环境数据表的创建如下所示：

```python
cur.execute("""
        create table `logs`(
            `log_id` int(11) unsigned unique NOT NULL AUTO_INCREMENT,
            `time` char(20) not null,
            `temperature` float(2),
            `humidity` float(2),
            `light` float(2),
            `pressure` float(2),
            PRIMARY KEY(`log_id`),
            index id(log_id)
        )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;""")
```

数据查找主要有两种模式，一种是select_logs(timestamp),其会根据传入的时间戳，查找大于这一个时间的数据，即可以实现查找最近一小时，最近一天等的数据，具体的实现代码如下：

```python
def select_logs(timestamp):
    conn=connect_BigPeng()
    cur=conn.cursor()
    sql=f"select * from logs where time>={timestamp};"
    try:
        ans=cur.fetchmany(cur.execute(sql))
    except Exception as e:
        conn.close()
        print("数据查找失败！")
        print(e)
        return False
    else:
        conn.close()
        print("数据查找成功")
        return ans
```

第二种是select_newlogs(index),其会根据传入的数量，按照时间倒序，查找最新的index条数据，具体的代码如下：

```python
def select_newlogs(index):
    conn=connect_BigPeng()
    cur=conn.cursor()
    sql=f"select * from logs order by time desc limit 0,{index};"
    try:
        ans=cur.fetchmany(cur.execute(sql))
    except Exception as e:
        conn.close()
        print("数据查找失败！")
        print(e)
        return False
    else:
        conn.close()
        print("数据查找成功")
        return ans
```

3.服务器设计与实现

3.1 串口连接和数据插入
	服务器端的串口操作，主要运用了python的serial库和threading库，serial用于串口通信交互。而threading用于使用多线程循环接受串口数据，并存储到数据库中。
	串口的操作部分，主要功能有，打开串口DopenPort(portx,bps,timeout)，读取数据ReadData(ser)，关闭串口DclosePort(ser)，写入数据DWritePort(ser,text)四个部分。
	当串口打开后，将会自动执行读取数据操作。具体代码如下：

```python
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
```

3.2 服务器框架设计与实现
	该智能大棚系统的服务器端主要使用Python的Flask服务器框架，能够快速接受前端的响应，支持session保存如登录状态等数据，结合之前编写的数据库API以及串口操作函数，能够实现对前端请求数据的获取和传递。其中获取某一时间段的函数如下所示：

```python
@app.route('/getjson/',methods=['GET','POST'])
def getjson():
    H=int(request.form.get('Hour'))
    beforetime=time.strptime((datetime.now()-timedelta(hours=H)).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
    timestamp=int(time.mktime(beforetime))
    try:
        ans=dealdata(sqlapi.select_logs(timestamp))
        #数据处理
    except Exception as e:
        print("Get Json 失败！")
        #print(e)
    else:
        return json.dumps(ans)
```

  由于json不支持时间类型的数据解析，因此每次需要服务器端将获取时间并转换为字符串类型的数据进行传递.

4.前端设计与实现
	前端包含四个页面，即登录页，首页，详细数据页，设备数据页。前端需要导入两个js文件，一个是jQuery,一个是echarts.js，后者主要用于数据图表的显示。
	前端页面具有登录检测功能，如果没有登录，则会自动跳转到登录页面，部分代码如下：

```js
check_session=function(){
            $.get('/check_session/').done(function(ans){
                data=$.parseJSON(ans);
                console.log(data)
                if(data["session"]=="false"){
                    window.location.replace("/login/");
                }
				})
}
```

前端具有数据图表以及按钮实时显示功能，每隔一定时间，将会请求服务器再次更新数据，设置定时更新的代码如下：

```js
        window.onload=function(){
            check_session()
            showdata()
            drawcharts()
            setInterval("showdata()",5000);
            setInterval("drawcharts()",5000);
            setInterval("check_session()",5000);
        }
```

**四，系统测试**

1.硬件运行
当硬件开启后，默认为自动模式，此时如果检测值超过设定的危险值后，警示灯将会点亮，并且运行响应的硬件设备，温度超过范围后自动控制的硬件运行图，如图4.1所示。一切正常时的运行图，如图4.2所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120018.png)
图4.1 温度超过范围后自动控制的硬件运行图

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120203.png)
图4.2 正常运行硬件图

2.服务器运行
当服务器运行后，将会查找BigPeng数据库是否存在，如果不存在，将会自动创建数据库和表，如果存在，则自动连接数据库，如图4.3所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120236.png)
图4.3 服务器正常运行示意图

3.前端运行
当服务器和硬件系统开启后，进入首页将会自动跳转登录页面，如图4.4所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120259.png)
图4.4 登陆页面

输入默认的用户名root和密码123456，即可自动跳转首页，首页上半部分如图4.5所示，下部分如图4.6所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120328.png)
图4.5 首页上部分示意图

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120459.png)
图4.6 首页下部分示意图

此时当服务器第一运行时，串口并没有打开，因此需要点击开始监测按钮才能进行数据记录，按下按钮后，可以看到数据表在实时更新，并且按钮状态已改变，这一将存储到服务器端，不会随刷新而改变，如图4.7所示。并且首页还能控制硬件端的模式和硬件设备的开启与停止，如果点击了关闭自动，并打开风机和气泵，等待几秒后将如图4.8所示，对应的硬件状态如图4.9所示

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120512.png)
图4.7 开启实时监测

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120524.png)
图4.8 关闭了自动模式打开风机气泵示意图

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120538.png)
图4.9 对应打开风机和气泵的硬件状态图

通过点击导航栏，可以跳转到详细数据页面，里面可以显示最近三小时，最近一天和最近两天的数据，如图4.10所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120700.png)
图4.10 详细数据页面

再点击导航栏上的设备详情，即可跳转设备数据页面，同样可以查看最近三小时，最近一天和最近两天的数据，如图4.11所示。

![](https://cdn.jsdelivr.net/gh/Justlovesmile/CDN2/post/20200624120715.png)
图4.11 设备数据页

**五，总结**
通过对智能大棚监测管理系统的设计，我们团队实现了对系统的全部预期目标，不仅能实时监控环境数据，还能监控硬件运行状态数据，并存储到数据库，并且通过不懈努力，前端页面具有高效的实时性和动态效果，能定时获取数据实时更新数据，前端也会根据数据的不同发生相对应的改变，在实验过程中也遇到了很多问题，但是在查阅了很多文档后，问题都得到了解决，目前需要改进的地方是，硬件端的传感器数量较少，能够实现的功能可以继续增加，其次是前端的数据更新仍需要5到10秒中时间，当点击了打开硬件设备后需要等待较长时间才会更新。这次智能大棚监测管理系统的设计，让我受益匪浅，希望以后的我，能将它继续完善。