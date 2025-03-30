
from .serial_decoder import SerialDecoder
from .port_manager import COMPortFinder
import os
# cheez_sdk/__init__.py  
import os  
import json  
import sys  
from pathlib import Path  

class ConfigManager:  
    DEFAULT_CONFIG = {  
        "device_ports": {  
            "CheezUSB_VCP": [0x1234, 0x5678],  
            "CheezBLE_VCP": [0x4321, 0x8765]  
        },  
        "default_baudrate": 115200,  
        "log_level": "INFO"  
    }  

    @classmethod  
    def find_config_file(cls):  
        # 查找配置文件的优先级策略  
        search_paths = [  
            # 1. 当前工作目录  
            os.getcwd(),  
            # 2. 用户主目录  
            os.path.expanduser('~'),  
            # 3. 脚本所在目录  
            os.path.dirname(os.path.abspath(sys.argv[0])),  
            # 4. SDK内置默认配置目录  
            os.path.join(os.path.dirname(__file__), 'config')  
        ]  

        config_filenames = [  
            'cheez_config.json',   
            'cheez_sdk_config.json',   
            'config.json'  
        ]  

        for path in search_paths:  
            for filename in config_filenames:  
                full_path = os.path.join(path, filename)  
                if os.path.exists(full_path):  
                    return full_path  
        
        return None  

    @classmethod  
    def load_config(cls, config_path=None):  
        # 如果没有提供路径，则自动查找  
        if config_path is None:  
            config_path = cls.find_config_file()  
        
        # 如果找不到配置文件，使用默认配置  
        if config_path is None:  
            print("使用默认配置：未找到自定义配置文件")  
            return cls.DEFAULT_CONFIG  

        try:  
            with open(config_path, 'r', encoding='utf-8') as f:  
                user_config = json.load(f)  
            
            # 合并默认配置和用户配置  
            config = {**cls.DEFAULT_CONFIG, **user_config}  
            return config  
        
        except json.JSONDecodeError:  
            print(f"配置文件 {config_path} 解析错误，使用默认配置")  
            return cls.DEFAULT_CONFIG  
        except Exception as e:  
            print(f"加载配置文件时发生错误：{e}")  
            return cls.DEFAULT_CONFIG  

    @classmethod  
    def generate_default_config(cls, output_path=None):  
        # 生成默认配置文件  
        if output_path is None:  
            output_path = os.path.join(os.getcwd(), 'cheez_sdk_config.json')  
        
        with open(output_path, 'w', encoding='utf-8') as f:  
            json.dump(cls.DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)  
        
        print(f"默认配置文件已生成：{output_path}")  
        
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
