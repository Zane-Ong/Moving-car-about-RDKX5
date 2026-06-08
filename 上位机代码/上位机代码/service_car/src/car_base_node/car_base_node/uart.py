#!/usr/bin/env python3

import sys
import signal
import serial
import os
import termios
import tty


def signal_handler(signal, frame):
    """捕获 CTRL+C 信号退出程序"""
    print("\n程序已退出")
    sys.exit(0)


def get_key():
    """监听键盘按键（非阻塞模式）"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


def serialTest():
    """串口测试功能"""
    # 列出可用的串口设备
    print("List of enabled UART:")
    os.system('ls /dev/tty[a-zA-Z]*')
    uart_dev = input("请输出需要测试的串口设备名: ")

    # 设置波特率
    baudrate = input("请输入波特率(9600,19200,38400,57600,115200,921600): ")
    try:
        ser = serial.Serial(uart_dev, int(baudrate), timeout=1)  # 1s 超时时间
    except Exception as e:
        print("打开串口失败！错误信息: ", e)
        return -1

    print(f"已成功打开串口 {uart_dev}，波特率 {baudrate}。")
    print("按下任意字母或数字键发送对应的16进制值，按 CTRL+C 退出程序。")
    print("同时，接收到的数据也会显示在屏幕上。")

    try:
        while True:
            # 检查是否有接收的数据
            if ser.in_waiting > 0:
                received_data = ser.read(ser.in_waiting)  # 读取所有待接收的数据
                print(f"接收到: {received_data.hex().upper()}")  # 打印接收到的数据（以16进制形式）

            key = get_key()  # 获取用户按下的按键
            if key == '\x03':  # 如果按下 CTRL+C（ASCII 码值为 3），退出程序
                print("\n检测到 CTRL+C，退出程序")
                break  # 退出循环
            elif key.isalnum():  # 判断是否为字母或数字
                if key.isdigit():  # 如果是数字
                    hex_value = int(key, 10)  # 直接转为十进制数字
                else:  # 如果是字母
                    hex_value = ord(key.upper()) - ord('A') + 0xA  # 将字母转为0x0A到0x0F
                # 发送16进制值（以0X开头）
                ser.write(bytes([hex_value]))  
                print(f"发送: {key}，对应的16进制值: 0X{hex_value:02X}")
            else:
                print(f"无效按键: {repr(key)}，请按字母或数字键。")
    except KeyboardInterrupt:
        # 捕获 CTRL+C 后退出
        print("\n检测到 CTRL+C，退出程序")
    finally:
        ser.close()
        print("串口已关闭")
    return 0


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # 捕获 CTRL+C 信号
    if serialTest() != 0:
        print("串口测试失败！")
    else:
        print("程序结束。")
