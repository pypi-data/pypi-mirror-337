import asyncio
import struct
import time
from aioserial import AioSerial  

class SerialDecoder:
    def __init__(self, port, baud):
        """
        Initialize the SerialDecoder.
        
        :param port: COM port to connect
        :param baud: Baudrate for connection 
        """
        self.port = port
        self.baudrate = baud
        self.serial = AioSerial(port=self.port, baudrate=self.baudrate, timeout=None)
        self._reset_state()
    
    def _reset_state(self):
        self.times = 0
        self.buffer = bytearray()  

        self.frame_count = 0  
        self.last_frame_count = 0  
        self.packet_rate = 0  
        self.start_time = time.time()  
        
        self.device_id = 0
        self.data1 = 0
        self.data2 = 0
        self.battery = 0

    async def read_data(self): 
        try:   
            # 读取直到遇到字节 b'\xcc\xcc'  
            data = await asyncio.wait_for(self.serial.read_until_async(b'\xcc\xcc'), timeout=100)  
            if data : 
                self.buffer.extend(data)  
                result = self._process_buffer() 
                self._update_packet_rate() 
                return result
                
        except asyncio.TimeoutError:  
            print("read data Timeout")
            return None    
    
    def _process_buffer(self): 
        # 准备默认的数据字典
        Data = { 
            'time': self.frame_count, 
            'DeviceID': self.device_id,
            'Battery': self.battery,
            'EMG1': self.data1,
            'EMG2': self.data2
        }
         
        # 检查缓冲区是否有足够的数据（10字节完整帧）
        if len(self.buffer) >= 10:   
            if self.buffer[0] == 204 and self.buffer[1] == 204:  
                
                try:
                    # 解析帧: 设备ID(1B), 数据长度(1B), data1(2B), data2(2B), 电池(1B), 校验和(1B)
                    device_id = self.buffer[2]
                    data_len = self.buffer[3]
                    
                    # 获取data1、data2的原始字节和电池字节用于校验和计算
                    data1_bytes = self.buffer[4:6]
                    data2_bytes = self.buffer[6:8]
                    battery_byte = self.buffer[8]
                    checksum = self.buffer[9]
                    
                    # 解析大端格式的数据
                    data1, = struct.unpack('>h', data1_bytes)
                    data2, = struct.unpack('>h', data2_bytes)
                     
                    if data_len != 6:
                        print(f"[E]Lenth: {data_len}")
                        self.buffer = self.buffer[2:]  # 只移除帧头，继续寻找下一个帧
                        return Data

                    # 正确计算校验和：累加所有单独的字节
                    calculated_checksum = (
                        self.buffer[4]+self.buffer[5]+ 
                        self.buffer[6]+self.buffer[7]+
                        self.buffer[8]
                    ) & 0xFF
                    
                    # 验证校验和
                    if calculated_checksum != checksum:
                        print(f"[E]Checksum: C:{calculated_checksum}, R:{checksum}")
                        self.buffer = self.buffer[2:]  # 只移除帧头，继续寻找下一个帧
                        return Data

                    # 更新类属性
                    self.device_id = device_id
                    self.data1 = data1
                    self.data2 = data2
                    self.battery = battery_byte

                    # 增加帧计数
                    self.frame_count += 1

                    # 更新数据字典
                    Data = { 
                        'time': self.frame_count,
                        'DeviceID': device_id,
                        'Battery': battery_byte,
                        'EMG1': data1,
                        'EMG2': data2
                    }

                    # 从缓冲区移除已处理的帧
                    self.buffer = self.buffer[10:]

                except Exception as e:
                    print(f"err: {e}")
                    self.buffer = self.buffer[2:]  # 移除帧头，继续处理
            else:  
                # 丢弃无效的字节  
                self.buffer.pop(0)  # 移除缓冲区的第一个字节   
        return Data 

    def _update_packet_rate(self):  
        """Update the packet rate calculation."""
        current_time = time.time()  
        elapsed_time = current_time - self.start_time  
        
        if elapsed_time >= 1:  
            self.packet_rate = self.frame_count - self.last_frame_count  
            self.last_frame_count = self.frame_count  
            self.start_time = current_time     

            
    def get_packet_rate(self):        
        """
        Get the current packet rate.
        
        :return: Packets per second
        """
        return self.packet_rate 

    async def set_device_id(self, device_id):  
        """  
        Set the device ID.  
        
        :param device_id: ID value between 0-255  
        :return: True if successful, False otherwise  
        """  
        # Validate ID range  
        if device_id < 0 or device_id > 255:  
            print(f"Device ID must be in range 0-255")  
            return False  
        
        # Build command: cccc0501 + ID (1 byte)  
        id_byte = device_id.to_bytes(1, byteorder='big')  
        command = b'\xcc\xcc\x05\x01' + id_byte  
        
        try:  
            if self.is_open():  
                # Send device ID setting command  
                await self.serial.write_async(command)  
                print(f"Set device ID to: {device_id}")  
                # Wait 100ms for device to process the command  
                await asyncio.sleep(0.1)  
                return True  
            else:  
                print("Device not connected, cannot set device ID")  
                return False  
        except Exception as e:  
            print(f"Failed to set device ID: {str(e)}")  
            return False  

    async def set_sampling_rate(self, rate="250Hz"):  
        """  
        Set the sampling rate.  
        
        :param rate: Sampling rate ("100 Hz", "250 Hz", or "500 Hz")  
        :return: True if successful, False otherwise  
        """  
        rate_map = {  
            "100Hz": b'\xcc\xcc\x02\x01\x05',  
            "250Hz": b'\xcc\xcc\x02\x01\x02',  
            "500Hz": b'\xcc\xcc\x02\x01\x01'  
        }  
        
        if rate not in rate_map:  
            print(f"Invalid sampling rate: {rate}. Must be one of {list(rate_map.keys())}")  
            return False  
        
        try:  
            if self.is_open():  
                # Send sampling rate setting command  
                await self.serial.write_async(rate_map[rate])  
                print(f"Set sampling rate to {rate}")  
                # Wait 100ms for device to process the command  
                await asyncio.sleep(0.1)  
                return True  
            else:  
                print("Device not connected, cannot set sampling rate")  
                return False  
        except Exception as e:  
            print(f"Failed to set sampling rate: {str(e)}")  
            return False  

    async def set_filter_state(self, enable=True):  
        """  
        Enable or disable filtering.  
        
        :param enable: True to enable filtering, False to disable  
        :return: True if successful, False otherwise  
        """  
        filter_map = {  
            False: b'\xcc\xcc\x03\x01\x00',  # Disable filtering  
            True: b'\xcc\xcc\x03\x01\x01'    # Enable filtering  
        }  
        
        try:  
            if self.is_open():  
                # Send filter setting command  
                await self.serial.write_async(filter_map[enable])  
                print(f"Filter state: {'Enabled' if enable else 'Disabled'}")  
                # Wait 100ms for device to process the command  
                await asyncio.sleep(0.1)  
                return True  
            else:  
                print("Device not connected, cannot set filter state")  
                return False  
        except Exception as e:  
            print(f"Failed to set filter state: {str(e)}")  
            return False  

    async def set_wear_detection(self, enable=True):  
        """  
        Enable or disable wear detection.  
        
        :param enable: True to enable wear detection, False to disable  
        :return: True if successful, False otherwise  
        """  
        wear_map = {  
            False: b'\xcc\xcc\x04\x01\x00',  # Disable wear detection  
            True: b'\xcc\xcc\x04\x01\x01'    # Enable wear detection  
        }  
        
        try:  
            if self.is_open():  
                # Send wear detection setting command  
                await self.serial.write_async(wear_map[enable])  
                print(f"Wear detection: {'Enabled' if enable else 'Disabled'}")  
                # Wait 100ms for device to process the command  
                await asyncio.sleep(0.1)  
                return True  
            else:  
                print("Device not connected, cannot set wear detection")  
                return False  
        except Exception as e:  
            print(f"Failed to set wear detection: {str(e)}")  
            return False  

    def close(self):
        """Close the serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()

    def open(self):
        """Open the serial connection."""
        if self.serial and not self.serial.is_open:
            self.serial.open()

    def is_open(self):
        """
        Check if the serial connection is open.
        
        :return: Connection status
        """
        return self.serial.is_open if self.serial else False
 
# async def main():
#     ser = SerialDecoder("COM11",256000)
#     while True:
#         Data = await ser.read_data()  
#         if Data is not None:
#             print(f"data:{Data},sps({ser.get_sps()})")
            

# if __name__ == '__main__':  
#     asyncio.run(main())
