from neurosdk.__utils import raise_exception_if
from neurosdk.__cmn_types import *
from neurosdk.amp_sensor import AmpSensor
from neurosdk.cmn_types import *
from neurosdk.neuro_smart_sensor import NeuroSmartSensor
from neurosdk.resist_sensor import ResistSensor
from neurosdk.sensor import Sensor, _neuro_lib
from neurosdk.signal_sensor import SignalSensor


class Headphones2Sensor(SignalSensor, ResistSensor, AmpSensor, NeuroSmartSensor):
    def __init__(self, ptr):
        super().__init__(ptr)
        # signatures
        _neuro_lib.readAmplifierParamHeadphones2.argtypes = [SensorPointer, POINTER(NativeHeadphones2AmplifierParam),
                                                             POINTER(OpStatus)]
        _neuro_lib.readAmplifierParamHeadphones2.restype = c_uint8
        _neuro_lib.writeAmplifierParamHeadphones2.argtypes = [SensorPointer, NativeHeadphones2AmplifierParam,
                                                              POINTER(OpStatus)]
        _neuro_lib.writeAmplifierParamHeadphones2.restype = c_uint8
        _neuro_lib.addResistCallbackHeadphones2.argtypes = [SensorPointer, ResistCallbackHeadphones2, c_void_p,
                                                            ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addResistCallbackHeadphones2.restype = c_uint8
        _neuro_lib.removeResistCallbackHeadphones2.argtypes = [Headphones2ResistDataListenerHandle]
        _neuro_lib.removeResistCallbackHeadphones2.restype = c_void_p
        _neuro_lib.addSignalDataCallbackHeadphones2.argtypes = [SensorPointer, SignalDataCallbackHeadphones2, c_void_p,
                                                                ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addSignalDataCallbackHeadphones2.restype = c_uint8
        _neuro_lib.removeSignalDataCallbackHeadphones2.argtypes = [Headphones2SignalDataListenerHandle]
        _neuro_lib.removeSignalDataCallbackHeadphones2.restype = c_void_p

    def set_signal_callbacks(self):
        self.__add_signal_data_callback_headphones2()

    def unset_signal_callbacks(self):
        _neuro_lib.removeSignalDataCallbackHeadphones2(self.__signalDataCallbackHeadphones2Handle)

    def set_resist_callbacks(self):
        self.__add_resist_callback_headphones2()

    def unset_resist_callbacks(self):
        _neuro_lib.removeResistCallbackHeadphones2(self.__resistCallbackHeadphones2Handle)

    def __add_resist_callback_headphones2(self):
        def __py_resist_callback_headphones2(ptr, data, sz_data, user_data):
            resist_data = [Headphones2ResistData(PackNum=int(data[i].PackNum),
                                                 Ch1=float(data[i].Ch1),
                                                 Ch2=float(data[i].Ch2),
                                                 Ch3=float(data[i].Ch3),
                                                 Ch4=float(data[i].Ch4)) for i in range(sz_data)]
            if user_data.resistDataReceived is not None:
                user_data.resistDataReceived(user_data, resist_data)

        status = OpStatus()
        self.__resistCallbackHeadphones2 = ResistCallbackHeadphones2(__py_resist_callback_headphones2)
        self.__resistCallbackHeadphones2Handle = Headphones2ResistDataListenerHandle()
        _neuro_lib.addResistCallbackHeadphones2(self.sensor_ptr, self.__resistCallbackHeadphones2,
                                                byref(self.__resistCallbackHeadphones2Handle),
                                                py_object(self), byref(status))
        raise_exception_if(status)

    def __add_signal_data_callback_headphones2(self):
        def __py_signal_data_callback_headphones2(ptr, data, sz_data, user_data):
            signal_data = [Headphones2SignalData(PackNum=int(data[i].PackNum),
                                                 Marker=int(data[i].Marker),
                                                 Ch1=float(data[i].Ch1),
                                                 Ch2=float(data[i].Ch2),
                                                 Ch3=float(data[i].Ch3),
                                                 Ch4=float(data[i].Ch4)) for i in range(sz_data)]
            if user_data.signalDataReceived is not None:
                user_data.signalDataReceived(user_data, signal_data)

        status = OpStatus()
        self.__signalDataCallbackHeadphones2 = SignalDataCallbackHeadphones2(__py_signal_data_callback_headphones2)
        self.__signalDataCallbackHeadphones2Handle = Headphones2SignalDataListenerHandle()
        _neuro_lib.addSignalDataCallbackHeadphones2(self.sensor_ptr,
                                                    self.__signalDataCallbackHeadphones2,
                                                    byref(self.__signalDataCallbackHeadphones2Handle),
                                                    py_object(self), byref(status))
        raise_exception_if(status)

    @property
    def amplifier_param(self) -> Headphones2AmplifierParam:
        status = OpStatus()
        cmap = POINTER(NativeHeadphones2AmplifierParam)
        amplifier_param_out = cmap(NativeHeadphones2AmplifierParam())
        _neuro_lib.readAmplifierParamHeadphones2(self.sensor_ptr, amplifier_param_out, byref(status))
        raise_exception_if(status)
        return Headphones2AmplifierParam(
            ChSignalUse1=bool(amplifier_param_out.contents.ChSignalUse1),
            ChSignalUse2=bool(amplifier_param_out.contents.ChSignalUse2),
            ChSignalUse3=bool(amplifier_param_out.contents.ChSignalUse3),
            ChSignalUse4=bool(amplifier_param_out.contents.ChSignalUse4),
            ChResistUse1=bool(amplifier_param_out.contents.ChResistUse1),
            ChResistUse2=bool(amplifier_param_out.contents.ChResistUse2),
            ChResistUse3=bool(amplifier_param_out.contents.ChResistUse3),
            ChResistUse4=bool(amplifier_param_out.contents.ChResistUse4),
            ChGain1=SensorGain(amplifier_param_out.contents.ChGain1),
            ChGain2=SensorGain(amplifier_param_out.contents.ChGain2),
            ChGain3=SensorGain(amplifier_param_out.contents.ChGain3),
            ChGain4=SensorGain(amplifier_param_out.contents.ChGain4),
            Current=GenCurrent(amplifier_param_out.contents.Current))

    @amplifier_param.setter
    def amplifier_param(self, params: Headphones2AmplifierParam):
        status = OpStatus()
        amplifier_param = NativeHeadphones2AmplifierParam()
        amplifier_param.ChSignalUse1=params.ChSignalUse1
        amplifier_param.ChSignalUse2=params.ChSignalUse2
        amplifier_param.ChSignalUse3=params.ChSignalUse3
        amplifier_param.ChSignalUse4=params.ChSignalUse4
        amplifier_param.ChResistUse1 = params.ChResistUse1
        amplifier_param.ChResistUse2 = params.ChResistUse2
        amplifier_param.ChResistUse3 = params.ChResistUse3
        amplifier_param.ChResistUse4 = params.ChResistUse4
        amplifier_param.ChGain1 = params.ChGain1.value
        amplifier_param.ChGain2 = params.ChGain2.value
        amplifier_param.ChGain3 = params.ChGain3.value
        amplifier_param.ChGain4 = params.ChGain4.value
        amplifier_param.Current = params.Current.value
        _neuro_lib.writeAmplifierParamHeadphones2(self.sensor_ptr, amplifier_param, byref(status))
        raise_exception_if(status)
