/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "can.h"
#include "dma.h"
#include "spi.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "bsp_can.h"
#include "CAN_receive.h"
#include "BMI088driver.h"
#include "PID.h"
#include "math.h"
#include "CAN_receive.h"

#define FRONT_WHEEL_DISTANCE 0.628  // 前轮到车辆重心的距离 (单位: mm)
#define REAR_WHEEL_DISTANCE 0.440   // 后轮到车辆重心的距离 (单位: mm)
#define MAX_STEERING_ANGLE 30     // �?大转向角度（度）
#define M_PI 3.1415926 
#define MAX_SP 21000  // �?大车速（km/h�?
#define Dwheel  0.144
float vehicle_speed;   // 车�?�，单位 km/h
float turning_radius;   // 转弯半径，单�? m


// 假设车�?�和转向角度通过某种方式获取?
void CalculateAndSendWheelSpeeds(float speed, float angle);
float CalculateTurningRadius(float speed, float angle);

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
PID_TypeDef PID_Example;
float measure = 0;
float target = 0;
extern motor_measure_t motor_chassis[7];
extern uint8_t Fore,Back,Left,Right;
extern  int fputc(int ch);
extern int MAX_SPEED;
extern int SPEED1;
extern int SPEED2;
extern int SPEED3;
extern int SPEED4;
extern uint8_t rx_buf;
extern uint8_t Bluetooth_data;
extern int flag1;
uint8_t A[]={02,02,02,02,02,02,02,02};
extern int Dif; 
extern int flag;
extern int flag2;
extern int flag3;
extern int max();
extern int lim();
extern int limit();
int t_speed=0;
extern uint8_t Rec_Speed[8];
extern int Speed_Num;
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_CAN1_Init();
  MX_USART6_UART_Init();
  MX_SPI1_Init();
  MX_TIM10_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */
    can_filter_init();
	HAL_TIM_Base_Start_IT(&htim10);
