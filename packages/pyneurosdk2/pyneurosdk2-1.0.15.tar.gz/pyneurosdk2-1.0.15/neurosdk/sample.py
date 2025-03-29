from threading import Thread

from neurosdk.sensor import Sensor

from scanner import Scanner
from cmn_types import *

from time import sleep


def sensor_found(scanner, sensors):
    for index in range(len(sensors)):
        print('Sensor found: %s' % sensors[index])


def on_sensor_state_changed(sensor, state):
    print('Sensor {0} is {1}'.format(sensor.name, state))


def on_battery_changed(sensor, battery):
    print('Battery: {0}'.format(battery))


def on_fpg_data_received(sensor, data):
    print('FPG: {0}'.format(data))


def on_amp_mode_changed(sensor: Sensor, mode: SensorAmpMode):
    print('Amp mode: {0}'.format(mode))


def on_signal_resist_data_received(sensor, signal, resist):
    print('Signal: {0}'.format(signal))
    print('Resist: {0}'.format(resist))


def on_signal_data_received(sensor: Sensor, data):
    print(data)


def on_resist_data_received(sensor: Sensor, data):
    print(data)


def on_electrodes_state_changed(sensor, data):
    print(data)


def on_envelope_received(sensor, data):
    print(data)


def on_respiration_data_received(sensor, data):
    print(data)


