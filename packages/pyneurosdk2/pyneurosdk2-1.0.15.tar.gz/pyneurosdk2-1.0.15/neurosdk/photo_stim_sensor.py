import contextlib

from neurosdk.__utils import raise_exception_if
from neurosdk.__cmn_types import *
from neurosdk.cmn_types import *
from neurosdk.sensor import Sensor, _neuro_lib

class PhotoStimSensor(Sensor):
    def __init__(self, ptr):
        super().__init__(ptr)
        # signatures

        _neuro_lib.addPhotoStimSyncStateCallback.argtypes = [SensorPointer, PhotoStimulSyncStateCallbackNeuroEEG, c_void_p, ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addPhotoStimSyncStateCallback.restype = c_uint8
        _neuro_lib.removePhotoStimSyncStateCallback.argtypes = [PhotoStimulSyncStateListenerHandle]
        _neuro_lib.removePhotoStimSyncStateCallback.restype = c_uint8

        _neuro_lib.addStimModeCallback.argtypes = [SensorPointer, StimulModeListenerCallbackNeuroEEG, c_void_p, ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addStimModeCallback.restype = c_uint8
        _neuro_lib.removeStimModeCallback.argtypes = [StimulModeListenerHandle]
        _neuro_lib.removeStimModeCallback.restype = c_void_p
        self.photoStimSyncStateChanged = None
        self.sensorStimModeChanged = None
        self.__add_stim_sync_state_callback()
        self.__add_stim_mode_callback()
        self.__closed = False


    def __del__(self):
        with contextlib.suppress(Exception):
            if not self.__closed:
                self.__closed = True
                self.photoStimSyncStateChanged = None
                _neuro_lib.removePhotoStimSyncStateCallback(self.__stim_sync_state_callback_handle)
                self.sensorStimModeChanged = None
                _neuro_lib.removeStimModeCallback(self.__stim_mode_callback_handle)
        super().__del__()

    def __add_stim_sync_state_callback(self):
        def __py_stim_sync_state_callback(ptr, state, user_data):
            if user_data.photoStimSyncStateChanged is not None:
                user_data.photoStimSyncStateChanged(user_data, SensorStimulSyncState(state))

        status = OpStatus()
        self.__stim_sync_state_callback = PhotoStimulSyncStateCallbackNeuroEEG(__py_stim_sync_state_callback)
        self.__stim_sync_state_callback_handle = PhotoStimulSyncStateListenerHandle()
        _neuro_lib.addPhotoStimSyncStateCallback(self.sensor_ptr, self.__stim_sync_state_callback,
                                                 byref(self.__stim_sync_state_callback_handle),
                                                 py_object(self), byref(status))
        raise_exception_if(status)

    def __add_stim_mode_callback(self):
        def __py_stim_mode_callback(ptr, mode, user_data):
            if user_data.sensorStimModeChanged is not None:
                user_data.sensorStimModeChanged(user_data, SensorStimulMode(mode))

        status = OpStatus()
        self.__stim_mode_callback = StimulModeListenerCallbackNeuroEEG(__py_stim_mode_callback)
        self.__stim_mode_callback_handle = StimulModeListenerHandle()
        _neuro_lib.addStimModeCallback(self.sensor_ptr, self.__stim_mode_callback,
                                                 byref(self.__stim_mode_callback_handle),
                                                 py_object(self), byref(status))
        raise_exception_if(status)
