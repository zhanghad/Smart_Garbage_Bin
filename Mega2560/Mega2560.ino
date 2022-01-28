
const int DELAY=10;
int i;

/**
 * 红外物体检测传感器  infrared ray
 */
const int RNUM=8;
const int R[RNUM]={46,47,48,49,50,51,52,53};


/*
 * 满载红外 1
 */
const int RF0_1=30;
const int RF0_2=31;
const int RF1_1=32;
const int RF1_2=33;
const int RF2_1=34;
const int RF2_2=35;
const int RF3_1=36;
const int RF3_2=37;


/**
 * 传送信息
 */
boolean detected;
boolean isfull_0;
boolean isfull_1;
boolean isfull_2;
boolean isfull_3;


void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(115200); //初始化USB串口
  
  for(i=0;i<RNUM;i++){//初始化红外物体检测传感器
    pinMode(R[i], INPUT);
  }
    
  //初始化红外满载检测传感器
  pinMode(RF0_1, INPUT);
  pinMode(RF0_2, INPUT);
  pinMode(RF1_1, INPUT);
  pinMode(RF1_2, INPUT);
  pinMode(RF2_1, INPUT);
  pinMode(RF2_2, INPUT);
  pinMode(RF3_1, INPUT);
  pinMode(RF3_2, INPUT);

}

void loop() {
  // init
  detected=true;
  isfull_0=!(digitalRead(RF0_1) | digitalRead(RF0_2));//1 is full,0 is not
  isfull_1=!(digitalRead(RF1_1) | digitalRead(RF1_2));
  isfull_2=!(digitalRead(RF2_1) | digitalRead(RF2_2));
  isfull_3=!(digitalRead(RF3_1) | digitalRead(RF3_2));
  
//  isfull_0=false;
//  isfull_1=false;
//  isfull_2=false;
//  isfull_3=false;
  

  //红外数据(无遮挡低电平，有遮挡高电平)
  for(i=0;i<RNUM;i++){
    //detected = detected & digitalRead(R[i]);
    Serial.print(digitalRead(R[i]),BIN);
  }
  
  // send message
//  Serial.print(!detected,BIN);//1 is detected,0 is not
  Serial.print(isfull_0,BIN);//1 is full,0 is not
  Serial.print(isfull_1,BIN);
  Serial.print(isfull_2,BIN);
  Serial.print(isfull_3,BIN);
  Serial.print("\n");
  
  delay(DELAY);

}