try:
    scanner = Scanner([SensorFamily.LEBrainBit,
                       SensorFamily.LECallibri,
                       SensorFamily.LEBrainBit2,
                       SensorFamily.LEHeadPhones2,
                       SensorFamily.LEHeadband,
                       SensorFamily.LENeuroEEG])

    scanner.sensorsChanged = sensor_found
    scanner.start()
    print("Starting search for 5 sec...")
    sleep(5)
    scanner.stop()

    sensorsInfo = scanner.sensors()
    for i in range(len(sensorsInfo)):
        current_sensor_info = sensorsInfo[i]
        print(sensorsInfo[i])
        sensor = scanner.create_sensor(sensorsInfo[i])
        sensor.sensorStateChanged = on_sensor_state_changed
        sensor.batteryChanged = on_battery_changed

        print(sensor.sens_family)
        print(sensor.features)
        print(sensor.commands)
        print(sensor.parameters)
        print(sensor.name)
        print(sensor.state)
        print(sensor.address)
        print(sensor.serial_number)
        print(sensor.batt_power)
        print(sensor.sampling_frequency)
        if sensor.is_supported_parameter(SensorParameter.Gain):
            print(sensor.gain)
        print(sensor.data_offset)
        print(sensor.version)

        if sensor.sens_family == SensorFamily.LECallibri:
            sensor.data_offset = SensorDataOffset.DataOffset3
            sensor.gain = SensorGain.Gain6
            sensor.ext_sw_input = SensorExternalSwitchInput.Electrodes
            sensor.signal_type = CallibriSignalType.ECG

        if sensor.sens_family == SensorFamily.LEBrainBit2 or sensor.sens_family == SensorFamily.LEBrainBitPro or sensor.sens_family == SensorFamily.LEBrainBitFlex:
            amp_param = sensor.amplifier_param
            ch_count = sensor.channels_count
            amp_param.ChGain = [SensorGain.Gain6 for i in range(ch_count)]
            amp_param.ChSignalMode = [BrainBit2ChannelMode.ChModeNormal for i in range(ch_count)]
            amp_param.ChResistUse = [True for i in range(ch_count)]
            amp_param.Current = GenCurrent.GenCurr6nA
            sensor.amplifier_param = amp_param
            print('Amp param: {0}'.format(sensor.amplifier_param))
            s_ch = sensor.supported_channels
            print('Supported channels: {0}'.format(s_ch))

        if sensor.sens_family == SensorFamily.LENeuroEEG:
            s_ch = sensor.supported_channels
            print('Supported channels: {0}'.format(s_ch))

            ch_count = sensor.channels_count
            print('Ch count: {0}'.format(ch_count))
            a_p = sensor.amplifier_param
            print('Start AmpParam: {0}'.format(a_p))
            a_p.ReferentResistMesureAllow = True
            a_p.Frequency = SensorSamplingFrequency.FrequencyHz250
            a_p.ChannelGain = [SensorGain.Gain6 for i in range(ch_count)]
            a_p.ChannelMode = [EEGChannelMode.EEGChModeSignalResist for i in range(ch_count)]
            sensor.amplifier_param = a_p
            print('New AmpParam: {0}'.format(sensor.amplifier_param))

        if sensor.is_supported_parameter(SensorParameter.Amplifier):
            print(sensor.amp_mode)
            sensor.sensorAmpModeChanged = on_amp_mode_changed

        if sensor.is_supported_parameter(SensorParameter.HardwareFilterState):
            if sensor.is_supported_filter(SensorFilter.BSFBwhLvl2CutoffFreq45_55Hz):
                sensor.hardware_filters = [SensorFilter.BSFBwhLvl2CutoffFreq45_55Hz]

        if sensor.is_supported_feature(SensorFeature.Signal):
            sensor.signalDataReceived = on_signal_data_received

        if sensor.is_supported_parameter(SensorParameter.ElectrodeState):
            print(sensor.electrode_state)
            sensor.electrodeStateChanged = on_electrodes_state_changed

        if sensor.is_supported_feature(SensorFeature.FPG):
            sensor.fpgDataReceived = on_fpg_data_received

        if sensor.is_supported_feature(SensorFeature.Resist):
            sensor.resistDataReceived = on_resist_data_received

        if sensor.is_supported_feature(SensorFeature.Respiration):
            sensor.respirationDataReceived = on_respiration_data_received

        if sensor.is_supported_feature(SensorFeature.Envelope):
            sensor.envelopeDataReceived = on_envelope_received

        if sensor.is_supported_command(SensorCommand.StartSignal):
            sensor.exec_command(SensorCommand.StartSignal)
            print("Start signal")
            sleep(5)
            sensor.exec_command(SensorCommand.StopSignal)
            print("Stop signal")

        if sensor.is_supported_command(SensorCommand.StartResist):
            sensor.exec_command(SensorCommand.StartResist)
            print("Start resist")
            sleep(5)
            sensor.exec_command(SensorCommand.StopResist)
            print("Stop resist")

        if sensor.is_supported_command(SensorCommand.StartEnvelope):
            sensor.exec_command(SensorCommand.StartEnvelope)
            print("Start envelope")
            sleep(5)
            sensor.exec_command(SensorCommand.StopEnvelope)
            print("Stop envelope")

        if sensor.is_supported_command(SensorCommand.StartRespiration):
            sensor.exec_command(SensorCommand.StartRespiration)
            print("Start respiration")
            sleep(5)
            sensor.exec_command(SensorCommand.StopRespiration)
            print("Stop respiration")

        if sensor.is_supported_command(SensorCommand.StartFPG):
            sensor.exec_command(SensorCommand.StartFPG)
            print("Start FPG")
            sleep(5)
            sensor.exec_command(SensorCommand.StopFPG)
            print("Stop FPG")

        if sensor.is_supported_command(SensorCommand.StartCurrentStimulation):
            sensor.exec_command(SensorCommand.StartCurrentStimulation)
            print("Start CurrentStimulation")
            sleep(5)
            sensor.exec_command(SensorCommand.StopCurrentStimulation)
            print("Stop CurrentStimulation")

        if sensor.is_supported_command(SensorCommand.StartSignalAndResist):
            sensor.signalResistDataReceived = on_signal_resist_data_received
            sensor.exec_command(SensorCommand.StartSignalAndResist)
            print("Start signal and resist")
            sleep(5)
            sensor.exec_command(SensorCommand.StopSignalAndResist)
            print("Stop signal and resist")

        sensor.disconnect()
        print("Disconnect from sensor")
        del sensor

    del scanner
    print('Remove scanner')
except Exception as err:
    print(err)
