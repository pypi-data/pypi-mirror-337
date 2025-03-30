from .serial_decoder import SerialDecoder  
from .port_manager import COMPortFinder  
import os  

class CheezSDK:  
    def __init__(self, config_path=None):  
        """  
        Initialize the Cheez SDK with optional custom config path.  
        
        :param config_path: Path to custom configuration file (optional)  
        """  
        # Use default config if not provided  
        if config_path is None:  
            config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json')  
        
        self.port_manager = COMPortFinder(config_path)  
        self._serial_decoder = None  
    
    def list_ports(self, verbose=False):  
        """  
        List available COM ports.  
        
        :param verbose: If True, print detailed port information  
        :return: List of available ports  
        """  
        return self.port_manager.get_ports_info(verbose)  
    
    def find_devices(self, *device_names):  
        """  
        Find specific device ports.  
        
        :param device_names: Names of devices to find (e.g., 'CheezUSB_VCP', 'CheezBLE_VCP')  
        :return: List of matching COM ports  
        """  
        return self.port_manager.find_ports(*device_names)  
    
    def connect(self, port=None, baudrate=115200):  
        """  
        Connect to a serial device.  
        
        :param port: COM port to connect (auto-detect if None)  
        :param baudrate: Baudrate for connection  
        :return: SerialDecoder instance  
        """  
        # If no port specified, try to auto-detect  
        if port is None:  
            ports = self.find_devices("CheezUSB_VCP", "CheezBLE_VCP")  
            if not ports:  
                raise ValueError("No compatible devices found")  
            port = ports[0]  
        
        self._serial_decoder = SerialDecoder(port, baudrate)  
        return self._serial_decoder  
    
    def disconnect(self):  
        """  
        Disconnect the current serial connection.  
        """  
        if self._serial_decoder:  
            self._serial_decoder.close()  
            self._serial_decoder = None  
