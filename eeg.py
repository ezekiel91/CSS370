from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *
from tools.logging import logger   
import pickle
##from em_st_artifacts.emotional_math import EmotionalMath
from em_st_artifacts.emotional_math import *

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
        
        # Start of Shariks code --  Try to move this to line 15, that might be where this code needs to be 
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
        logger.debug("EMOTIONS HERE")
        logger.debug(emotions) ## This is a Data Structure Including the emotions from the Headband.
        logger.debug("END OF EMOTIONS HERE")

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
## here is code found from -- https://gitlab.com/neurosdk2/neurosamples/-/tree/main/python -- Lets try running this in class monday!

def on_signal_received(sensor, data):
    raw_channels = [support_classes.RawChannels]
    for sample in data:
        left_bipolar = sample.T3-sample.O1
        right_bipolar = sample.T4-sample.O2
        raw_channels.append(support_classes.RawChannels(left_bipolar, right_bipolar))

    math.push_data(raw_channels)
    math.process_data_arr()
    if not math.calibration_finished():
        print(f'Artifacted: {math.is_both_sides_artifacted()}')
        print(f'Calibration percents: {math.get_calibration_percents()}')
    else:
        print(f'Artifacted: {math.is_artifacted_sequence()}')
        print(f'Mental data: {math.read_mental_data_arr()}')
        print(f'Spectral data: {math.read_spectral_data_percents_arr()}')

    print(data)

try:
    scanner = Scanner([SensorFamily.LEBrainBit, SensorFamily.LEBrainBitBlack])

    scanner.sensorsChanged = sensor_found
    scanner.start()
    print("Starting search for 5 sec...")
    sleep(5)
    scanner.stop()

    sensorsInfo = scanner.sensors()
    for i in range(len(sensorsInfo)):
        current_sensor_info = sensorsInfo[i]
        print(sensorsInfo[i])


        def device_connection(sensor_info):
            return scanner.create_sensor(sensor_info)


        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(device_connection, current_sensor_info)
            sensor = future.result()
            print("Device connected")

        sensor.sensorStateChanged = on_sensor_state_changed
        sensor.batteryChanged = on_battery_changed

        if sensor.is_supported_feature(SensorFeature.Signal):
            sensor.signalDataReceived = on_signal_received


        # init emotions lib
        calibration_length = 8
        nwins_skip_after_artifact = 10

        mls = lib_settings.MathLibSetting(sampling_rate=250,
                             process_win_freq=25,
                             fft_window=1000,
                             n_first_sec_skipped=4,
                             bipolar_mode=True,
                             channels_number=4,
                             channel_for_analysis=3)
        ads = lib_settings.ArtifactDetectSetting(hanning_win_spectrum=True, num_wins_for_quality_avg=125)
        sads = lib_settings.ShortArtifactDetectSetting(ampl_art_extremum_border=25)
        mss = lib_settings.MentalAndSpectralSetting()

        math = emotional_math.EmotionalMath(mls, ads, sads, mss) 

        logger.debug("EMOTIONS HERE")
        logger.debug(math) ## This is a Data Structure Including the emotions from the Headband.
        logger.debug("END OF EMOTIONS HERE")
        
        math.set_calibration_length(calibration_length)
        math.set_mental_estimation_mode(False)
        math.set_skip_wins_after_artifact(nwins_skip_after_artifact)
        math.set_zero_spect_waves(True, 0, 1, 1, 1, 0)
        math.set_spect_normalization_by_bands_width(True)

        if sensor.is_supported_command(SensorCommand.StartSignal):
            sensor.exec_command(SensorCommand.StartSignal)
            print("Start signal")
            math.start_calibration()
            sleep(120)
            sensor.exec_command(SensorCommand.StopSignal)
            print("Stop signal")

        sensor.disconnect()
        print("Disconnect from sensor")
        del sensor
        del math

    del scanner
    print('Remove scanner')
except Exception as err:
    print(err)

