/**
  ******************************************************************************
  * File Name          : TIM.c
  * Description        : This file provides code for the configuration
  *                      of the TIM instances.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "tim.h"

/* USER CODE BEGIN 0 */
#include "struct_typedef.h"
#include "BMI088driver.h"
#include "CAN_receive.h"
#include "stm32f4xx_it.h"
fp32 gyro[3], accel[3], temp;
extern  motor_measure_t motor_chassis[7];
typedef struct {
    float x;
    float y;
    float z;
} GyroData;
volatile float angle_x = 0.0;
volatile float angle_y = 0.0;
volatile float angle_z = 0.0;
extern  int fputc(int ch);
extern  int fputc1(int ch);

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM10) { // ??????????
//        BMI088_read(gyro, accel, &temp);
//        
//        const float sampling_rate = 100.0;
//        const float delta_t = 1.0 / sampling_rate;
//        
//        angle_x += gyro[0] * delta_t;
//        angle_y += gyro[1] * delta_t;
//        angle_z += gyro[2] * delta_t;
		fputc1(0xFF);
		fputc(motor_chassis[0].ecd);
		fputc(motor_chassis[2].ecd);
	    fputc(motor_chassis[1].ecd);
		fputc(motor_chassis[3].ecd);
//		for(int i=0;i<4;i++)
//	{
////		uint16_t temp;
////		if(motor_chassis[i].ecd>21000)
////		{
////			temp=0xFFFF-motor_chassis[i].ecd;
////			fputc(temp);
////		}
////		else
//	    fputc(motor_chassis[i].ecd);
//	}
	//fputc(Distance);
//	HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,1);
		
		
        
    }
}
/* USER CODE END 0 */

TIM_HandleTypeDef htim10;

/* TIM10 init function */
void MX_TIM10_Init(void)
{

  htim10.Instance = TIM10;
  htim10.Init.Prescaler = 1000;
  htim10.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim10.Init.Period = 8400;
  htim10.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim10.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim10) != HAL_OK)
  {
    Error_Handler();
  }

}

void HAL_TIM_Base_MspInit(TIM_HandleTypeDef* tim_baseHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(tim_baseHandle->Instance==TIM10)
  {
  /* USER CODE BEGIN TIM10_MspInit 0 */

  /* USER CODE END TIM10_MspInit 0 */
    /* TIM10 clock enable */
    __HAL_RCC_TIM10_CLK_ENABLE();

    __HAL_RCC_GPIOF_CLK_ENABLE();
    /**TIM10 GPIO Configuration
    PF6     ------> TIM10_CH1
    */
    GPIO_InitStruct.Pin = GPIO_PIN_6;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    GPIO_InitStruct.Alternate = GPIO_AF3_TIM10;
    HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

    /* TIM10 interrupt Init */
    HAL_NVIC_SetPriority(TIM1_UP_TIM10_IRQn, 1, 0);
    HAL_NVIC_EnableIRQ(TIM1_UP_TIM10_IRQn);
  /* USER CODE BEGIN TIM10_MspInit 1 */

  /* USER CODE END TIM10_MspInit 1 */
  }
}

void HAL_TIM_Base_MspDeInit(TIM_HandleTypeDef* tim_baseHandle)
{

  if(tim_baseHandle->Instance==TIM10)
  {
  /* USER CODE BEGIN TIM10_MspDeInit 0 */

  /* USER CODE END TIM10_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_TIM10_CLK_DISABLE();

    /**TIM10 GPIO Configuration
    PF6     ------> TIM10_CH1
    */
    HAL_GPIO_DeInit(GPIOF, GPIO_PIN_6);

    /* TIM10 interrupt Deinit */
    HAL_NVIC_DisableIRQ(TIM1_UP_TIM10_IRQn);
  /* USER CODE BEGIN TIM10_MspDeInit 1 */

  /* USER CODE END TIM10_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */

/* USER CODE END 1 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
