import time
import math
from rascam.i2c import I2C
import sys
import tty
import termios
import asyncio
from rascam.filedb import FileDB


def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)


def bytes_toint(msb, lsb):
    '''
    Convert two bytes to signed integer (big endian)
    for little endian reverse msb, lsb arguments
    Can be used in an interrupt handler
    '''
    if not msb & 0x80:
        return msb << 8 | lsb  # +ve
    return - (((msb ^ 255) << 8) | (lsb ^ 255) + 1)


def default_wait():
    '''
    delay of 10 ms
    '''
    time.sleep(0.01)

def stop_func():
    return False

class Sh3001(I2C):
    SH3001_ADDRESS				= 0x36		# 7bit: 011 0111
    '''
    /******************************************************************
    *	SH3001 Registers Macro Definitions 
    ******************************************************************/
    '''
    SH3001_ACC_XL				= 0x00
    SH3001_ACC_XH				= 0x01
    SH3001_ACC_YL				= 0x02
    SH3001_ACC_YH				= 0x03
    SH3001_ACC_ZL				= 0x04
    SH3001_ACC_ZH				= 0x05
    SH3001_GYRO_XL				= 0x06
    SH3001_GYRO_XH				= 0x07
    SH3001_GYRO_YL				= 0x08
    SH3001_GYRO_YH				= 0x09
    SH3001_GYRO_ZL				= 0x0A
    SH3001_GYRO_ZH				= 0x0B
    SH3001_TEMP_ZL				= 0x0C
    SH3001_TEMP_ZH				= 0x0D
    SH3001_CHIP_ID				= 0x0F
    SH3001_INT_STA0				= 0x10
    SH3001_INT_STA1				= 0x11
    SH3001_INT_STA2				= 0x12
    SH3001_INT_STA3				= 0x14
    SH3001_INT_STA4				= 0x15
    SH3001_FIFO_STA0			= 0x16
    SH3001_FIFO_STA1			= 0x17
    SH3001_FIFO_DATA			= 0x18
    SH3001_TEMP_CONF0			= 0x20
    SH3001_TEMP_CONF1			= 0x21

    SH3001_ACC_CONF0			= 0x22		# accelerometer config 0x22-0x26
    SH3001_ACC_CONF1			= 0x23
    SH3001_ACC_CONF2			= 0x25
    SH3001_ACC_CONF3			= 0x26

    SH3001_GYRO_CONF0			= 0x28		# gyroscope config 0x28-0x2B
    SH3001_GYRO_CONF1			= 0x29
    SH3001_GYRO_CONF2			= 0x2B

    SH3001_SPI_CONF				= 0x32
    SH3001_FIFO_CONF0			= 0x35
    SH3001_FIFO_CONF1			= 0x36
    SH3001_FIFO_CONF2			= 0x37
    SH3001_FIFO_CONF3			= 0x38
    SH3001_FIFO_CONF4			= 0x39
    SH3001_MI2C_CONF0						= 0x3A
    SH3001_MI2C_CONF1						= 0x3B
    SH3001_MI2C_CMD0						= 0x3C
    SH3001_MI2C_CMD1						= 0x3D
    SH3001_MI2C_WR							= 0x3E
    SH3001_MI2C_RD							= 0x3F
    SH3001_INT_ENABLE0					= 0x40
    SH3001_INT_ENABLE1					= 0x41
    SH3001_INT_CONF							= 0x44
    SH3001_INT_LIMIT						= 0x45
    SH3001_ORIEN_INTCONF0				= 0x46
    SH3001_ORIEN_INTCONF1				= 0x47
    SH3001_ORIEN_INT_LOW				= 0x48
    SH3001_ORIEN_INT_HIGH				= 0x49
    SH3001_ORIEN_INT_SLOPE_LOW	= 0x4A
    SH3001_ORIEN_INT_SLOPE_HIGH	= 0x4B
    SH3001_ORIEN_INT_HYST_LOW		= 0x4C
    SH3001_ORIEN_INT_HYST_HIGH	= 0x4D
    SH3001_FLAT_INT_CONF				= 0x4E
    SH3001_ACT_INACT_INT_CONF		= 0x4F
    SH3001_ACT_INACT_INT_LINK		= 0x50
    SH3001_TAP_INT_THRESHOLD		= 0x51
    SH3001_TAP_INT_DURATION			= 0x52
    SH3001_TAP_INT_LATENCY			= 0x53
    SH3001_DTAP_INT_WINDOW			= 0x54
    SH3001_ACT_INT_THRESHOLD		= 0x55
    SH3001_ACT_INT_TIME					= 0x56
    SH3001_INACT_INT_THRESHOLDL	= 0x57
    SH3001_INACT_INT_TIME				= 0x58
    SH3001_HIGHLOW_G_INT_CONF		= 0x59
    SH3001_HIGHG_INT_THRESHOLD	= 0x5A
    SH3001_HIGHG_INT_TIME				= 0x5B
    SH3001_LOWG_INT_THRESHOLD		= 0x5C
    SH3001_LOWG_INT_TIME				= 0x5D
    SH3001_FREEFALL_INT_THRES		= 0x5E
    SH3001_FREEFALL_INT_TIME		= 0x5F
    SH3001_INT_PIN_MAP0					= 0x79
    SH3001_INT_PIN_MAP1					= 0x7A
    SH3001_INACT_INT_THRESHOLDM	= 0x7B
    SH3001_INACT_INT_THRESHOLDH	= 0x7C
    SH3001_INACT_INT_1G_REFL		= 0x7D
    SH3001_INACT_INT_1G_REFH		= 0x7E
    SH3001_SPI_REG_ACCESS				= 0x7F
    SH3001_GYRO_CONF3						= 0x8F
    SH3001_GYRO_CONF4						= 0x9F
    SH3001_GYRO_CONF5						= 0xAF
    SH3001_AUX_I2C_CONF					= 0xFD

    '''
    /******************************************************************
    *	ACC Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_ODR_1000HZ			= 0x00
    SH3001_ODR_500HZ			= 0x01
    SH3001_ODR_250HZ			= 0x02
    SH3001_ODR_125HZ			= 0x03
    SH3001_ODR_63HZ				= 0x04
    SH3001_ODR_31HZ				= 0x05
    SH3001_ODR_16HZ				= 0x06
    SH3001_ODR_2000HZ			= 0x08
    SH3001_ODR_4000HZ			= 0x09
    SH3001_ODR_8000HZ			= 0x0A
    SH3001_ODR_16000HZ		= 0x0B
    SH3001_ODR_32000HZ		= 0x0C

    SH3001_ACC_RANGE_16G	= 0x02
    SH3001_ACC_RANGE_8G		= 0x03
    SH3001_ACC_RANGE_4G		= 0x04
    SH3001_ACC_RANGE_2G		= 0x05

    SH3001_ACC_ODRX040		= 0x00
    SH3001_ACC_ODRX025		= 0x20
    SH3001_ACC_ODRX011		= 0x40
    SH3001_ACC_ODRX004		= 0x60

    SH3001_ACC_FILTER_EN	= 0x00
    SH3001_ACC_FILTER_DIS	= 0x80

    '''
    /******************************************************************
    *	GYRO Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_GYRO_RANGE_125		= 0x02
    SH3001_GYRO_RANGE_250		= 0x03
    SH3001_GYRO_RANGE_500		= 0x04
    SH3001_GYRO_RANGE_1000	= 0x05
    SH3001_GYRO_RANGE_2000	= 0x06

    SH3001_GYRO_ODRX00			= 0x00
    SH3001_GYRO_ODRX01			= 0x04
    SH3001_GYRO_ODRX02			= 0x08
    SH3001_GYRO_ODRX03			= 0x0C

    SH3001_GYRO_FILTER_EN		= 0x00
    SH3001_GYRO_FILTER_DIS	= 0x10

    '''
    /******************************************************************
    *	Temperature Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_TEMP_ODR_500		= 0x00
    SH3001_TEMP_ODR_250		= 0x10
    SH3001_TEMP_ODR_125		= 0x20
    SH3001_TEMP_ODR_63		= 0x30

    SH3001_TEMP_EN				= 0x80
    SH3001_TEMP_DIS				= 0x00

    '''
    /******************************************************************
    *	INT Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_INT_LOWG					= 0x8000
    SH3001_INT_HIGHG				= 0x4000
    SH3001_INT_INACT				= 0x2000
    SH3001_INT_ACT					= 0x1000
    SH3001_INT_DOUBLE_TAP		= 0x0800
    SH3001_INT_TAP					= 0x0400
    SH3001_INT_FLAT					= 0x0200
    SH3001_INT_ORIENTATION	= 0x0100
    SH3001_INT_FIFO_GYRO		= 0x0010
    SH3001_INT_GYRO_READY		= 0x0008
    SH3001_INT_ACC_FIFO			= 0x0004
    SH3001_INT_ACC_READY		= 0x0002
    SH3001_INT_FREE_FALL		= 0x0001
    SH3001_INT_UP_DOWN_Z		= 0x0040

    SH3001_INT_ENABLE				= 0x01
    SH3001_INT_DISABLE			= 0x00

    SH3001_INT_MAP_INT1			= 0x01
    SH3001_INT_MAP_INT			= 0x00

    SH3001_INT_LEVEL_LOW		= 0x80
    SH3001_INT_LEVEL_HIGH		= 0x7F
    SH3001_INT_NO_LATCH			= 0x40
    SH3001_INT_LATCH				= 0xBF
    SH3001_INT_CLEAR_ANY		= 0x10
    SH3001_INT_CLEAR_STATUS	= 0xEF
    SH3001_INT_INT1_NORMAL	= 0x04
    SH3001_INT_INT1_OD			= 0xFB
    SH3001_INT_INT_NORMAL		= 0x01
    SH3001_INT_INT_OD				= 0xFE

    '''
    /******************************************************************
    *	Orientation Blocking Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_ORIENT_BLOCK_MODE0	= 0x00
    SH3001_ORIENT_BLOCK_MODE1	= 0x04
    SH3001_ORIENT_BLOCK_MODE2	= 0x08
    SH3001_ORIENT_BLOCK_MODE3	= 0x0C

    SH3001_ORIENT_SYMM				= 0x00
    SH3001_ORIENT_HIGH_ASYMM	= 0x01
    SH3001_ORIENT_LOW_ASYMM		= 0x02

    '''
    /******************************************************************
    *	Flat Time Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_FLAT_TIME_500MS		= 0x40
    SH3001_FLAT_TIME_1000MS		= 0x80
    SH3001_FLAT_TIME_2000MS		= 0xC0

    '''
    /******************************************************************
    *	ACT and INACT Int Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_ACT_AC_MODE		= 0x80
    SH3001_ACT_DC_MODE		= 0x00
    SH3001_ACT_X_INT_EN		= 0x40
    SH3001_ACT_X_INT_DIS	= 0x00
    SH3001_ACT_Y_INT_EN		= 0x20
    SH3001_ACT_Y_INT_DIS	= 0x00
    SH3001_ACT_Z_INT_EN		= 0x10
    SH3001_ACT_Z_INT_DIS	= 0x00


    SH3001_INACT_AC_MODE		= 0x08
    SH3001_INACT_DC_MODE		= 0x00
    SH3001_INACT_X_INT_EN		= 0x04
    SH3001_INACT_X_INT_DIS	= 0x00
    SH3001_INACT_Y_INT_EN		= 0x02
    SH3001_INACT_Y_INT_DIS	= 0x00
    SH3001_INACT_Z_INT_EN		= 0x01
    SH3001_INACT_Z_INT_DIS	= 0x00


    SH3001_LINK_PRE_STA			= 0x01
    SH3001_LINK_PRE_STA_NO	= 0x00

    '''
    /******************************************************************
    *	TAP Int Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_TAP_X_INT_EN		= 0x08
    SH3001_TAP_X_INT_DIS	= 0x00
    SH3001_TAP_Y_INT_EN		= 0x04
    SH3001_TAP_Y_INT_DIS	= 0x00
    SH3001_TAP_Z_INT_EN		= 0x02
    SH3001_TAP_Z_INT_DIS	= 0x00

    '''
    /******************************************************************
    *	HIGHG Int Config Macro Definitions 
    ******************************************************************/
    '''

    SH3001_HIGHG_ALL_INT_EN		= 0x80
    SH3001_HIGHG_ALL_INT_DIS	= 0x00
    SH3001_HIGHG_X_INT_EN			= 0x40
    SH3001_HIGHG_X_INT_DIS		= 0x00
    SH3001_HIGHG_Y_INT_EN			= 0x20
    SH3001_HIGHG_Y_INT_DIS		= 0x00
    SH3001_HIGHG_Z_INT_EN			= 0x10
    SH3001_HIGHG_Z_INT_DIS		= 0x00

    '''
    /******************************************************************
    *	LOWG Int Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_LOWG_ALL_INT_EN		= 0x01
    SH3001_LOWG_ALL_INT_DIS		= 0x00

    '''
    /******************************************************************
    *	SPI Interface Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_SPI_3_WIRE		= 0x01
    SH3001_SPI_4_WIRE		= 0x00


    '''
    /******************************************************************
    *	FIFO Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_FIFO_MODE_DIS				= 0x00
    SH3001_FIFO_MODE_FIFO				= 0x01
    SH3001_FIFO_MODE_STREAM			= 0x02
    SH3001_FIFO_MODE_TRIGGER		= 0x03

    SH3001_FIFO_ACC_DOWNS_EN		= 0x80
    SH3001_FIFO_ACC_DOWNS_DIS		= 0x00
    SH3001_FIFO_GYRO_DOWNS_EN		= 0x08
    SH3001_FIFO_GYRO_DOWNS_DIS	= 0x00

    SH3001_FIFO_FREQ_X1_2				= 0x00
    SH3001_FIFO_FREQ_X1_4				= 0x01
    SH3001_FIFO_FREQ_X1_8				= 0x02
    SH3001_FIFO_FREQ_X1_16			= 0x03
    SH3001_FIFO_FREQ_X1_32			= 0x04
    SH3001_FIFO_FREQ_X1_64			= 0x05
    SH3001_FIFO_FREQ_X1_128			= 0x06
    SH3001_FIFO_FREQ_X1_256			= 0x07

    SH3001_FIFO_EXT_Z_EN				= 0x2000
    SH3001_FIFO_EXT_Y_EN				= 0x1000
    SH3001_FIFO_EXT_X_EN				= 0x0080
    SH3001_FIFO_TEMPERATURE_EN	= 0x0040
    SH3001_FIFO_GYRO_Z_EN				= 0x0020
    SH3001_FIFO_GYRO_Y_EN				= 0x0010
    SH3001_FIFO_GYRO_X_EN				= 0x0008
    SH3001_FIFO_ACC_Z_EN				= 0x0004
    SH3001_FIFO_ACC_Y_EN				= 0x0002
    SH3001_FIFO_ACC_X_EN				= 0x0001
    SH3001_FIFO_ALL_DIS					= 0x0000

    '''
    /******************************************************************
    *	AUX I2C Config Macro Definitions 
    ******************************************************************/
    '''
    SH3001_MI2C_NORMAL_MODE			= 0x00
    SH3001_MI2C_BYPASS_MODE			= 0x01

    SH3001_MI2C_READ_ODR_200HZ	= 0x00
    SH3001_MI2C_READ_ODR_100HZ	= 0x10
    SH3001_MI2C_READ_ODR_50HZ		= 0x20
    SH3001_MI2C_READ_ODR_25HZ		= 0x30

    SH3001_MI2C_FAIL						= 0x20
    SH3001_MI2C_SUCCESS					= 0x10

    SH3001_MI2C_READ_MODE_AUTO		= 0x40
    SH3001_MI2C_READ_MODE_MANUAL	= 0x00


    '''
    /******************************************************************
    *	Other Macro Definitions 
    ******************************************************************/
    '''
    SH3001_TRUE		= 0
    SH3001_FALSE	= 1

    SH3001_NORMAL_MODE		= 0x00
    SH3001_SLEEP_MODE			= 0x01
    SH3001_POWERDOWN_MODE	= 0x02


    def __init__(self):
        super().__init__()
        # self.6d_data_buf = bytearray([0,0,0,0,0,0])
        db = '/home/pi/.rascam_config'
        self.reg_status = bytearray([0])
        self.sh3001_init()
        # self.acc_cal = [-288.0, 141.5, 31.5]
        self.db = FileDB(db=db)
        db_val = self.db.get('calibrate_offset_list', default_value=str(self.new_list(0)))
        db_val = [float(i.strip()) for i in db_val.strip("[]").split(",")]
        self.acc_offset = db_val
        
        # self.acc_offset = [-288.0, 141.5, -30]
        # self.acc_scale = [1,1,1]
        # self.gyro_offset = [-40,-235,-15]
        self.gyro_offset = [0,0,0]
        self.data_vector = [0,0,0]
        # self.cal = [0,0,0]
        # pass

    def new_list(self, default_value):
        _ = [0 for i in range(3)]
        return _

    def calibrate(self,aram, stopfunc=stop_func, waitfunc=default_wait):
        '''
        calibration routine, sets cal
        '''
        # self.update()
        # if aram isinstance()
        maxvec = self.data_vector[:]                # Initialise max and min lists with current values
        minvec = self.data_vector[:]
        count = 0
        # print(stop_func)
        if aram == 'acc':
            while True:
                # pass
            # print('quit_cal')
                # if count >=500:
                #     break
                waitfunc()
                self.data_vector = self._sh3001_getimudata()[0]
                # minvec = sensor.sh3001_getimudata(aram,'xyz')

                maxvec = list(map(max, maxvec, self.data_vector))
                minvec = list(map(min, minvec, self.data_vector))
                print('max_list: ',maxvec,'min_list: ',minvec)
                exec("self." + aram + "_offset = tuple(map(lambda a, b: (a + b)/2, maxvec, minvec))")
            # count +=1
        elif aram == 'gyro':
            sum_list = [0,0,0]
            count = 0
            for i in range(503):
                if i > 2:
                    sum_list = [sum_list[i] + sensor.sh3001_getimudata('gyro','xyz')[i] for i in range(3)]
                    # print(count)
                    # count +=1
            # print("sum_list:",sum_list)
            self.gyro_offset = [round(sum_list[i],2) / 500.0 for i in range(3)]
            print("gyro_offset:",self.gyro_offset)
        
        else:
            raise ValueError('aram must be acc or gyro')
        # exec("self." + aram + "_scale = tuple(map(lambda a, b: (a - b)/ 4096.0, maxvec, minvec))")
        # exec("self." + aram + "_offset = tuple(map(lambda a, b: (a + b)/2, maxvec, minvec))")
        # print(self.acc_offset)
        # return self.acc_offset
        # print(self.acc_scale)


        # sum_list = [0,0,0]
        # count = 0
        # for i in range(503):
        #     if i > 2:
        #         sum_list = [sum_list[i] + sensor.sh3001_getimudata('acc','xyz')[i] for i in range(3)]
        #         # print(count)
        #         # count +=1
        # print("sum_list:",sum_list)
        # self.acc_cal = [round(sum_list[i] / 500.0, 2) for i in range(3)]
        # # print("gyro_val:",self.gyro_offset)
        # self.acc_cal[0]
        # print("acc_cal:",self.acc_cal)


    def sh3001_write(self,reg_addr,data):
        # data = bytearray(data)
        self.mem_write(data, self.SH3001_ADDRESS, reg_addr, timeout=5000, addr_size=8)

    def sh3001_read(self,reg_addr,data):
        data = bytearray(data)
        return self.mem_read(data, self.SH3001_ADDRESS, reg_addr, timeout=5000, addr_size=8)

    def sh3001_init(self):
        regData = [0] 
        i = 0
        while((regData[0] != 0x61) and (i<3)):
            regData = self.sh3001_read(self.SH3001_CHIP_ID,self.reg_status)
            i+=1
            if (i==3) and (regData[0] !=0x61):
                return False
        # print('module_reset')
        self.sh3001_module_reset()
        # print('sh3001_acc_config')
        self.sh3001_acc_config(self.SH3001_ODR_500HZ,self.SH3001_ACC_RANGE_16G,self.SH3001_ACC_ODRX025,self.SH3001_ACC_FILTER_EN)
        # print('sh3001_gyro_config')
        self.sh3001_gyro_config(self.SH3001_ODR_500HZ,self.SH3001_GYRO_RANGE_2000,self.SH3001_GYRO_RANGE_2000, self.SH3001_GYRO_RANGE_2000\
        ,self.SH3001_GYRO_ODRX00,self.SH3001_GYRO_FILTER_EN)
        # print('sh3001_temp_config')
        self.sh3001_temp_config(self.SH3001_TEMP_ODR_63, self.SH3001_TEMP_EN)

        return True

        
    def sh3001_module_reset(self):

        #soft reset
        regData = 0x73
        self.sh3001_write(self.SH3001_ADDRESS,regData)
        time.sleep(0.05)

        #ADCreset
        regdata = 0x02
        self.sh3001_write(self.SH3001_ADDRESS,regData)
        regdata = 0xC1
        self.sh3001_write(self.SH3001_ADDRESS,regData)
        regdata = 0xC2
        self.sh3001_write(self.SH3001_ADDRESS,regData)
        regdata = 0x00
        self.sh3001_write(self.SH3001_ADDRESS,regData)

        #CVA reset
        regdata = 0x18
        self.sh3001_write(self.SH3001_ADDRESS,regData)
        regdata = 0x00
        self.sh3001_write(self.SH3001_ADDRESS,regData)
        time.sleep(0.01)


    def sh3001_acc_config(self,accODR,accRange,accCutOffFreq, accFilterEnble):
        # print('acc_config')
        # enable acc digital filter
        regData = self.sh3001_read(self.SH3001_ACC_CONF0, self.reg_status)
        regData[0] |= 0x01
        self.sh3001_write(self.SH3001_ACC_CONF0,regData)

        # set acc ODR
        self.sh3001_write(self.SH3001_ACC_CONF1,accODR)

        # set acc Range
        self.sh3001_write(self.SH3001_ACC_CONF2,accRange)
        regData = self.sh3001_read(self.SH3001_ACC_CONF2, self.reg_status)
        # print(regData)

        # bypass acc low pass filter or not
        regData = self.sh3001_read(self.SH3001_ACC_CONF3, self.reg_status)
        regData[0] &= 0x17
        regData[0] |= (accCutOffFreq | accFilterEnble)
        self.sh3001_write(self.SH3001_ACC_CONF3,regData)


    def sh3001_gyro_config(self,gyroODR,gyroRangeX,gyroRangeY,gyroRangeZ,gyroCutOffFreq,gyroFilterEnble):

        regData = self.sh3001_read(self.SH3001_GYRO_CONF0, self.reg_status)
        regData[0] |= 0x01
        self.sh3001_write(self.SH3001_GYRO_CONF0,regData)

        # set gyro ODR
        self.sh3001_write(self.SH3001_GYRO_CONF1,gyroODR)

        # set acc Range
        self.sh3001_write(self.SH3001_GYRO_CONF3,gyroRangeX)
        self.sh3001_write(self.SH3001_GYRO_CONF4,gyroRangeY)
        self.sh3001_write(self.SH3001_GYRO_CONF5,gyroRangeZ)

        # bypass acc low pass filter or not
        regData = self.sh3001_read(self.SH3001_GYRO_CONF2, self.reg_status)
        regData[0] &= 0xE3
        regData[0] |= (gyroCutOffFreq | gyroFilterEnble)
        self.sh3001_write(self.SH3001_GYRO_CONF2,regData)

    def sh3001_temp_config(self,tempODR,tempEnable):

        regData = self.sh3001_read(self.SH3001_TEMP_CONF0, self.reg_status)
        regData[0] &= 0x4F
        regData[0] |= (tempODR | tempEnable)
        self.sh3001_write(self.SH3001_TEMP_CONF0,regData)
        regData = self.sh3001_read(self.SH3001_TEMP_CONF0, self.reg_status)

    def _sh3001_getimudata(self):
        gyroData = [0,0,0]
        accData = [0,0,0]
        regData = [0 for i in range(12)]
        regData = self.sh3001_read(self.SH3001_ACC_XL,regData)
 
        accData[0] = bytes_toint(regData[1],regData[0])
        accData[1] = bytes_toint(regData[3],regData[2])
        accData[2] = bytes_toint(regData[5],regData[4])
        # accData = [(accData[i] - self.acc_cal[i]) for i in range(len(accData))]


        gyroData[0] = bytes_toint(regData[7],regData[6])
        gyroData[1] = bytes_toint(regData[9],regData[8])
        gyroData[2] = bytes_toint(regData[11],regData[10])
        #   
        # gyroData = [gyroData[i] - self.gyro_offset[i] for i in range(len(gyroData))]

        return accData,gyroData

    def sh3001_getimudata(self,aram,axis):
        accData,gyroData = self._sh3001_getimudata()
        accData = [(accData[i] - self.acc_offset[i]) for i in range(len(accData))]
        gyroData = [gyroData[i] - self.gyro_offset[i] for i in range(len(gyroData))]
        # print()

        if aram == 'acc':
            if axis == 'x':
                return accData[0]
            elif axis == 'y':
                return accData[1]
            elif axis == 'z':
                return accData[2]
            elif axis == 'xy':
                return [accData[0],accData[1]]
            elif axis == 'xz':
                return [accData[0],accData[2]]
            elif axis == 'yz':
                return [accData[1],accData[2]]
            elif axis == 'xyz':
                return [accData[0],accData[1],accData[2]]
            # else:
            #     raise ValueError('axis must be x,y,z,xy,xz,xyz')

        elif aram == 'gyro':
            if axis == 'x':
                return gyroData[0]
            elif axis == 'y':
                return gyroData[1]
            elif axis =='z':
                return gyroData[2]
            elif axis == 'xy':
                return [gyroData[0],gyroData[1]]
            elif axis == 'xz':
                return [gyroData[0],gyroData[2]]
            elif axis == 'yz':
                return [gyroData[1],gyroData[2]]
            elif axis == 'xyz':
                return [gyroData[0],gyroData[1],gyroData[2]]
            # else:
            #     raise ValueError('axis must be x,y,z,xy,xz,xyz')

        elif aram == 'all':
            return accData,gyroData
        
        else:
            raise ValueError('aram must be acc ,gyro or all')



    def sh3001_gettempdata(self):
        regdata =[0,0]
        tempref = [0,0]
        regData = self.sh3001_read(self.SH3001_TEMP_CONF0, regdata)
        tempref[0] = regData[0] & 0x0F << 8 | regData[1]

        regData = self.sh3001_read(self.SH3001_TEMP_ZL, regdata)
        tempref[1] = regData[1] & 0x0F << 8 | regData[0]

        return (tempref[1] - tempref[0])/16.0 + 25.0

    # def zero_point_init(self):
    #     sum_list = [0,0,0]
    #     count = 0
    #     for i in range(503):
    #         if i > 2:
    #             sum_list = [sum_list[i] + sensor.sh3001_getimudata('gyro','xyz')[i] for i in range(3)]
    #             # print(count)
    #             # count +=1
    #     print("sum_list:",sum_list)
    #     self.gyro_offset = [round(sum_list[i],2) / 500.0 for i in range(3)]
    #     print("gyro_val:",self.gyro_offset)

    def set_offset(self,offset_list):
        temp = str(list(offset_list))
        self.db.set('calibrate_offset_list',temp)
        self.acc_offset = offset_list

    def acc_calibrate_cmd(self):

        try:
            # sensor = Sh3001()
            print('press the s to start calibrate,\nquit use ctrl c')
            input_val = readkey()
            print(input_val)
            if input_val == 's':
                print("start_calibrating")
                while True:
                    # print('cal')
                    self.calibrate('acc')
                    time.sleep(0.1)
                    # break
        finally:
            self.set_offset(self.acc_offset)
            print('offset: ',self.acc_offset)


if __name__ == '__main__':
    import time
    from math import asin
    # import sys
    # import tty
    # import termios
    # import asyncio
    
    

    sensor = Sh3001()
    # sensor.zero_point_init()
    # print('init')
    # print(sensor.sh3001_init())
    a = 0
    current_val = [0,0,0]
    delta = 1
    last_val = [0,0,0]
    count = 0
    ODR_T = 0.1
    acc_list = []
    while True:
        pass
    #  gyro
        # current_val = [i / 16.4 * ODR_T if abs(i / 16.4 * ODR_T) > 1 else 0 for i in sensor.sh3001_getimudata('gyro','xyz')]
        # last_val = [last_val[i] + current_val[i] for i in range(3)]

        current_val = [i / 16.4 * 0.1 for i in sensor.sh3001_getimudata('acc','xyz')]
        # last_val = [last_val[i] + current_val[i] for i in range(3)]
        
        print(current_val)
        time.sleep(ODR_T)


    # # acc
        
        # acc_list = sensor.sh3001_getimudata('acc','xyz')
        # print(acc_list)

        # acc_list = [min(2046,i) for i in acc_list]
        # acc_list = [max(-2046,i) for i in acc_list]
        # # print(asin(acc_list[0] / 2100.0))
        # print((asin(acc_list[0] / 2046.0)) / math.pi * 180)
        # time.sleep(0.1)