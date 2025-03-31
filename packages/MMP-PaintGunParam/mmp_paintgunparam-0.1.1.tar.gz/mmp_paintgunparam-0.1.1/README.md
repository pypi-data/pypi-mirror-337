# PaintGunParamHandler

`PaintGunParamHandler` is a Python class designed to interface with and control a paint gun controller, such as the MS100 from Carlisle. This class allows users to configure parameters, read and write registers, and control the device via Modbus communication.

## Features

- Configure and initialize the paint gun controller with values from a YAML configuration file.
- Read and write to both holding registers and bits within holding registers.
- The Carlisle MS100 controller uses only holding registers as per the table 1.
- Enable or disable powder output with simple methods.
- Validate register addresses and manage bitwise operations for bit registers.

## Requirements

- Python 3.7+
- `pyModbusTCP version 0.2.1 only`
- `PyYAML`
- A compatible paint gun controller (e.g., MS100).

## Installation

pip install MMP_PaintGunParam
Ensure you have a `configs.yml` file in the same directory as the script (see the [Configuration](#configuration) section for details).

## Usage

### Initialization

Create an instance of `PaintGunParamHandler` by specifying a timeout value (default is `0.03` seconds):

```python
from MMP_PaintGunParam.paint_gun_param_handler import PaintGunParamHandler

handler = PaintGunParamHandler()

# To start the gun
handler.set_param("ctrl_word_bit_start", 1)

# To stop the gun
handler.set_param("ctrl_word_bit_start", 0)

```
Sets a specific parameter:

- `name`: The name of the parameter as defined in the `configs.yml` file.
- `value`: The value to set.

Example:

```python
handler.set_param("gun_btn_enabled", 1)
```

#### `get_param(name)`
Gets the current value of a parameter:

- `name`: The name of the parameter as defined in the `configs.yml` file.

Example:

```python
value = handler.get_param("gun_btn_enabled")
print(value)
```

### Configuration

The `configs.yml` file should define the controller's IP address, port, and register details. Example format:

```yaml
IP_ADDRESS: "192.168.2.111"
PORT: 4660
REGISTERS:
  gun_btn_enabled:
    address: 100
    init: true
    value: 0
  gun_btn_cmd_logic:
    address: 101
    init: true
    value: 0
  ...
```

### Table 1 - List of registers uses by the MS100 controller
| REG    | BIT/Type | Parameter      | Function Name                                      |
|--------|----------|----------------|---------------------------------------------------|
| 1      | bool     | ctrl_word      | Main control word for board operations            |
| 1.0    | 0        | ctrl_word_bit_on        | Board enable                                      |
| 1.01   | 1        | ctrl_word_bit_start     | Start board (if enabled)                         |
| 1.02   | 2        | ctrl_word_bit_tribo_on  | Tribo enable                                     |
| 1.03   | 3        | ctrl_word_bit_valve_pid_start_cmd | Valve PID direct start command                  |
| 1.04   | 4        | ctrl_word_bit_topcoat_gun       | Topcoat gun auto man                             |
| 1.08   | 8        | ctrl_word_bit_clock_in          | Com clock input from master                      |
| 1.09   | 9        | ctrl_word_bit_wash_on           | Enable mode wash                                 |
| 1.10   | 10       | ctrl_word_bit_start_autotuning  | Start autotuning                                 |
| 1.11   | 11       | ctrl_word_bit_wr_frequency      | Write frequency from register                    |
| 2      | Register | setpoint_kv                   | Setpoint kV                                      |
| 3      | Register | setpoint_ua                   | Setpoint uA                                      |
| 4      | Register | setpoint_ua_tribo             | uA tribo limit                                   |
| 5      | Register | setpoint_valve_bar_1          | Setpoint valve 1 in bar                          |
| 6      | Register | setpoint_valve_bar_2          | Setpoint valve 2 in bar                          |
| 7      | Register | setpoint_valve_bar_3          | Setpoint valve 3 in bar                          |
| 8      | Register | program_num_edit_popup        | Popup to edit program number                     |
| 9      | Register | program_number                | Program number                                   |
| 10     | bool     | wash_ctrl_word                |                                                  |
| 10.02  | 2        | ctrl_word_bit_valve_1_on       | Valve 1 ON                                       |
| 10.03  | 3        | ctrl_word_bit_valve_2_on       | Valve 2 ON                                       |
| 10.04  | 4        | ctrl_word_bit_valve_3_on       | Valve 3 ON                                       |
| 10.08  | 8        | ctrl_word_bit_fluid_on         | Fluid box ON (0=Normal operation; 1=Always ON)   |
| 10.09  | 9        | ctrl_word_bit_vibrator_on      | Vibrator ON (0=Normal operation; 1=Always ON)    |
| 11     | bool     | china_board                   |                                                  |
| 11.0   | 0        | china_board_bit_start          | Alternative start for China Board                |
| 12     | Register | frequency_setpoint             | Setpoint frequency                               |
| 13     | Register | autotuning_ua_limit            | Autotuning uA limit (fail)                       |
| 14     | Register | setpoint_wash_valve_1          | Setpoint wash valve 1                            |
| 15     | Register | setpoint_wash_valve_2          | Setpoint wash valve 2                            |
| 16     | Register | setpoint_wash_valve_3          | Setpoint wash valve 3                            |
| 17     | Register | cable_selection                | Cable selection                                  |
| 19     | bool     | gun_btn_management             |                                                  |
| 19.0   | 0        | gun_btn_enabled                | Gun button enabled                               |
| 19.01  | 1        | gun_btn_cmd_logic              | Gun button command logic                         |
| 20     | Register | uom_selection                  | UOM selection                                    |
| 21     | Register | setpoint_1                     | Setpoint valve 1                                 |
| 22     | Register | setpoint_2                     | Setpoint valve 2                                 |
| 23     | Register | setpoint_3                     | Setpoint valve 3                                 |
| 24     | Register | injector_type                  | Injector type (0=T9; 1=ELITE)                   |
| 51     | bool     | status_word                    |                                                  |
| 51.0   | 0        | status_word_bit_on             | Print enabled                                    |
| 51.01  | 1        | status_word_bit_start          | Print in start                                   |
| 51.02  | 2        | status_word_bit_tribo_on       | Tribo enabled                                    |
| 51.03  | 3        | status_word_bit_freq_mode      | Frequency mode (0=40kHz 1=20kHz)                |
| 51.05  | 5        | status_word_bit_positive_cascade | Positive cascade selected from hardware input  |
| 51.08  | 8        | status_word_bit_clock_out      | Com clock out to master                          |
| 51.09  | 9        | status_word_bit_wash_on        | Wash on                                          |
| 51.10  | 10       | status_word_bit_autotuning_running | Autotuning running                           |
| 51.11  | 11       | status_word_bit_autotuning_done | Autotuning done                               |
| 51.12  | 12       | status_word_bit_autotuning_fail | Autotuning done                               |
| 51.13  | 13       | status_word_bit_btn_mode_sel   | Gun selection mode button pressed (if manual gun) |
| 51.14  | 14       | status_word_bit_btn_increase   | Gun button plus pressed (if manual gun)         |
| 51.15  | 15       | status_word_bit_btn_decrease   | Gun button minus pressed (if manual gun)        |
| 52     | bool     | alm_word                      |                                                  |
| 52.0   | 0        | alm_word_bit_missing_ua_corona | Missing uA Corona                               |
| 52.01  | 1        | alm_word_bit_exceeding_ua      | Exceeding uA                                     |
| 52.02  | 2        | alm_word_bit_missing_ua_tribo  | Missing uA Tribo                                 |
| 52.05  | 5        | alm_word_bit_exceeding_kv_corona | Exceeding kV Corona                           |
| 52.08  | 8        | alm_word_bit_comm_eth          | Ethernet communication alarm                    |
| 52.09  | 9        | alm_word_bit_comm_serial       | Serial communication alarm                      |
| 52.10  | 10       | alm_word_bit_synth_overtemp    | Synthesizer overtemperature alarm               |
| 52.11  | 11       | alm_word_bit_synth_dc_output   | Synthesizer dc output alarm                     |
| 52.12  | 12       | alm_word_bit_synth_undervoltage | Synthesizer undervoltage alarm                |
| 53     | Register | feedback_kv                    | Feedback kV                                      |
| 54     | Register | feedback_ua_corona             | Feedback uA corona                               |
| 55     | Register | feedback_ua_tribo              | Feedback uA tribo                                |
| 57     | Register | feedback_frequency             | Actual frequency setpoint                        |
| 60     | Register | cycle_time 60                  | Cycle time in ms                                 |
| 61     | Register | test_pid_kp                    | PID KP test (scaled 1/1000)                      |
| 62     | Register | test_pid_kd                    | PID KD test (scaled 1/1000)                      |
| 63     | Register | test_pid_ki                    | PID KI test (scaled 1/1000)                      |
| 64     | Register | test_pid_ki_ua                 | PID KI test for uA (scaled 1/1000)              |
| 65     | Register | test_pid_step_slow             | PID step value (scaled 1/100)                   |
| 66     | Register | test_pid_theorical_value       | PID theorical reference value                   |
| 67     | Register | test_pid_integral_limit        | PID integral limit                              |
| 69     | Register | pid_test_enable                | PID enable test                                 |
| 70     | Register | pid_test_select                | PID select (0=Osc,1=V1,2=V2,3=V3)              |
| 71     | Register | pid_test_mode                  | PID mode (0=direct; 1=force K)                 |
| 72     | Register | pid_test_direct_ana            | PID direct ANA value (for direct mode)         |
| 80     | Register | pid_kv_fb_error                | PID kV error feedback                           |
| 81     | Register | pid_kv_fb_error_t1             | PID kV error t1 feedback                        |
| 82     | Register | pid_kv_fb_error_sum            | PID kV error sum feedback                       |
| 85     | Register | pid_ua_fb_error_sum            | PID uA error sum feedback                       |
| 91     | Register | sw_version                     | Software version                                |
| 92     | Register | print_type                     | Print type 0="CP1", 1="CP2"                   |
| 94     | Register | fb_valve_1_bar                 | Valve 1 bar feedback*100                        |
| 95     | Register | fb_valve_2_bar                 | Valve 2 bar feedback*100                        |
| 96     | Register | fb_valve_3_bar                 | Valve 3 bar feedback*100                        |
| 97     | Register | pid_v1_error_sum               | PID valve 1 error sum                           |
| 98     | Register | pid_v2_error_sum               | PID valve 2 error sum                           |
| 99     | Register | pid_v3_error_sum               | PID valve 3 error sum                           |
| 100    | Register | pid_v1_output                  | PID valve 1 output                              |
| 101    | Register | pid_v2_output                  | PID valve 2 output                              |
| 102    | Register | pid_v3_output                  | PID valve 3 output                              |
| 103    | Register | fb_valve_3_psi                 | Valve 3 feedback in PSI                         |
| 104    | Register | fb_valve_3_nm3h                | Valve 3 feedback in Nm3/h*10                    |
| 105    | Register | fb_total_air_perc              | Feedback of total air percentage for powder     |
| 106    | Register | fb_total_air_psi               | Percentual total air PSI feedback               |
| 107    | Register | fb_total_air_nm3h              | Percentual total air Nm3/h*10 feedback          |
| 110    | bool     | fb_di                          |                                                  |
| 110.0  | 0        | fb_di_bit_tribo_reed           | Digital Input external start feedback           |
| 110.01 | 1        | fb_di_bit_btn_mode_sel         | Digital Input mode selection button feedback    |
| 110.02 | 2        | fb_di_bit_wash_ext_start       | Digital Input wash external start feedback      |
| 110.03 | 3        | fb_di_bit_btn_increase         | Digital input button increase feedback          |
| 110.04 | 4        | fb_di_bit_corona_reed          | Digital input reed in feedback                  |
| 110.05 | 5        | fb_di_bit_btn_decrease         | Digital input tribo enable feedback             |
| 110.06 | 6        | fb_di_bit_synth_overtemp_alm   | Digital input synthesizer overtemperature alarm |
| 110.07 | 7        | fb_di_bit_synth_dc_output_alm  | Digital input synthesizer DC output alarm       |
| 110.08 | 8        | fb_di_bit_synth_undervolt_alm  | Digital input synthesizer undervoltage alarm    |
| 110.12 | 12       | fb_di_bit_dip_0               | Digital input dip switch 0 feedback             |
| 110.13 | 13       | fb_di_bit_dip_1               | Digital input dip switch 1 feedback             |
| 110.14 | 14       | fb_di_bit_dip_2               | Digital input dip switch 2 feedback             |
| 110.15 | 15       | fb_di_bit_dip_3               | Digital input dip switch 3 feedback             |
| 111    | bool     | fb_do                         |                                                  |
| 111.0  | 0        | fb_do_bit_relay               | Digital Output relay feedback                   |
| 111.01 | 1        | fb_do_bit_led44               | Digital Output led 1 feedback                   |
| 111.02 | 2        | fb_do_bit_board_start         | Digital Output start feedback                   |
| 111.03 | 3        | fb_do_bit_vibrator_fluid      | Digital Output fluid valve feedback             |
| 111.04 | 4        | fb_do_bit_do3                 | Digital Output 2 in feedback                    |
| 111.05 | 5        | fb_do_bit_gun_alm             | Digital Output gun alarm feedback               |
| 111.06 | 6        | fb_do_bit_led42               | Digital Output relay 1 feedback                 |
| 111.07 | 7        | fb_do_bit_led43               | Digital Output relay 2 feedback                 |
| 112    | Register | fb_rotary_switch              | Rotary switch feedback                          |
| 113    | bool     | fb_com                        |                                                  |
| 113.0  | 0        | fb_com_master_rx              | Master in rx                                    |
| 113.01 | 1        | fb_com_master_tx              | Master in tx                                    |
| 113.02 | 2        | fb_com_slave_rx               | Slave in rx                                     |
| 113.03 | 3        | fb_com_slave_tx               | Slave in tx                                     |
| 113.04 | 4        | fb_eeprom_rd                  | EEPROM ready                                    |
| 113.05 | 5        | fb_eeprom_wr                  | EEPROM in write operation                       |
| 114    | Register | oscillator_output             | Oscillator output                               |
| 115    | Register | fb_ua_corona_adc              | Direct ADC feeback for UA CORONA                |
| 116    | Register | fb_ua_tribo_adc               | Direct ADC feeback for UA TRIBO                 |
| 117    | Register | fb_kv_adc                     | Direct ADC feeback for kV                       |
| 118    | Register | fb_valve_1_adc                | Direct ADC feeback for valve 1                  |
| 119    | Register | fb_valve_2_adc                | Direct ADC feeback for valve 2                  |
| 120    | Register | fb_valve_3_adc                | Direct ADC feeback for valve 3                  |
| 122    | Register | valve_1_dac_out               | Direct DAC out for valve 1                      |
| 123    | Register | valve_2_dac_out               | Direct DAC out for valve 2                      |
| 124    | Register | valve_3_dac_out               | Direct DAC out for valve 3                      |


### Error Handling
Errors are logged to the console, and the class provides informative messages for invalid operations or configuration issues.

### Logging
The class uses Python's built-in `logging` module to log Modbus communication at the DEBUG level. You can customize logging settings as needed.

## License
This project is licensed under Technologies NeuroBotIA Inc.
