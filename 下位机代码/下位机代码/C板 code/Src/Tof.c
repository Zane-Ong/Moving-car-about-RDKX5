
#include "usart.h"

extern UART_HandleTypeDef huart6;

 int fputc2(int ch)
{
	HAL_UART_Transmit(&huart6, (uint8_t *)&ch, 1, 0xFFFF);
  return ch;
}

void Get_Distance()
{
	fputc2(0X01);
	fputc2(0X03);
	fputc2(0X00);
	fputc2(0X10);
	fputc2(0X00);
	fputc2(0X01);
	fputc2(0X85);
	fputc2(0XCF);
	
	
}