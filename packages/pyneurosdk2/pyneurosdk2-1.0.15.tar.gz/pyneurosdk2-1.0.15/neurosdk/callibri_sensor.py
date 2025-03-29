import contextlib
from builtins import super

from neurosdk.electrode_sensor import ElectrodeSensor
from neurosdk.envelope_sensor import EnvelopeSensor
from neurosdk.mems_sensor import MemsSensor
from neurosdk.respiration_sensor import RespirationSensor
from neurosdk.sensor import Sensor, _neuro_lib
from neurosdk.__utils import raise_exception_if
from neurosdk.__cmn_types import *
from neurosdk.cmn_types import *
from neurosdk.signal_sensor import SignalSensor


class CallibriSensor(MemsSensor, RespirationSensor, SignalSensor, EnvelopeSensor, ElectrodeSensor):
    def __init__(self, ptr):
        super().__init__(ptr)
        # signatures
        _neuro_lib.getSupportedFiltersCountSensor.argtypes = [SensorPointer]
        _neuro_lib.getSupportedFiltersCountSensor.restype = c_int32
        _neuro_lib.getSupportedFiltersSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(c_int32), POINTER(OpStatus)]
        _neuro_lib.getSupportedFiltersSensor.restype = c_int8
        _neuro_lib.isSupportedFilterSensor.argtypes = [SensorPointer, c_int8]
        _neuro_lib.isSupportedFilterSensor.restype = c_int8
        _neuro_lib.readHardwareFiltersSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(c_int32),
                                                         POINTER(OpStatus)]
        _neuro_lib.readHardwareFiltersSensor.restype = c_uint8
        _neuro_lib.writeHardwareFiltersSensor.argtypes = [SensorPointer, POINTER(c_int8), c_int32, POINTER(OpStatus)]
        _neuro_lib.writeHardwareFiltersSensor.restype = c_uint8
        _neuro_lib.writeSamplingFrequencySensor.argtypes = [SensorPointer, c_int8, POINTER(OpStatus)]
        _neuro_lib.writeSamplingFrequencySensor.restype = c_uint8
        _neuro_lib.writeGainSensor.argtypes = [SensorPointer, c_int8, POINTER(OpStatus)]
        _neuro_lib.writeGainSensor.restype = c_uint8
        _neuro_lib.writeDataOffsetSensor.argtypes = [SensorPointer, c_uint8, POINTER(OpStatus)]
        _neuro_lib.writeDataOffsetSensor.restype = c_uint8
        _neuro_lib.readExternalSwitchSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(OpStatus)]
        _neuro_lib.readExternalSwitchSensor.restype = c_uint8
        _neuro_lib.writeExternalSwitchSensor.argtypes = [SensorPointer, c_int8, POINTER(OpStatus)]
        _neuro_lib.writeExternalSwitchSensor.restype = c_uint8
        _neuro_lib.readADCInputSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(OpStatus)]
        _neuro_lib.readADCInputSensor.restype = c_uint8
        _neuro_lib.writeADCInputSensor.argtypes = [SensorPointer, c_int8, POINTER(OpStatus)]
        _neuro_lib.writeADCInputSensor.restype = c_uint8
        _neuro_lib.writeFirmwareModeSensor.argtypes = [SensorPointer, c_int8, POINTER(OpStatus)]
        _neuro_lib.writeFirmwareModeSensor.restype = c_uint8
        _neuro_lib.readStimulatorAndMAStateCallibri.argtypes = [SensorPointer, POINTER(NativeCallibriStimulatorMAState),
                                                                POINTER(OpStatus)]
        _neuro_lib.readStimulatorAndMAStateCallibri.restype = c_uint8
        _neuro_lib.readStimulatorParamCallibri.argtypes = [SensorPointer, POINTER(NativeCallibriStimulationParams),
                                                           POINTER(OpStatus)]
        _neuro_lib.readStimulatorParamCallibri.restype = c_uint8
        _neuro_lib.writeStimulatorParamCallibri.argtypes = [SensorPointer, NativeCallibriStimulationParams,
                                                            POINTER(OpStatus)]
        _neuro_lib.writeStimulatorParamCallibri.restype = c_uint8
        _neuro_lib.readMotionAssistantParamCallibri.argtypes = [SensorPointer,
                                                                POINTER(NativeCallibriMotionAssistantParams),
                                                                POINTER(OpStatus)]
        _neuro_lib.readMotionAssistantParamCallibri.restype = c_uint8
        _neuro_lib.writeMotionAssistantParamCallibri.argtypes = [SensorPointer, NativeCallibriMotionAssistantParams,
                                                                 POINTER(OpStatus)]
        _neuro_lib.writeMotionAssistantParamCallibri.restype = c_uint8
        _neuro_lib.readMotionCounterParamCallibri.argtypes = [SensorPointer, POINTER(NativeCallibriMotionCounterParam),
                                                              POINTER(OpStatus)]
        _neuro_lib.readMotionCounterParamCallibri.restype = c_uint8
        _neuro_lib.writeMotionCounterParamCallibri.argtypes = [SensorPointer, NativeCallibriMotionCounterParam,
                                                               POINTER(OpStatus)]
        _neuro_lib.writeMotionCounterParamCallibri.restype = c_uint8
        _neuro_lib.readMotionCounterCallibri.argtypes = [SensorPointer, POINTER(c_uint32), POINTER(OpStatus)]
        _neuro_lib.readMotionCounterCallibri.restype = c_uint8
        _neuro_lib.readColorCallibri.argtypes = [SensorPointer, POINTER(c_int), POINTER(OpStatus)]
        _neuro_lib.readColorCallibri.restype = c_uint8
        _neuro_lib.setSignalSettingsCallibri.argtypes = [SensorPointer, c_uint8, POINTER(OpStatus)]
        _neuro_lib.setSignalSettingsCallibri.restype = c_uint8
        _neuro_lib.getSignalSettingsCallibri.argtypes = [SensorPointer, POINTER(c_int), POINTER(OpStatus)]
        _neuro_lib.getSignalSettingsCallibri.restype = c_uint8
        _neuro_lib.readMEMSCalibrateStateCallibri.argtypes = [SensorPointer, POINTER(c_uint8), POINTER(OpStatus)]
        _neuro_lib.readMEMSCalibrateStateCallibri.restype = c_uint8
        _neuro_lib.addQuaternionDataCallback.argtypes = [SensorPointer, QuaternionDataCallback, c_void_p,
                                                         ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addQuaternionDataCallback.restype = c_uint8
        _neuro_lib.removeQuaternionDataCallback.argtypes = [QuaternionDataListenerHandle]
        _neuro_lib.removeQuaternionDataCallback.restype = c_void_p
        _neuro_lib.addSignalCallbackCallibri.argtypes = [SensorPointer, SignalCallbackCallibri, c_void_p,
                                                         ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addSignalCallbackCallibri.restype = c_uint8
        _neuro_lib.removeSignalCallbackCallibri.argtypes = [CallibriSignalDataListenerHandle]
        _neuro_lib.removeSignalCallbackCallibri.restype = c_void_p
        _neuro_lib.addRespirationCallbackCallibri.argtypes = [SensorPointer, RespirationCallbackCallibri, c_void_p,
                                                              ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addRespirationCallbackCallibri.restype = c_uint8
        _neuro_lib.removeRespirationCallbackCallibri.argtypes = [CallibriRespirationDataListenerHandle]
        _neuro_lib.removeRespirationCallbackCallibri.restype = c_void_p
        _neuro_lib.addElectrodeStateCallbackCallibri.argtypes = [SensorPointer, ElectrodeStateCallbackCallibri,
                                                                 c_void_p, ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addElectrodeStateCallbackCallibri.restype = c_uint8
        _neuro_lib.removeElectrodeStateCallbackCallibri.argtypes = [CallibriElectrodeStateListenerHandle]
        _neuro_lib.removeElectrodeStateCallbackCallibri.restype = c_void_p
        _neuro_lib.addEnvelopeDataCallbackCallibri.argtypes = [SensorPointer, EnvelopeDataCallbackCallibri, c_void_p,
                                                               ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addEnvelopeDataCallbackCallibri.restype = c_uint8
        _neuro_lib.removeEnvelopeDataCallbackCallibri.argtypes = [CallibriEnvelopeDataListenerHandle]
        _neuro_lib.removeEnvelopeDataCallbackCallibri.restype = c_void_p
        if self.is_supported_feature(SensorFeature.MEMS):
            self.quaternionDataReceived = None
            self.__add_quaternion_data_callback()

    def __del__(self):
        with contextlib.suppress(Exception):
            if not self.__closed:
                self.__closed = True
                self.quaternionDataReceived = None
                _neuro_lib.removeQuaternionDataCallback(self.__quaternionDataCallbackHandle)
        super().__del__()

    def set_signal_callbacks(self):
        self.__add_signal_callback_callibri()

    def unset_signal_callbacks(self):
        _neuro_lib.removeSignalCallbackCallibri(self.__signalCallbackCallibriHandle)

    def set_envelope_callbacks(self):
        self.__add_envelope_data_callback_callibri()

    def unset_envelope_callbacks(self):
        _neuro_lib.removeEnvelopeDataCallbackCallibri(self.__envelopeDataCallbackCallibriHandle)

    def set_respiration_callbacks(self):
        self.__add_respiration_callback_callibri()

    def unset_respiration_callbacks(self):
        _neuro_lib.removeRespirationCallbackCallibri(self.__respirationCallbackCallibriHandle)

    def set_electrode_callbacks(self):
        self.__add_electrode_state_callback_callibri()

    def unset_electrode_callbacks(self):
        _neuro_lib.removeElectrodeStateCallbackCallibri(self.__electrodeStateCallbackCallibriHandle)

    @Sensor.sampling_frequency.setter
    def sampling_frequency(self, sf: SensorSamplingFrequency):
        status = OpStatus()
        _neuro_lib.writeSamplingFrequencySensor(self.sensor_ptr, sf.value, byref(status))
        raise_exception_if(status)

    def is_supported_filter(self, sensor_filter: SensorFilter) -> bool:
        status = OpStatus()
        supported = _neuro_lib.isSupportedFilterSensor(self.sensor_ptr, sensor_filter.value, byref(status))
        return bool(int(supported))
    
    @property
    def supported_filters(self) -> list[SensorFilter]:
        status = OpStatus()
        filters_out = EnumType(c_int8())
        count = _neuro_lib.getSupportedFiltersCountSensor(self.sensor_ptr)
        sz_filters_in_out = SizeType(c_int32(count))
        _neuro_lib.getSupportedFiltersSensor(self.sensor_ptr, filters_out, sz_filters_in_out, byref(status))
        raise_exception_if(status)
        return [SensorFilter(filters_out[i]) for i in range(sz_filters_in_out.contents.value)]

    @property
    def hardware_filters(self) -> list[SensorFilter]:
        status = OpStatus()
        filters_out = EnumType(c_int8())
        sz_filters_in_out = SizeType(c_int32(64))
        _neuro_lib.readHardwareFiltersSensor(self.sensor_ptr, filters_out, sz_filters_in_out, byref(status))
        raise_exception_if(status)
        return [SensorFilter(filters_out[i]) for i in range(sz_filters_in_out.contents.value)]

    @hardware_filters.setter
    def hardware_filters(self, filters: list):
        status = OpStatus()
        filters_len = len(filters)
        filters_values = (c_int8 * filters_len)(*[filters[i].value for i in range(filters_len)])
        _neuro_lib.writeHardwareFiltersSensor(self.sensor_ptr, filters_values, filters_len, byref(status))
        raise_exception_if(status)

    @Sensor.data_offset.setter
    def data_offset(self, do: SensorDataOffset):
        status = OpStatus()
        _neuro_lib.writeDataOffsetSensor(self.sensor_ptr, do.value, byref(status))
        raise_exception_if(status)

    @property
    def ext_sw_input(self) -> SensorExternalSwitchInput:
        status = OpStatus()
        ext_sw_input_val = EnumType(c_int8(1))
        _neuro_lib.readExternalSwitchSensor(self.sensor_ptr, ext_sw_input_val, byref(status))
        raise_exception_if(status)
        return SensorExternalSwitchInput(ext_sw_input_val.contents.value)

    @ext_sw_input.setter
    def ext_sw_input(self, ext_sw_inp: SensorExternalSwitchInput):
        status = OpStatus()
        _neuro_lib.writeExternalSwitchSensor(self.sensor_ptr, ext_sw_inp.value, byref(status))
        raise_exception_if(status)

    @property
    def adc_input(self) -> SensorADCInput:
        status = OpStatus()
        adc_input_val = EnumType(c_int8(1))
        _neuro_lib.readADCInputSensor(self.sensor_ptr, adc_input_val, byref(status))
        raise_exception_if(status)
        return SensorADCInput(adc_input_val.contents.value)

    @adc_input.setter
    def adc_input(self, adc_inp: SensorADCInput):
        status = OpStatus()
        _neuro_lib.writeADCInputSensor(self.sensor_ptr, adc_inp.value, byref(status))
        raise_exception_if(status)

    @MemsSensor.acc_sens.setter
    def acc_sens(self, acc_sens: SensorAccelerometerSensitivity):
        status = OpStatus()
        _neuro_lib.writeAccelerometerSensSensor(self.sensor_ptr, acc_sens.value, byref(status))
        raise_exception_if(status)

    @MemsSensor.gyro_sens.setter
    def gyro_sens(self, gyro_sens: SensorGyroscopeSensitivity):
        status = OpStatus()
        _neuro_lib.writeGyroscopeSensSensor(self.sensor_ptr, gyro_sens.value, byref(status))
        raise_exception_if(status)

    @Sensor.firmware_mode.setter
    def firmware_mode(self, mode: SensorFirmwareMode):
        status = OpStatus()
        _neuro_lib.writeFirmwareModeSensor(self.sensor_ptr, mode.value, byref(status))
        raise_exception_if(status)

    @Sensor.gain.setter
    def gain(self, gain: SensorGain):
        status = OpStatus()
        _neuro_lib.writeGainSensor(self.sensor_ptr, gain.value, byref(status))
        raise_exception_if(status)

    @property
    def stimulator_ma_state(self) -> CallibriStimulatorMAState:
        status = OpStatus()
        csmas = POINTER(NativeCallibriStimulatorMAState)
        ma_state = csmas(NativeCallibriStimulatorMAState())
        _neuro_lib.readStimulatorAndMAStateCallibri(self.sensor_ptr, ma_state, byref(status))
        raise_exception_if(status)
        return CallibriStimulatorMAState(StimulatorState=CallibriStimulatorState(ma_state.contents.StimulatorState),
                                         MAState=CallibriStimulatorState(ma_state.contents.MAState))

    @property
    def stimulator_param(self) -> CallibriStimulationParams:
        status = OpStatus()
        csp = POINTER(NativeCallibriStimulationParams)
        stimulation_params_out = csp(NativeCallibriStimulationParams())
        _neuro_lib.readStimulatorParamCallibri(self.sensor_ptr, stimulation_params_out, byref(status))
        raise_exception_if(status)
        return CallibriStimulationParams(Current=int(stimulation_params_out.contents.Current),
                                         PulseWidth=int(stimulation_params_out.contents.PulseWidth),
                                         Frequency=int(stimulation_params_out.contents.Frequency),
                                         StimulusDuration=int(stimulation_params_out.contents.StimulusDuration))

    @stimulator_param.setter
    def stimulator_param(self, params: CallibriStimulationParams):
        status = OpStatus()
        stim_params = NativeCallibriStimulationParams()
        stim_params.Current = params.Current
        stim_params.PulseWidth = params.PulseWidth
        stim_params.Frequency = params.Frequency
        stim_params.StimulusDuration = params.StimulusDuration
        _neuro_lib.writeStimulatorParamCallibri(self.sensor_ptr, stim_params, byref(status))
        raise_exception_if(status)

    @property
    def motion_assistant_param(self) -> CallibriMotionAssistantParams:
        status = OpStatus()
        cmap = POINTER(NativeCallibriMotionAssistantParams)
        motion_assistant_params_out = cmap(NativeCallibriMotionAssistantParams())
        _neuro_lib.readMotionAssistantParamCallibri(self.sensor_ptr, motion_assistant_params_out, byref(status))
        raise_exception_if(status)
        return CallibriMotionAssistantParams(GyroStart=motion_assistant_params_out.contents.GyroStart,
                                             GyroStop=motion_assistant_params_out.contents.GyroStop,
                                             Limb=motion_assistant_params_out.contents.Limb,
                                             MinPauseMs=motion_assistant_params_out.contents.MinPauseMs)

    @motion_assistant_param.setter
    def motion_assistant_param(self, params: CallibriMotionAssistantParams):
        status = OpStatus()
        stimulation_params = NativeCallibriMotionAssistantParams()
        stimulation_params.GyroStart = params.GyroStart
        stimulation_params.GyroStop = params.GyroStop
        stimulation_params.Limb = params.Limb.value[0]
        stimulation_params.MinPauseMs = params.MinPauseMs
        _neuro_lib.writeMotionAssistantParamCallibri(self.sensor_ptr, stimulation_params, byref(status))
        raise_exception_if(status)

    @property
    def motion_counter_param(self) -> CallibriMotionCounterParam:
        status = OpStatus()
        cmcp = POINTER(NativeCallibriMotionCounterParam)
        motion_counter_param_out = cmcp(NativeCallibriMotionCounterParam())
        _neuro_lib.readMotionCounterParamCallibri(self.sensor_ptr, motion_counter_param_out, byref(status))
        raise_exception_if(status)
        return CallibriMotionCounterParam(InsenseThresholdMG=motion_counter_param_out.contents.InsenseThresholdMG,
                                          InsenseThresholdSample=motion_counter_param_out.contents.
                                          InsenseThresholdSample)

    @motion_counter_param.setter
    def motion_counter_param(self, params: CallibriMotionCounterParam):
        status = OpStatus()
        motion_counter_param = NativeCallibriMotionCounterParam()
        motion_counter_param.InsenseThresholdMG = params.InsenseThresholdMG
        motion_counter_param.InsenseThresholdSample = params.InsenseThresholdSample
        _neuro_lib.writeMotionCounterParamCallibri(self.sensor_ptr, motion_counter_param, byref(status))
        raise_exception_if(status)

    @property
    def motion_counter(self) -> int:
        status = OpStatus()
        enum_type = POINTER(c_uint32)
        motion_counter_out = enum_type(c_uint32(1))
        _neuro_lib.readMotionCounterCallibri(self.sensor_ptr, motion_counter_out, byref(status))
        raise_exception_if(status)
        return int(motion_counter_out.contents.value)

    @property
    def color(self) -> CallibriColorType:
        status = OpStatus()
        callibri_color_out = EnumType(c_uint8(1))
        _neuro_lib.readColorCallibri(self.sensor_ptr, callibri_color_out, byref(status))
        raise_exception_if(status)
        return CallibriColorType(callibri_color_out.contents.value)

    @property
    def signal_type(self) -> CallibriSignalType:
        status = OpStatus()
        callibri_signal_type_out = EnumType(c_uint8(1))
        _neuro_lib.getSignalSettingsCallibri(self.sensor_ptr, callibri_signal_type_out, byref(status))
        raise_exception_if(status)
        return CallibriSignalType(callibri_signal_type_out.contents.value)

    @signal_type.setter
    def signal_type(self, signal_type: CallibriSignalType):
        status = OpStatus()
        _neuro_lib.setSignalSettingsCallibri(self.sensor_ptr, signal_type.value, byref(status))
        raise_exception_if(status)

    @property
    def mems_calibrate_state(self) -> bool:
        status = OpStatus()
        state_out = EnumType(c_uint8(0))
        _neuro_lib.readMEMSCalibrateStateCallibri(self.sensor_ptr, state_out, byref(status))
        raise_exception_if(status)
        return bool(int(state_out))

    def __add_electrode_state_callback_callibri(self):
        def __py_electrode_state_callback_callibri(ptr, state, user_data):
            if user_data.electrodeStateChanged is not None:
                user_data.electrodeStateChanged(user_data, CallibriElectrodeState(state))

        status = OpStatus()
        self.__electrodeStateCallbackCallibri = ElectrodeStateCallbackCallibri(__py_electrode_state_callback_callibri)
        self.__electrodeStateCallbackCallibriHandle = CallibriElectrodeStateListenerHandle()
        _neuro_lib.addElectrodeStateCallbackCallibri(self.sensor_ptr, self.__electrodeStateCallbackCallibri,
                                                     byref(self.__electrodeStateCallbackCallibriHandle),
                                                     py_object(self), byref(status))
        raise_exception_if(status)

    def __add_signal_callback_callibri(self):
        def __py_signal_callback_callibri(ptr, data, sz_data, user_data):
            signal_data = [CallibriSignalData(PackNum=int(data[i].PackNum),
                                              Samples=[float(data[i].Samples[j]) for j in range(data[i].SzSamples)])
                           for i in range(sz_data)]
            if user_data.signalDataReceived is not None:
                user_data.signalDataReceived(user_data, signal_data)

        status = OpStatus()
        self.__signalCallbackCallibri = SignalCallbackCallibri(__py_signal_callback_callibri)
        self.__signalCallbackCallibriHandle = CallibriSignalDataListenerHandle()
        _neuro_lib.addSignalCallbackCallibri(self.sensor_ptr, self.__signalCallbackCallibri,
                                             byref(self.__signalCallbackCallibriHandle),
                                             py_object(self), byref(status))
        raise_exception_if(status)

    def __add_quaternion_data_callback(self):
        def __py_quaternion_data_callback(ptr, data, sz_data, user_data):
            qa_data = [QuaternionData(PackNum=int(data[i].PackNum),
                                      W=data[i].W,
                                      X=data[i].X,
                                      Y=data[i].Y,
                                      Z=data[i].Z) for i in range(sz_data)]
            if user_data.quaternionDataReceived is not None:
                user_data.quaternionDataReceived(user_data, qa_data)

        status = OpStatus()
        self.__quaternionDataCallback = QuaternionDataCallback(__py_quaternion_data_callback)
        self.__quaternionDataCallbackHandle = QuaternionDataListenerHandle()
        _neuro_lib.addQuaternionDataCallback(self.sensor_ptr, self.__quaternionDataCallback,
                                             byref(self.__quaternionDataCallbackHandle),
                                             py_object(self), byref(status))
        raise_exception_if(status)

    def __add_respiration_callback_callibri(self):
        def __py_respiration_callback_callibri(ptr, data, sz_data, user_data):
            resp_data = [CallibriRespirationData(PackNum=int(data[i].PackNum),
                                                 Samples=[float(data[i].Samples[j]) for j in range(data[i].SzSamples)])
                         for i in range(sz_data)]
            if user_data.respirationDataReceived is not None:
                user_data.respirationDataReceived(user_data, resp_data)

        status = OpStatus()
        self.__respirationCallbackCallibri = RespirationCallbackCallibri(__py_respiration_callback_callibri)
        self.__respirationCallbackCallibriHandle = CallibriRespirationDataListenerHandle()
        _neuro_lib.addRespirationCallbackCallibri(self.sensor_ptr, self.__respirationCallbackCallibri,
                                                  byref(self.__respirationCallbackCallibriHandle),
                                                  py_object(self), byref(status))
        raise_exception_if(status)

    def __add_envelope_data_callback_callibri(self):
        def __py_envelope_data_callback_callibri(ptr, data, sz_data, user_data):
            env_data = [CallibriEnvelopeData(PackNum=int(data[i].PackNum),
                                             Sample=float(data[i].Sample))
                        for i in range(sz_data)]
            if user_data.envelopeDataReceived is not None:
                user_data.envelopeDataReceived(user_data, env_data)

        status = OpStatus()
        self.__envelopeDataCallbackCallibri = EnvelopeDataCallbackCallibri(__py_envelope_data_callback_callibri)
        self.__envelopeDataCallbackCallibriHandle = CallibriEnvelopeDataListenerHandle()
        _neuro_lib.addEnvelopeDataCallbackCallibri(self.sensor_ptr, self.__envelopeDataCallbackCallibri,
                                                   byref(self.__envelopeDataCallbackCallibriHandle),
                                                   py_object(self), byref(status))
        raise_exception_if(status)
