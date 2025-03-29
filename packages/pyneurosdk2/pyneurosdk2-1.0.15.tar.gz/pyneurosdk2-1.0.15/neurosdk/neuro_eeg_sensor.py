import contextlib
import ctypes
from ctypes import c_uint8, c_uint32, c_void_p, c_double

from _ctypes import byref, POINTER
from neurosdk.amp_sensor import AmpSensor
from neurosdk.signal_resist_sensor import SignalResistSensor
from neurosdk.neuro_smart_sensor import NeuroSmartSensor
from neurosdk.resist_sensor import ResistSensor
from neurosdk.signal_sensor import SignalSensor
from neurosdk.photo_stim_sensor import PhotoStimSensor

from neurosdk.cmn_types import SignalChannelsData, ResistChannelsData, EEGChannelInfo, EEGChannelId, EEGChannelType, \
    NeuroEEGAmplifierParam, SensorSamplingFrequency, EEGRefMode, EEGChannelMode, SensorGain, SensorStimulMode, \
    SensorStimulSyncState, StimulPhase

from neurosdk.__cmn_types import SensorPointer, OpStatus, NativeEEGChannelInfo, NativeResistChannelsData, \
    NativeSignalChannelsData, NeuroEEGSignalDataListenerHandle, NativeNeuroEEGAmplifierParam, \
    SignalDataCallbackNeuroEEG, ResistDataCallbackNeuroEEG, NeuroEEGResistDataListenerHandle, \
    SignalResistDataCallbackNeuroEEG, NeuroEEGSignalResistDataListenerHandle, NeuroEEGSignalRawDataListenerHandle, \
    SignalRawDataCallbackNeuroEEG, NeuroEEGSignalProcessParam, SizeType, NEURO_EEG_MAX_CH_COUNT, NativeStimulPhase, \
    EnumType

from neurosdk.__utils import raise_exception_if



from neurosdk.sensor import _neuro_lib

