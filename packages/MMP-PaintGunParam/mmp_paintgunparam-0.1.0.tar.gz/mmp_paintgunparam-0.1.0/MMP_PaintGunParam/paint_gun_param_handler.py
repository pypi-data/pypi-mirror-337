from CustomModbusClient import CustomModbusClient
import yaml
import logging

logging.basicConfig()
logging.getLogger('pyModbusTCP.client').setLevel(logging.DEBUG)


class PaintGunParamHandler:

    """
    PaintGunParam is used to set the parameters of a paint  gun controller like the MS100 from Carlisle.
    Two types of parameters can be set: Registers and register bits. Write and / or read are possible.
    """

    def __init__(self, timeout=0.03):
        """
        Initialize the PaintGunParam object.

        :param host: The IP address of the paint controller.
        :param port: The port of the paint controller.
        :param timeout: The timeout for the connection to the paint controller.
        """
        self._load_config()
        self.client = CustomModbusClient(host=self.host, port=self.port, auto_open=True, auto_close=True, timeout=timeout, debug=False)
        self.error_message = None
        self._configure_controller()

    # Load the YAML registers file
    def _load_config(self):
        file_path = 'configs.yml'
        with open(file_path, 'r') as file:
            configs = yaml.safe_load(file)
            self.registers = configs["REGISTERS"]
            self.host = configs["IP_ADDRESS"]
            self.port = configs["PORT"]

    def _configure_controller(self):
        """
        Configure the controller with the values from the configs.yml file.
        """
        for name, fields in self.registers.items():
            if fields.get("init"):
                self.set_param(name, fields["value"])

    def powder_on(self):
        """
        Turn the powder on.
        """
        self.set_param("gun_btn_enabled", 1)
        self.set_param("gun_btn_cmd_logic", 1)

    def powder_off(self):
        """
        Turn the powder off.
        """
        self.set_param("gun_btn_enabled", 0)
        self.set_param("gun_btn_cmd_logic", 0)

    def set_param(self, name, value):
        if name not in self.registers:
            print(f"Error: {name} not found in the configs.yml file")
            return None
        
        address = self.registers.get(name)["address"]

        if not self._valid_adress(address):
            print(f"Error: No address found for {name} or adress type is not valid")
            return None
        
        print(f"Full Address for {name} is {address}")

        if self._is_bit_register(address):
            self._write_to_bit_register(address, name, value)
            return None

        self._write_to_register(address, name, [value])  

    def get_param(self, name):
        if name not in self.registers:
            print(f"Error: {name} not found in the configs.yml file")
            return None
        
        reg_address = self.registers.get(name)["address"]

        if reg_address is None:
            print(f"Error: No address found for {name}")
            return None

        read_result = self.client.read_holding_registers(reg_address)

        if read_result != [0]:
            print(f"Successfully read {name} with value {read_result[0]}")
        else:
            print(f"Error reading {name} at address {reg_address}")
            return read_result[0] 

    def _write_to_register(self, reg_address, register_name, value):
        """
        Write a value to a register and confirm the operation.

        :register: The register to write to.
        :value: The value to write.
        :return: True if the write was successful, False otherwise.
        """
        
        # Write the value to the register
        self.client.write_multiple_registers(reg_address, value)

        # Read the value from the register
        read_result = self.client.read_holding_registers(reg_address)

        if read_result == value:
            print(f"Successfully wrote: {value} to register: {reg_address} for: {register_name}")
            return True
        else:
            print(f"Error writing {value} to {register_name} at address {reg_address}")
            return False
        
    def _write_to_bit_register(self, reg_address, register_name, value):
        """
        Write a value to a bit register and confirm the operation.

        :register: The register to write to.
        :value: The value to write.
        :return: True if the write was successful, False otherwise.
        """
        # Register adresse and bit position extraction
        bit_position = self._get_bit_position(reg_address)
        reg_address = int(reg_address)
        print(f"Register Adress is {reg_address}")
        print(f"Bit position is {bit_position}")

        # Read the current value of the register
        reg_value = self.client.read_holding_registers(reg_address)
        current_value = reg_value[0]

        if current_value is not None:
            print(f"Current value of register {reg_address}: {current_value}")

            # Modify the specific bit using bitwise operations
            if value:
                new_value = current_value | (1 << bit_position)  # Set the bit to 1
                self._write_to_register(reg_address, register_name, [new_value])
            else:
                new_value = current_value & ~(1 << bit_position)  # Clear the bit to 0
                self._write_to_register(reg_address, register_name, [new_value])
        else:
            print("Failed to read the holding register.") 

    def _is_bit_register(self, reg_address):
        """
        Check if the register address is a bit register.

        :param reg_address: The register address to check.
        :return: True if the register address is a bit register, False otherwise.
        """
        return isinstance(reg_address, float)
    
    def _get_bit_position(self, reg_address):
        """
        Get the bit position of the register address.
        :param reg_address: The register address to get the bit position from.
        """
        decimal_part = reg_address - int(reg_address)
        return round(decimal_part * 100)
    
    def _valid_adress(self, reg_address):
        """
        Check if the register address is valid.
        :param reg_address: The register address to check.
        :return: True if the register address is valid, False otherwise.
        """
        return isinstance(reg_address, int) or isinstance(reg_address, float)