//	    while(BMI088_init())
//    {
//        ;
//    }
//	PID_Init(&PID_Example, 9600, 5000, 0,3, 1, 5, 0.3, 0.3, 100, 100, ErrorHandle | Integral_Limit | OutputFilter);
   HAL_Delay(2000); 
	 		CAN_cmd_init();
    __HAL_UART_ENABLE_IT(&huart1, UART_IT_RXNE);  //receive interrupt
    __HAL_UART_ENABLE_IT(&huart1, UART_IT_IDLE);  //idle interrupt
	 __HAL_UART_ENABLE_IT(&huart6, UART_IT_RXNE);  //receive interrupt
    __HAL_UART_ENABLE_IT(&huart6, UART_IT_IDLE);  //idle interrupt
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  CAN_cmd_chassis(0, 0, 0, 0);

  while (1)
  {
	 // CAN_cmd_chassis1(A);
	  
	  if(flag1==1)
	  {
		  flag1=0;
	    if(Bluetooth_data==0xF0)
		 {
		 	flag3=1;
		  }
		  //CAN_cmd_chassis(2000,-2000,2000,-2000);
		  if(flag3==0)
		  {
			  
	  if(Bluetooth_data==0x00)		 
   
	{
		stop:
		
	   flag2=1;
		switch(flag)
     {
		case 1:
			for(int i=1000;t_speed-i>=0;i+=1000) 
              {
				if(flag2==1&&flag1==0)
				{
			    CAN_cmd_chassis(limit(t_speed-i), -limit(t_speed-i),limit(t_speed-i),-limit(t_speed-i));
				HAL_Delay(50);
				t_speed=t_speed-i;
				}
				else
                {t_speed=t_speed-i;
				goto END;}
			  }
			   CAN_cmd_chassis(0,0,0,0);
			  flag=0;flag2=0;break;
	    case 2:
			for(int i=1000;t_speed-i>=0;i+=1000) 
              {
				if(flag2==1&&flag1==0)
				{
			    CAN_cmd_chassis(-limit(t_speed-i), limit(t_speed-i),-limit(t_speed-i),limit(t_speed-i));
				HAL_Delay(50);
				t_speed=t_speed-i;
				}
	          else
                {t_speed=t_speed-i;
				goto END;}
			  }
			   CAN_cmd_chassis(0,0,0,0);
			  flag=0;flag2=0;break;
	    case 3:
			for(int i=1000;t_speed-i>=0;i+=1000) 
              {
				if(flag2==1&&flag1==0)
				{
			     CAN_cmd_chassis(limit(t_speed-Dif-i), -limit(t_speed-i),limit(t_speed-Dif-i),-limit(t_speed-i));
				 HAL_Delay(50);
				t_speed=t_speed-i;
				}
				else
                {t_speed=t_speed-i;
				goto END;}
			  }
			   CAN_cmd_chassis(0,0,0,0);
			  flag=0;flag2=0;break;
	    case 4:
			for(int i=1000;t_speed-i>=0;i+=1000) 
              {
				if(flag2==1&&flag1==0)
				{
			     CAN_cmd_chassis(limit(t_speed-i), -limit(t_speed-Dif-i),limit(t_speed-i),-limit(t_speed-Dif-i));
				 HAL_Delay(50);
					t_speed=t_speed-i;
				}
				else
                {t_speed=t_speed-i;
				goto END;}
			  }
			  CAN_cmd_chassis(0,0,0,0);
			  flag=0;flag2=0;break;			  
	    case 5:
			for(int i=1000;t_speed-i>=0;i+=1000) 
              {
				if(flag2==1&&flag1==0)
				{
			     CAN_cmd_chassis(-limit(t_speed-i), -limit(t_speed-i),-limit(t_speed-i),-limit(t_speed-i));
				 HAL_Delay(50);
					t_speed=t_speed-i;
				}
				else
                {t_speed=t_speed-i;
				goto END;}
			  }
			  CAN_cmd_chassis(0,0,0,0);
			  flag=0;flag2=0;break;	
	    case 6:
			for(int i=1000;t_speed-i>=0;i+=1000) 
              {
				if(flag2==1&&flag1==0)
				{
			     CAN_cmd_chassis(limit(t_speed-i), limit(t_speed-i),limit(t_speed-i),limit(t_speed-i));
				 HAL_Delay(50);
					t_speed=t_speed-i;
				}
				else
                {t_speed=t_speed-i;
				goto END;}
			  }
			  CAN_cmd_chassis(0,0,0,0);
			  flag=0;flag2=0;break;				  
//		//case 2:for(int i=1000;a-i>=0;i+=1000) {CAN_cmd_chassis(-limit(SPEED1-i), limit(SPEED2-i),-limit(SPEED3-i),limit(SPEED4-i));HAL_Delay(100);flag=0;}break;
//		case 3:for(int i=1000;a-i>=0;i+=1000) {CAN_cmd_chassis(limit(SPEED1-Dif-i), -limit(SPEED2-i),limit(SPEED3-Dif-i),-limit(SPEED4-i));HAL_Delay(100);flag=0;}break;
//		case 4:for(int i=1000;a-i>=0;i+=1000) {CAN_cmd_chassis(limit(SPEED1-i), -limit(SPEED2-Dif-i),limit(SPEED3-i),-limit(SPEED4-Dif-i));HAL_Delay(100);flag=0;}break;
//		case 5:for(int i=1000;a-i>=0;i+=1000) {CAN_cmd_chassis(-limit(SPEED1-i), -limit(SPEED2-i),-limit(SPEED3-i),-limit(SPEED4-i));HAL_Delay(100);flag=0;}break;
//		case 6:for(int i=1000;a-i>=0;i+=1000) {CAN_cmd_chassis(limit(SPEED1-i), limit(SPEED2-i),limit(SPEED3-i),limit(SPEED4-i));HAL_Delay(100);flag=0; }break;
    
	 }//ɲ
	 
	}
	 if(Bluetooth_data==0x0A)        
		 { 
			 if(flag==2)
			 {
				 goto stop;
			 }
	
			flag=1;
			 for(int i=t_speed;i<=max();i+=1000)
			 {
				 if(flag==1&&flag1==0)
			  {CAN_cmd_chassis(lim(i,SPEED1), -lim(i,SPEED2),  lim(i,SPEED3), -lim(i,SPEED4));t_speed=i;HAL_Delay(50);}
			  else 
			  {t_speed=i;goto END;}
			 }//ǰ
		 }
	 else if(Bluetooth_data==0x0B)    
		{
	      if(flag!=0)
		  {goto stop;
		  }
			flag=2;
			
			for(int i=t_speed;i<=max();i+=1000)
		 {
			if(flag==2&&flag1==0)
			{CAN_cmd_chassis(-lim(i,SPEED1), lim(i,SPEED2), -lim(i,SPEED3), lim(i,SPEED4));t_speed=i;HAL_Delay(50);}
			 else 
			  {t_speed=i;goto END;}
		 }//��
            
    	}		
	 else if(Bluetooth_data==0x0D)    
		 {
		
			 flag=3;
			 for(int i=t_speed;i<=max();i+=1000)
			 {
				 if(flag==3&&flag1==0)
			 {CAN_cmd_chassis(lim(i,SPEED1-Dif), -lim(i,SPEED2), lim(i,SPEED3-Dif), -lim(i,SPEED4));t_speed=i;HAL_Delay(50);}
			  else 
			  {t_speed=i;goto END;}
			 }
		 }//��
	else if(Bluetooth_data==0x0C)    
		{
	
			flag=4;
			for(int i=t_speed;i<=max();i+=1000)
		 {
			if(flag==4&&flag1==0)
			{CAN_cmd_chassis(lim(i,SPEED1), -lim(i,(SPEED2-Dif)), lim(i,SPEED3), -lim(i,(SPEED4-Dif)));t_speed=i;HAL_Delay(50);}
			else 
			 {t_speed=i;goto END;}
		 }//��
	    }
	else if(Bluetooth_data==0x02)    
		{
			
			flag=5;
			for(int i=t_speed;i<=max();i+=1000)
		 {
			if(flag==5&&flag1==0)
			{CAN_cmd_chassis(-lim(i,SPEED1), -lim(i,SPEED2),  -lim(i,SPEED3), -lim(i,SPEED4));t_speed=i;HAL_Delay(50);}
			else 
			 {t_speed=i;goto END;}
		 }
	 }
	else if(Bluetooth_data==0x03)   
		{
		
			flag=6;
			for(int i=t_speed;i<=max();i+=1000)
		   {
			   if(flag==6&&flag1==0)
		       {CAN_cmd_chassis(lim(i,SPEED1), lim(i,SPEED2),  lim(i,SPEED3), lim(i,SPEED4));t_speed=i;HAL_Delay(50);}
			   else 
			 {t_speed=i;goto END;}
		   }
	    }

		else if(Bluetooth_data==0x08)    
	{
		
		if(SPEED1<21000)
		{
			SPEED1+=1000;
			SPEED2+=1000;
			SPEED3+=1000;
			SPEED4+=1000;
		}
		else
		{
			HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,1);
			HAL_Delay(500);
			HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,0);
		}
	}
		else if(Bluetooth_data==0x05)    
	{
		
		if(SPEED1>0)
		{
			SPEED1-=1000;
			SPEED2-=1000;
			SPEED3-=1000;
			SPEED4-=1000;
		}
		else
		{
			HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,1);
			HAL_Delay(500);
			HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,0);
		}
	}
	
	else if(Bluetooth_data==0x07)    
	{
		
		if(Dif<21000)
		{
			Dif+=1000;
		}
		else
		{
			HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,1);
			HAL_Delay(500);
			HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,0);
		}
	}
	else if(Bluetooth_data==0x04)    
	{
		
		if(Dif>0)
		{
			Dif-=1000;
		}
		else
		{
			HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,1);
			HAL_Delay(500);
			HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,0);
		}
	}
		else if(Bluetooth_data==0x01)    
	{
		CAN_cmd_chassis(0,0,0,0);
         t_speed=0;
	}
  END:
	
    flag2=0;
		  }
		
 
}
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
//	  CAN_cmd_chassis(10000,10000, 10000, 10000);
//	  HAL_Delay(1000);
//	    vehicle_speed = 3.0f;    // 车�?? 60 km/h
//	   turning_radius = 0.05f;   // 假设目标转弯半径�?10�?
//	   CalculateAndSendWheelSpeeds(vehicle_speed, turning_radius);
	  // CAN_cmd_chassis(2000, -21000, 2000, -21000);