class NeuroEEGSensor(SignalSensor, ResistSensor, AmpSensor, NeuroSmartSensor, SignalResistSensor):
    def __init__(self, ptr):
        super().__init__(ptr)
        # signatures
        _neuro_lib.readSamplingFrequencyResistSensor.argtypes = [SensorPointer, c_uint8, POINTER(OpStatus)]
        _neuro_lib.readSamplingFrequencyResistSensor.restype = c_uint8

        _neuro_lib.readSupportedChannelsNeuroEEG.argtypes = [SensorPointer, POINTER(NativeEEGChannelInfo), POINTER(
            ctypes.c_int32), POINTER(OpStatus)]
        _neuro_lib.readSupportedChannelsNeuroEEG.restype = ctypes.c_uint8

        _neuro_lib.readPhotoStimNeuroEEG.argtypes = [SensorPointer]
        _neuro_lib.readPhotoStimNeuroEEG.restype = SensorPointer

        _neuro_lib.writePhotoStimNeuroEEG.argtypes = [SensorPointer, SensorPointer, POINTER(OpStatus)]
        _neuro_lib.writePhotoStimNeuroEEG.restype = ctypes.c_uint8

        _neuro_lib.createSignalProcessParamNeuroEEG.argtypes = [NativeNeuroEEGAmplifierParam, POINTER(NeuroEEGSignalProcessParam), POINTER(OpStatus)]
        _neuro_lib.createSignalProcessParamNeuroEEG.restype = ctypes.c_uint8
        _neuro_lib.removeSignalProcessParamNeuroEEG.argtypes = [NeuroEEGSignalProcessParam]
        _neuro_lib.removeSignalProcessParamNeuroEEG.restype = ctypes.c_void_p

        _neuro_lib.parseRawSignalNeuroEEG.argtypes = [POINTER(c_uint8), POINTER(c_uint32), NeuroEEGSignalProcessParam, POINTER(NativeSignalChannelsData), POINTER(c_uint32), POINTER(NativeResistChannelsData), POINTER(c_uint32), POINTER(OpStatus)]
        _neuro_lib.parseRawSignalNeuroEEG.restype = ctypes.c_uint8

        _neuro_lib.readSurveyIdNeuroEEG.argtypes = [SensorPointer, POINTER(c_uint32), POINTER(OpStatus)]
        _neuro_lib.readSurveyIdNeuroEEG.restype = ctypes.c_uint8
        _neuro_lib.writeSurveyIdNeuroEEG.argtypes = [SensorPointer, c_uint32, POINTER(OpStatus)]
        _neuro_lib.writeSurveyIdNeuroEEG.restype = ctypes.c_uint8

        _neuro_lib.readAmplifierParamNeuroEEG.argtypes = [SensorPointer, POINTER(NativeNeuroEEGAmplifierParam), POINTER(OpStatus)]
        _neuro_lib.readAmplifierParamNeuroEEG.restype = ctypes.c_uint8
        _neuro_lib.writeAmplifierParamNeuroEEG.argtypes = [SensorPointer, NativeNeuroEEGAmplifierParam, POINTER(OpStatus)]
        _neuro_lib.writeAmplifierParamNeuroEEG.restype = ctypes.c_uint8

        _neuro_lib.addSignalCallbackNeuroEEG.argtypes = [SensorPointer, SignalDataCallbackNeuroEEG,
                                                         c_void_p, ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addSignalCallbackNeuroEEG.restype = ctypes.c_uint8
        _neuro_lib.removeSignalCallbackNeuroEEG.argtypes = [NeuroEEGSignalDataListenerHandle]
        _neuro_lib.removeSignalCallbackNeuroEEG.restype = ctypes.c_void_p

        _neuro_lib.addResistCallbackNeuroEEG.argtypes = [SensorPointer, ResistDataCallbackNeuroEEG,
                                                         c_void_p, ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addResistCallbackNeuroEEG.restype = ctypes.c_uint8
        _neuro_lib.removeResistCallbackNeuroEEG.argtypes = [NeuroEEGResistDataListenerHandle]
        _neuro_lib.removeResistCallbackNeuroEEG.restype = ctypes.c_void_p

        _neuro_lib.addSignalResistCallbackNeuroEEG.argtypes = [SensorPointer, SignalResistDataCallbackNeuroEEG, c_void_p, ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addSignalResistCallbackNeuroEEG.restype = ctypes.c_uint8
        _neuro_lib.removeSignalResistCallbackNeuroEEG.argtypes = [NeuroEEGSignalResistDataListenerHandle]
        _neuro_lib.removeSignalResistCallbackNeuroEEG.restype = ctypes.c_void_p

        _neuro_lib.addSignalRawCallbackNeuroEEG.argtypes = [SensorPointer, SignalRawDataCallbackNeuroEEG, NeuroEEGSignalRawDataListenerHandle, ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addSignalRawCallbackNeuroEEG.restype = ctypes.c_uint8
        _neuro_lib.removeSignalRawCallbackNeuroEEG.argtypes = [NeuroEEGSignalRawDataListenerHandle]
        _neuro_lib.removeSignalRawCallbackNeuroEEG.restype = ctypes.c_void_p
        
        _neuro_lib.readPhotoStimSyncState.argtypes = [SensorPointer, c_uint8, POINTER(OpStatus)]
        _neuro_lib.readPhotoStimSyncState.restype = c_uint8

        _neuro_lib.readPhotoStimTimeDefer.argtypes = [SensorPointer, POINTER(ctypes.c_double), POINTER(OpStatus)]
        _neuro_lib.readPhotoStimTimeDefer.restype = c_uint8
        _neuro_lib.writePhotoStimTimeDefer.argtypes = [SensorPointer, ctypes.c_double, POINTER(OpStatus)]
        _neuro_lib.writePhotoStimTimeDefer.restype = c_uint8

        _neuro_lib.getMaxStimulPhasesCountSensor.argtypes = [SensorPointer]
        _neuro_lib.getMaxStimulPhasesCountSensor.restype = ctypes.c_int32
        _neuro_lib.readStimMode.argtypes = [SensorPointer, POINTER(c_uint8), POINTER(OpStatus)]
        _neuro_lib.readStimMode.restype = c_uint8
        _neuro_lib.readStimPrograms.argtypes = [SensorPointer, POINTER(NativeStimulPhase), POINTER(ctypes.c_int32), POINTER(OpStatus)]
        _neuro_lib.readStimPrograms.restype = c_uint8
        _neuro_lib.writeStimPrograms.argtypes = [SensorPointer, POINTER(NativeStimulPhase), ctypes.c_int32, POINTER(OpStatus)]
        _neuro_lib.writeStimPrograms.restype = c_uint8

        self._photo_stim_sensor = None


    def __del__(self):
        super().__del__()

    def set_signal_callbacks(self):
        self.__add_signal_data_callback_neuro_eeg()

    def unset_signal_callbacks(self):
        _neuro_lib.removeSignalCallbackNeuroEEG(self.__signalDataCallbackNeuroEEGHandle)

    def set_resist_callbacks(self):
        self.__add_resist_callback_neuro_eeg()

    def unset_resist_callbacks(self):
        _neuro_lib.removeResistCallbackNeuroEEG(self.__resistCallbackNeuroEEGHandle)

    def set_signal_resist_callbacks(self):
        self.__add_signal_resist_callback_neuro_eeg()

    def unset_signal_resist_callbacks(self):
        _neuro_lib.removeSignalResistCallbackNeuroEEG(self.__signalResistCallbackNeuroEEGHandle)

    def __add_signal_data_callback_neuro_eeg(self):
        def __py_signal_data_callback_neuro_eeg(ptr, data, sz_data, user_data):
            signal_data = [SignalChannelsData(PackNum=int(data[i].PackNum),
                                              Marker=int(data[i].Marker),
                                              Samples=[float(data[i].Samples[j]) for j in range(data[i].SzSamples)]) for
                           i in range(sz_data)]
            if user_data.signalDataReceived is not None:
                user_data.signalDataReceived(user_data, signal_data)

        status = OpStatus()
        self.__signalDataCallbackNeuroEEG = SignalDataCallbackNeuroEEG(__py_signal_data_callback_neuro_eeg)
        self.__signalDataCallbackNeuroEEGHandle = NeuroEEGSignalDataListenerHandle()
        _neuro_lib.addSignalCallbackNeuroEEG(self.sensor_ptr, self.__signalDataCallbackNeuroEEG,
                                              byref(self.__signalDataCallbackNeuroEEGHandle),
                                              ctypes.py_object(self), byref(status))
        raise_exception_if(status)

    def __add_resist_callback_neuro_eeg(self):
        def __py_resist_callback_neuro_eeg(ptr, data, sz_data, user_data):
            resist = [ResistChannelsData(PackNum=int(data[i].PackNum),
                                         A1=float(data[i].A1),
                                         A2=float(data[i].A2),
                                         Bias=float(data[i].Bias),
                                         Values=[float(data[i].Values[j]) for j in range(data[i].SzValues)])
                      for i in range(sz_data)]
            if user_data.resistDataReceived is not None:
                user_data.resistDataReceived(user_data, resist)

        status = OpStatus()
        self.__resistCallbackNeuroEEG = ResistDataCallbackNeuroEEG(__py_resist_callback_neuro_eeg)
        self.__resistCallbackNeuroEEGHandle = NeuroEEGResistDataListenerHandle()
        _neuro_lib.addResistCallbackNeuroEEG(self.sensor_ptr, self.__resistCallbackNeuroEEG,
                                              byref(self.__resistCallbackNeuroEEGHandle),
                                              ctypes.py_object(self), byref(status))
        raise_exception_if(status)

    def __add_signal_resist_callback_neuro_eeg(self):
        def __py_signal_resist_callback_neuro_eeg(ptr, signalData, sz_signalData, resistData, sz_resistData, user_data):
            s_res = [SignalChannelsData(PackNum=int(signalData[i].PackNum),
                                              Marker=int(signalData[i].Marker),
                                              Samples=[float(signalData[i].Samples[j]) for j in range(signalData[i].SzSamples)]) for
                           i in range(sz_signalData)]
            r_res = [ResistChannelsData(PackNum=int(resistData[i].PackNum),
                                         A1=float(resistData[i].A1),
                                         A2=float(resistData[i].A2),
                                         Bias=float(resistData[i].Bias),
                                         Values=[float(resistData[i].Values[j]) for j in range(resistData[i].SzValues)])
                      for i in range(sz_resistData)]
            if user_data.signalResistDataReceived is not None:
                user_data.signalResistDataReceived(user_data, s_res, r_res)

        status = OpStatus()
        self.__signalResistCallbackNeuroEEG = SignalResistDataCallbackNeuroEEG(__py_signal_resist_callback_neuro_eeg)
        self.__signalResistCallbackNeuroEEGHandle = NeuroEEGSignalResistDataListenerHandle()
        _neuro_lib.addSignalResistCallbackNeuroEEG(self.sensor_ptr, self.__signalResistCallbackNeuroEEG,
                                                   byref(self.__signalResistCallbackNeuroEEGHandle),
                                                   ctypes.py_object(self), byref(status))
        raise_exception_if(status)

    @property
    def photo_stim_module(self) -> PhotoStimSensor:
        return self._photo_stim_sensor

    @photo_stim_module.setter
    def photo_stim_module(self, ps_sensor: PhotoStimSensor):
        status = OpStatus()
        _neuro_lib.writePhotoStimNeuroEEG(self.sensor_ptr, ps_sensor.sensor_ptr, byref(status))
        raise_exception_if(status)
        self._photo_stim_sensor = ps_sensor

    @property
    def survey_id(self) -> int:
        status = OpStatus()
        si_type = POINTER(c_uint32)
        si_out = si_type(c_uint32(1))
        _neuro_lib.readSurveyIdNeuroEEG(self.sensor_ptr, si_out, byref(status))
        raise_exception_if(status)
        return int(si_out.contents.value)

    @survey_id.setter
    def survey_id(self, id: int):
        status = OpStatus()
        _neuro_lib.writeSurveyIdNeuroEEG(self.sensor_ptr, id, byref(status))
        raise_exception_if(status)

    @property
    def supported_channels(self) -> list[EEGChannelInfo]:
        status = OpStatus()
        ch_count = _neuro_lib.getChannelsCountSensor(self.sensor_ptr)
        channel_info_out = (NativeEEGChannelInfo * ch_count)(*[NativeEEGChannelInfo() for _ in range(ch_count)])
        sz_channel_info_in_out = SizeType(ctypes.c_int32(ch_count))
        _neuro_lib.readSupportedChannelsNeuroEEG(self.sensor_ptr, channel_info_out, sz_channel_info_in_out,
                                                  byref(status))
        raise_exception_if(status)
        channel_info = []
        for i in range(sz_channel_info_in_out.contents.value):
            channel_info.append(
                EEGChannelInfo(Id=EEGChannelId(channel_info_out[i].Id),
                               ChType=EEGChannelType(channel_info_out[i].ChType),
                               Name=''.join([chr(c) for c in channel_info_out[i].Name]).rstrip('\x00'),
                               Num=int(channel_info_out[i].Num)))
        return channel_info

    @property
    def amplifier_param(self) -> NeuroEEGAmplifierParam:
        status = OpStatus()
        cmap = POINTER(NativeNeuroEEGAmplifierParam)
        amp_param_out = cmap(NativeNeuroEEGAmplifierParam())
        _neuro_lib.readAmplifierParamNeuroEEG(self.sensor_ptr, amp_param_out, byref(status))
        raise_exception_if(status)
        ch_count = _neuro_lib.getChannelsCountSensor(self.sensor_ptr)
        return (NeuroEEGAmplifierParam(
            ReferentResistMesureAllow=bool(amp_param_out.contents.ReferentResistMesureAllow),
            Frequency=SensorSamplingFrequency(amp_param_out.contents.Frequency),
            ReferentMode=EEGRefMode(amp_param_out.contents.ReferentMode),
            ChannelMode=[EEGChannelMode(amp_param_out.contents.ChannelMode[i]) for i in range(ch_count)],
            ChannelGain=[SensorGain(amp_param_out.contents.ChannelGain[i]) for i in range(ch_count)],
            RespirationOn=bool(amp_param_out.contents.RespirationOn)
        ))

    @amplifier_param.setter
    def amplifier_param(self, params: NeuroEEGAmplifierParam):
        status = OpStatus()
        ch_count = _neuro_lib.getChannelsCountSensor(self.sensor_ptr)
        amplifier_param = NativeNeuroEEGAmplifierParam()
        amplifier_param.ReferentResistMesureAllow=params.ReferentResistMesureAllow # ???????
        amplifier_param.Frequency=params.Frequency.value
        amplifier_param.ReferentMode=params.ReferentMode.value
        amplifier_param.ChannelMode=(ctypes.c_uint8 * NEURO_EEG_MAX_CH_COUNT)(
            *[params.ChannelMode[i].value for i in range(ch_count)])
        amplifier_param.ChannelGain=(ctypes.c_uint8 * NEURO_EEG_MAX_CH_COUNT)(
            *[params.ChannelGain[i].value for i in range(ch_count)])
        amplifier_param.RespirationOn=params.RespirationOn
        _neuro_lib.writeAmplifierParamNeuroEEG(self.sensor_ptr, amplifier_param, byref(status))
        raise_exception_if(status)

    @property
    def stim_mode(self) -> SensorStimulMode:
        status = OpStatus()
        mode_val = EnumType(ctypes.c_int8(1))
        _neuro_lib.readStimMode(self.sensor_ptr, mode_val, byref(status))
        raise_exception_if(status)
        return SensorStimulMode(mode_val.contents.value)

    @property
    def photo_stim_sync_state(self) -> SensorStimulSyncState:
        status = OpStatus()
        state_val = EnumType(ctypes.c_int8(1))
        _neuro_lib.readPhotoStimSyncState(self.sensor_ptr, state_val, byref(status))
        raise_exception_if(status)
        return SensorStimulSyncState(state_val.contents.value)

    @property
    def stim_programs(self) -> list[StimulPhase]:
        status = OpStatus()
        max_phases_count = _neuro_lib.getMaxStimulPhasesCountSensor(self.sensor_ptr)
        phases_out = POINTER(NativeStimulPhase)(NativeStimulPhase())
        sz_phases_in_out = SizeType(ctypes.c_int32(max_phases_count))
        _neuro_lib.readStimPrograms(self.sensor_ptr, phases_out, sz_phases_in_out, byref(status))
        raise_exception_if(status)
        return [StimulPhase(Frequency=float(phases_out[i].Frequency),
                            Power=float(phases_out[i].Power),
                            Pulse=float(phases_out[i].Pulse),
                            StimulDuration=float(phases_out[i].StimulDuration),
                            Pause=float(phases_out[i].Pause),
                            FillingFrequency=float(phases_out[i].FillingFrequency)) for i in range(sz_phases_in_out)]

    @stim_programs.setter
    def stim_programs(self, programs: list[StimulPhase]):
        status = OpStatus()
        phases_len = len(programs)
        phases_values=(NativeStimulPhase * phases_len(*[NativeStimulPhase(
            Frequency=c_double(programs[i].Frequency),
            Power=c_double(programs[i].Power),
            Pulse=c_double(programs[i].Pulse),
            StimulDuration=c_double(programs[i].StimulDuration),
            Pause=c_double(programs[i].Pause),
            FillingFrequency=c_double(programs[i].FillingFrequency)
        ) for i in range(phases_len)]))
        _neuro_lib.writeStimPrograms(self.sensor_ptr, phases_values, phases_len, byref(status))
        raise_exception_if(status)

    @property
    def photo_stim_time_defer(self) -> float:
        status = OpStatus()
        time = POINTER(c_double)(c_double(0))
        _neuro_lib.readPhotoStimTimeDefer(self.sensor_ptr, time, byref(status))
        raise_exception_if(status)
        return float(time.contents.value)

    @photo_stim_time_defer.setter
    def photo_stim_time_defer(self, time: float):
        status = OpStatus()
        _neuro_lib.writePhotoStimTimeDefer(self.sensor_ptr, time, byref(status))
        raise_exception_if(status)
        