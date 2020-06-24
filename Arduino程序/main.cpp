#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <DHT.h>
#include<Adafruit_BMP085.h>
#include<Arduino_FreeRTOS.h>

String comdata = "";

#define DHTPIN 2     //设定2号引脚为数据输入
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

const int LDR_PIN = A0;   //设定电压输出位A0口
float var;                //暂存电压变量
bool MYBOOL=true;            //手动自动，默认自动

Adafruit_BMP085 bmp;


int led_pin[] = {8, 9, 10, 11, 12, 13, 7, 6};  //LED灯的连接的数据引脚
int led_cnt = 8;          //led灯的数量


TaskHandle_t StartTask_Handler;
TaskHandle_t ZongTask_Handler;

void start_task(void* pvParameters);
void zong_task(void* pvParameters);

void setup() {
  dht.begin();

  if (!bmp.begin()) {
	  Serial.println("Could not find a valid BMP085 sensor, check wiring!");
	  while (1) {}
  }
//LED
  for (int i = 0; i < led_cnt; i++)
  {
    pinMode(led_pin[i], OUTPUT);
    digitalWrite(led_pin[i], LOW);
  }
  Serial.begin(9600);
  xTaskCreate(              // 创建开始任务
    start_task,
    "start_task",
    128,
    NULL,
    1,
    &StartTask_Handler);
  vTaskStartScheduler();    // 开启任务调度
}

void loop() {  
}


void start_task(void* pvParameters) {
  taskENTER_CRITICAL();   // 进入临界区
  xTaskCreate(            // 创建总任务
    zong_task,
    "zong_task",
    128,
    NULL,
    2,
    &ZongTask_Handler);

  vTaskDelete(StartTask_Handler);  //删除start_task
  taskEXIT_CRITICAL();    // 退出临界区
}



void zong_task(void* pvParameters) {
  for(;;) {
    delay(1000); 
    while (Serial.available())  
    {
        comdata += char(Serial.read());
        if(comdata == "1" && !MYBOOL)  //打开风机
        {
          digitalWrite(led_pin[4], HIGH);
        }
        else if (comdata == "2" && !MYBOOL) //关闭风机
        {
          digitalWrite(led_pin[4], LOW);
        }
        
        else if(comdata == "3" && !MYBOOL)  //打开除湿
        {
          digitalWrite(led_pin[5], HIGH);
          
        }
        else if (comdata == "4" && !MYBOOL)  //关闭除湿
        {
          digitalWrite(led_pin[5], LOW);
        }
        
        else if(comdata == "5" && !MYBOOL)  //打开灯光
        {
          digitalWrite(led_pin[6], HIGH);
        }
        else if (comdata == "6" && !MYBOOL)  //关闭灯光
        {
          digitalWrite(led_pin[6], LOW);
        }
        
        else if(comdata == "7" && !MYBOOL)  //打开气泵
        {
          digitalWrite(led_pin[7], HIGH);
        }  
        else if (comdata == "8" && !MYBOOL)  //关闭气泵
        {
          digitalWrite(led_pin[7], LOW);
        }
        else if(comdata == "9" && MYBOOL)  //关闭自动
        {
        	MYBOOL=false;
        }
        else if(comdata == "0" && !MYBOOL) //打开自动
        {
        	MYBOOL=true;
        }
        
        comdata = "";
    }
    // DHT11每隔3s更新一次数据
    delay(3000); 
    // 读取温湿度
    float h = dht.readHumidity();   //读取湿度
    float t = dht.readTemperature(); //读取温度
    // 读取失败处理
    if (isnan(h) || isnan(t)) {
      Serial.println(F("Failed to read from DHT sensor!"));
      return;
    }
    // 计算热指数（利用摄氏温度）
    Serial.print(F("T:"));
    Serial.print(t);
    Serial.print(",");
    Serial.print(F("H:"));
    Serial.print(h);
    Serial.print(",");
    //读取光照强度
    var = analogRead(LDR_PIN);
    Serial.print(F("L:"));
    Serial.print(var);
    Serial.print(",");
    //读取气压值
    Serial.print("P:");
    Serial.print(bmp.readSealevelPressure());
    Serial.print(",");
    if (t > 35 || t < 5)
    {
      //LED0灯亮起
      digitalWrite(led_pin[0], HIGH);
    }
    else
    {
      //LED0熄灭
      digitalWrite(led_pin[0], LOW);
      // digitalWrite(led_pin[1], LOW);
    }
    
    if (h > 70 || h < 30)
    {
      //湿度过高或过低，LED1亮起
      digitalWrite(led_pin[1], HIGH);
    }
    else
    {
      //LED1熄灭
      digitalWrite(led_pin[1], LOW);
    }

    if (var > 200 || var < 100)
    {
       //LED2亮起
      digitalWrite(led_pin[2], HIGH);
    }
    else
    {
      digitalWrite(led_pin[2], LOW);
    }

    if (bmp.readSealevelPressure() > 101300 || bmp.readSealevelPressure() < 100000)
    {
      digitalWrite(led_pin[3], HIGH);
    }
    else
    {
      digitalWrite(led_pin[3], LOW);
    }
    if(MYBOOL){
    	if(t>35){
    		digitalWrite(led_pin[4],HIGH);
    	}
    	else{
    		digitalWrite(led_pin[4],LOW);
    	}
    	if(h>70){
    		digitalWrite(led_pin[5],HIGH);
    	}
    	else{
    		digitalWrite(led_pin[5],LOW);
    	}
    	if(var>200){
    		digitalWrite(led_pin[6],HIGH);
    	}
    	else{
    		digitalWrite(led_pin[6],LOW);
    	}
    	if(bmp.readSealevelPressure()>101300){
    		digitalWrite(led_pin[7],HIGH);
    	}
    	else{
    		digitalWrite(led_pin[7],LOW);
    	}
      Serial.print(1);
      Serial.print(",");
    }
    else{
      Serial.print(0);
      Serial.print(",");
    }
    Serial.print(digitalRead(led_pin[4]));
    Serial.print(",");
    Serial.print(digitalRead(led_pin[5]));
    Serial.print(",");
    Serial.print(digitalRead(led_pin[6]));
    Serial.print(",");
    Serial.print(digitalRead(led_pin[7]));
  }
}

// void press_task(void* pvParameters) {
//   for(;;) {
   
//     //读取气压值
//     Serial.print("P:");
//     Serial.print(bmp.readSealevelPressure());
//     if (bmp.readSealevelPressure() > 101300 || bmp.readSealevelPressure() < 100000)
//     {
//       digitalWrite(led_pin[3], HIGH);
//     }
//     else
//     {
//       digitalWrite(led_pin[3], LOW);
//     }
//      vTaskDelay(5000);
//   }
// }

