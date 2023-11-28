from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *
from tools.logging import logger   
import pickle

data_col = [] ## This will hold the data for me to put into a file later

#doing all this a the "module level" in "Demo" server mode it will work fine :)

def on_sensor_state_changed(sensor, state):
    logger.debug('Sensor {0} is {1}'.format(sensor.Name, state))

def on_brain_bit_signal_data_received(sensor, data):
    logger.debug(data)
    data_col.append(data) # this reads input from Headband 

logger.debug("Create Headband Scanner")
gl_scanner = Scanner([SensorFamily.SensorLEBrainBit])
gl_sensor = None
logger.debug("Sensor Found Callback")

def sensorFound(scanner, sensors):
    global gl_scanner
    global gl_sensor
    for i in range(len(sensors)):
        logger.debug('Sensor %s' % sensors[i])
        logger.debug('Connecting to sensor')
        gl_sensor = gl_scanner.create_sensor(sensors[i])
        gl_sensor.sensorStateChanged = on_sensor_state_changed
        gl_sensor.connect()
        gl_sensor.signalDataReceived = on_brain_bit_signal_data_received
        
        # Start of Shariks code --  
        ## this code is from the Branbit SDK website under, Initialization (Main Parameters)
        mls = MathLibSetting(sampling_rate=250,
        process_win_freq=25,
        fft_window=1000,
        n_first_sec_skipped=4,
        bipolar_mode=False,
        channels_number=4,
        channel_for_analysis=3)

        ads = ArtifactDetectSetting(hanning_win_spectrum=True, num_wins_for_quality_avg=125)

        sads = ShortArtifactDetectSetting(ampl_art_extremum_border=25)

        mss = MentalAndSpectralSetting()

        emotions = EmotionalMath(mls, ads, sads, mss)
        ## Till Here
        
        print(emotions) ## This is a Data Structure Including the emotions from the Headband.

        dbfile = open('brainbitTest.pcl','ab') ## opens a .pcl file to write binary too
        pickle.dump(data_col, dbfile)   ## dumps the data_col into the dbfile

        dbfile.close()          ##closes file

        dbfile = open('brainbitTest.pcl','rb')      ## re opens file in 'rb' so that way we get a readable output
        print(pickle.load(dbfile))      ##prints the output
        ## End of Shariks Code---------------
        gl_sensor.BrainBitSensor()

        gl_scanner.stop()
        del gl_scanner


gl_scanner.sensorsChanged = sensorFound

logger.debug("Start scan")
gl_scanner.start()


def get_head_band_sensor_object():
    return gl_sensor

