from pyModbusTCP.client import ModbusClient
import struct

READ_HOLDING_REGISTERS = 0x03
MB_RECV_ERR = 4

class CustomModbusClient(ModbusClient):
    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30, debug=False, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout, debug, auto_open, auto_close)

    def read_holding_registers(self, reg_addr, reg_nb=1):
        """Modbus function READ_HOLDING_REGISTERS (0x03).

        :param reg_addr: register address (0 to 65535)
        :type reg_addr: int
        :param reg_nb: number of registers to read (1 to 125)
        :type reg_nb: int
        :returns: registers list or None if fail
        :rtype: list of int or None
        """
        # check params
        if not 0 <= int(reg_addr) <= 0xffff:
            raise ValueError('reg_addr out of range (valid from 0 to 65535)')
        if not 1 <= int(reg_nb) <= 125:
            raise ValueError('reg_nb out of range (valid from 1 to 125)')
        if int(reg_addr) + int(reg_nb) > 0x10000:
            raise ValueError('read after end of modbus address space')
        # make request
        try:
            tx_pdu = struct.pack('>BHH', READ_HOLDING_REGISTERS, reg_addr, reg_nb)
            rx_pdu = self._req_pdu(tx_pdu=tx_pdu, rx_min_len=3)
            # extract field "byte count"
            byte_count = rx_pdu[1]
            # print(byte_count)
            # frame with regs value
            f_regs = rx_pdu[2:-1]
            # check rx_byte_count: buffer size must be consistent and have at least the requested number of registers
            if byte_count < 2 * reg_nb or byte_count != len(f_regs):
                raise ModbusClient._NetworkError(MB_RECV_ERR, 'rx byte count mismatch')
            # allocate a reg_nb size list
            registers = [0] * reg_nb
            # fill registers list with register items
            for i in range(reg_nb):
                registers[i] = struct.unpack('>H', f_regs[i * 2:i * 2 + 2])[0]
            # return registers list
            return registers
        # handle error during request
        except ModbusClient._InternalError as e:
            self._req_except_handler(e)
            return None
        