//	  CAN_cmd_chassis(15000, -15000, 15000, -15000);
//	  HAL_Delay(3000);
//	  	  CAN_cmd_chassis(-21000, -21000, -21000, -21000);
//	   HAL_Delay(5000);
//	  	  CAN_cmd_chassis(21000, 21000, 21000, 21000);
//	   HAL_Delay(5000);
//	    CAN_cmd_chassis(-15000, +15000, -15000, +15000);
//	  HAL_Delay(3000);
	  
//	  	//ң��
//	if((Fore==0)&&(Back==0))target=0;//δ���ܵ�ǰ������ָ��-->�ٶ����㣬����ԭ��
//	if(Fore==1)
//	{
////		if(distance<50)
////			target--;
////		else
//			target++;
//	}
//	if(Back==1){target--;}
//	CAN_cmd_chassis(
//	PID_Calculate(&PID_Example,motor_chassis[0].ecd,target),
//	PID_Calculate(&PID_Example,motor_chassis[1].ecd,target),
//	PID_Calculate(&PID_Example,motor_chassis[2].ecd,target),
//	PID_Calculate(&PID_Example,motor_chassis[3].ecd,target)
//	);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the CPU, AHB and APB busses clocks
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 6;
  RCC_OscInitStruct.PLL.PLLN = 168;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */
