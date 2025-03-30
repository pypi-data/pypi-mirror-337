import asyncio  
import struct  
import time  
from aioserial import AioSerial  
import logging  

class SerialDecoder:  
    def __init__(self, port, baud, log_level=logging.INFO):  
        """  
        Initialize the SerialDecoder.  
        
        :param port: COM port to connect  
        :param baud: Baudrate for connection  
        :param log_level: Logging level  
        """  
        # Configure logging  
        logging.basicConfig(  
            level=log_level,  
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  
        )  
        self.logger = logging.getLogger(__name__)  
        
        self.port = port  
        self.baudrate = baud  
        self.serial = AioSerial(port=self.port, baudrate=self.baudrate, timeout=None)  
        
        # Reset internal state  
        self._reset_state()  
    
    def _reset_state(self):  
        """Reset internal state variables."""  
        self.times = 0  
        self.buffer = bytearray()   
        self.frame_count = 0  
        self.start_time = time.time()  
        self.last_frame_count = 0  
        self.packet_rate = 0  
         
        self.device_id = 0  
        self.data1 = 0  
        self.data2 = 0  
        self.battery = 0  

    async def read_data(self):   
        """  
        Asynchronously read and process serial data.  
        
        :return: Decoded data dictionary or None  
        """  
        try:   
            # Read until marker bytes are found  
            data = await asyncio.wait_for(self.serial.read_until_async(b'\xcc\xcc'), timeout=1)   
            if data :   
                self.buffer.extend(data)   
                result = self._process_buffer()  
                self._update_packet_rate()   
                return result  
                
        except asyncio.TimeoutError:  
            self.logger.warning("Serial read timeout")  
            return None  
        except Exception as e:  
            self.logger.error(f"Error reading serial data: {e}")  
            return None  
    
    def _process_buffer(self):  
        """  
        Process the internal buffer and extract data.  
        
        :return: Data dictionary  
        """  
        default_data = {   
            'time': self.frame_count,   
            'DeviceID': self.device_id,  
            'EMG1': self.data1,  
            'EMG2': self.data2,  
            'Battery': self.battery  
        }  
          
        if len(self.buffer) >= 10:   
            if self.buffer[0] == 204 and self.buffer[1] == 204:  
                try:  
                    # Unpack frame: device_id(1B), data_len(1B), data1(2B), data2(2B), battery(1B), checksum(1B)  
                    device_id = self.buffer[2]  
                    data_len = self.buffer[3]   
                    data1_bytes = self.buffer[4:6]  
                    data2_bytes = self.buffer[6:8]  
                    battery_byte = self.buffer[8]  
                    checksum = self.buffer[9]  
                     
                    data1, = struct.unpack('>h', data1_bytes)  
                    data2, = struct.unpack('>h', data2_bytes)  
                     
                    if data_len != 6:  
                        self.logger.warning(f"Invalid data length: {data_len}")  
                        self.buffer = self.buffer[2:]  
                        return default_data  
   
                    calculated_checksum = (  
                        self.buffer[4]+self.buffer[5]+   
                        self.buffer[6]+self.buffer[7]+  
                        self.buffer[8]  
                    ) & 0xFF  
                    
                    # Verify checksum  
                    if calculated_checksum != checksum:  
                        self.logger.warning(f"Checksum mismatch. Calculated: {calculated_checksum}, Received: {checksum}")  
                        self.buffer = self.buffer[2:]  
                        return default_data  
   
                    # Update internal state  
                    self.device_id = device_id  
                    self.data1 = data1  
                    self.data2 = data2  
                    self.battery = battery_byte   
                    self.frame_count += 1  
   
                    # Return processed data  
                    return {   
                        'time': self.frame_count,  
                        'DeviceID': device_id,  
                        'EMG1': data1,  
                        'EMG2': data2,  
                        'Battery': battery_byte  
                    }  
   
                except Exception as e:  
                    self.logger.error(f"Data processing error: {e}")  
                    self.buffer = self.buffer[2:]   
            else:   
                self.buffer.pop(0)  
        return default_data   

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