void CalculateAndSendWheelSpeeds(float speed, float turning_radius)
{
    float front_left_speed, front_right_speed, rear_left_speed, rear_right_speed;
    float angular_velocity;
 	float r1,r2;
    // 计算角�?�度 (omega = v / R)
    angular_velocity = (speed / 3.6) / turning_radius;
	r1=turning_radius-(REAR_WHEEL_DISTANCE/2);
	r2=turning_radius+(REAR_WHEEL_DISTANCE/2);
    // 计算前后轮的切向速度
    front_left_speed = angular_velocity * r1/M_PI/Dwheel*6000;
    front_right_speed = angular_velocity * r2/M_PI/Dwheel*6000;
    rear_left_speed = angular_velocity * r1/M_PI/Dwheel*6000;
    rear_right_speed = angular_velocity *  r2/M_PI/Dwheel*6000;

    // 如果车�?�为负（例如倒车），则将切向速度反转
//    if (speed < 0) {
//        front_left_speed = -front_left_speed;
//        front_right_speed = -front_right_speed;
//        rear_left_speed = -rear_left_speed;
//        rear_right_speed = -rear_right_speed;
//    }

    // 限制轮�?�的范围，避免超出最大�?�度
    if (front_left_speed > MAX_SPEED) front_left_speed = MAX_SPEED;
    if (front_right_speed > MAX_SPEED) front_right_speed = MAX_SPEED;
    if (rear_left_speed > MAX_SPEED) rear_left_speed = MAX_SPEED;
    if (rear_right_speed > MAX_SPEED) rear_right_speed = MAX_SPEED;
	
    // 将前后轮的切速度发�?�到CAN总线
    CAN_cmd_chassis(front_left_speed, -front_right_speed, rear_left_speed, -rear_right_speed);
}

float CalculateTurningRadius(float speed, float angle)
{
    // 转向半径计算公式：R = v / tan(θ)
    // 其中v是车速，θ是转向角，单位转换：车�?�从 km/h 转为 m/s
    float turning_radius = (speed / 3.6) / tan(angle * M_PI / 180.0);
    return turning_radius;
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
