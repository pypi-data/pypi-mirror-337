from enum import Enum
from dataclasses import dataclass


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if type(self).__qualname__ != type(other).__qualname__:
            return NotImplemented
        return self.name == other.name and self.value == other.value

    def __hash__(self):
        return hash((type(self).__qualname__, self.name))


class SensorFamily(OrderedEnum):
    SensorUnknown = 0
    LECallibri = 1
    LEKolibri = 2
    LEBrainBit = 3
    LEBrainBitBlack = 4
    LEHeadPhones2 = 6
    LEHeadband = 11
    LEBrainBit2 = 18
    LEBrainBitPro = 19
    LEBrainBitFlex = 20
    LENeuroEEG = 14


@dataclass
class SensorInfo:
    SensFamily: SensorFamily
    SensModel: int
    Name: str
    Address: str
    SerialNumber: str
    PairingRequired: bool
    RSSI: int


class SensorFeature(OrderedEnum):
    Signal = 0
    MEMS = 1
    CurrentStimulator = 2
    Respiration = 3
    Resist = 4
    FPG = 5
    Envelope = 6
    PhotoStimulator = 7
    AcousticStimulator = 8
    FlashCard = 9
    LedChannels = 10
    SignalWithResist = 11


class SensorFirmwareMode(OrderedEnum):
    Bootloader = 0
    Application = 1


class SensorCommand(OrderedEnum):
    StartSignal = 0
    StopSignal = 1
    StartResist = 2
    StopResist = 3
    StartMEMS = 4
    StopMEMS = 5
    StartRespiration = 6
    StopRespiration = 7
    StartCurrentStimulation = 8
    StopCurrentStimulation = 9
    EnableMotionAssistant = 10
    DisableMotionAssistant = 11
    FindMe = 12
    StartAngle = 13
    StopAngle = 14
    CalibrateMEMS = 15
    ResetQuaternion = 16
    StartEnvelope = 17
    StopEnvelope = 18
    ResetMotionCounter = 19
    CalibrateStimulation = 20
    Idle = 21
    PowerDown = 22
    StartFPG = 23
    StopFPG = 24
    StartSignalAndResist = 25
    StopSignalAndResist = 26
    StartPhotoStimulation = 27
    StopPhotoStimulation = 28
    StartAcousticStimulation = 29
    StopAcousticStimulation = 30
    FileSystemEnable = 31
    FileSystemDisable = 32
    FileSystemStreamClose = 33
    StartCalibrateSignal = 34
    StopCalibrateSignal = 35
    CommandPhotoStimEnable = 36
    CommandPhotoStimDisable = 37


class SensorParameter(OrderedEnum):
    Name = 0
    State = 1
    Address = 2
    SerialNumber = 3
    HardwareFilterState = 4
    FirmwareMode = 5
    SamplingFrequency = 6
    Gain = 7
    Offset = 8
    ExternalSwitchState = 9
    ADCInputState = 10
    AccelerometerSens = 11
    GyroscopeSens = 12
    StimulatorAndMAState = 13
    StimulatorParamPack = 14
    MotionAssistantParamPack = 15
    FirmwareVersion = 16
    MEMSCalibrationStatus = 17
    MotionCounterParamPack = 18
    MotionCounter = 19
    BattPower = 20
    SensorFamily = 21
    SensorMode = 22
    IrAmplitude = 23
    RedAmplitude = 24
    EnvelopeAvgWndSz = 25
    EnvelopeDecimation = 26
    SamplingFrequencyResist = 27
    SamplingFrequencyMEMSv = 28
    SamplingFrequencyFPG = 29
    Amplifier = 30
    SensorChannels = 31
    SamplingFrequencyResp = 32
    SurveyId = 33
    FileSystemStatus = 34
    FileSystemDiskInfo = 35
    ReferentsShort = 36
    ReferentsGround = 37
    SamplingFrequencyEnvelope = 38
    ChannelConfiguration = 39
    ElectrodeState = 40
    ChannelResistConfiguration = 41
    BattVoltage = 42
    PhotoStimTimeDefer = 43
    PhotoStimSyncState = 44
    SensorPhotoStim = 45
    StimMode = 46
    LedChannels = 47
    LedState = 48


class SensorParamAccess(OrderedEnum):
    Read = 0
    ReadWrite = 1
    ReadNotify = 2


class SensorState(OrderedEnum):
    StateInRange = 0
    StateOutOfRange = 1


class SensorSamplingFrequency(OrderedEnum):
    FrequencyHz10 = 0
    FrequencyHz20 = 1
    FrequencyHz100 = 2
    FrequencyHz125 = 3
    FrequencyHz250 = 4
    FrequencyHz500 = 5
    FrequencyHz1000 = 6
    FrequencyHz2000 = 7
    FrequencyHz4000 = 8
    FrequencyHz8000 = 9
    FrequencyHz10000 = 10
    FrequencyHz12000 = 11
    FrequencyHz16000 = 12
    FrequencyHz24000 = 13
    FrequencyHz32000 = 14
    FrequencyHz48000 = 15
    FrequencyHz64000 = 16
    FrequencyUnsupported = 0xFF


class SensorGain(OrderedEnum):
    Gain1 = 0
    Gain2 = 1
    Gain3 = 2
    Gain4 = 3
    Gain6 = 4
    Gain8 = 5
    Gain12 = 6
    Gain24 = 7
    Gain5 = 8
    Gain2x = 9
    Gain4x = 10
    GainUnsupported = 11


class SensorDataOffset(OrderedEnum):
    DataOffset0 = 0x00
    DataOffset1 = 0x01
    DataOffset2 = 0x02
    DataOffset3 = 0x03
    DataOffset4 = 0x04
    DataOffset5 = 0x05
    DataOffset6 = 0x06
    DataOffset7 = 0x07
    DataOffset8 = 0x08
    DataOffsetUnsupported = 0xFF


@dataclass
class ParameterInfo:
    Param: SensorParameter
    ParamAccess: SensorParamAccess


@dataclass
class SensorVersion:
    FwMajor: int
    FwMinor: int
    FwPatch: int
    HwMajor: int
    HwMinor: int
    HwPatch: int
    ExtMajor: int


class GenCurrent(OrderedEnum):
    GenCurr0uA = 0
    GenCurr6nA = 1
    GenCurr24nA = 2
    GenCurr6uA = 3
    GenCurr24uA = 4
    GenUnsupported = 0xFF

    
@dataclass
class Point3D:
    X: float = 0
    Y: float = 0
    Z: float = 0


@dataclass
class MEMSData:
    PackNum: int
    Accelerometer: Point3D
    Gyroscope: Point3D


class SensorAccelerometerSensitivity(OrderedEnum):
    AccSens2g = 0
    AccSens4g = 1
    AccSens8g = 2
    AccSens16g = 3
    AccSensUnsupported = 4


class SensorGyroscopeSensitivity(OrderedEnum):
    GyroSens250Grad = 0
    GyroSens500Grad = 1
    GyroSens1000Grad = 2
    GyroSens2000Grad = 3
    GyroSensUnsupported = 4

    
@dataclass
class CallibriSignalData:
    PackNum: int
    Samples: list[float]


@dataclass
class CallibriRespirationData:
    PackNum: int
    Samples: list[float]


@dataclass
class CallibriEnvelopeData:
    PackNum: int
    Sample: float

    
class CallibriStimulatorState(OrderedEnum):
    NoParams = 0
    Disabled = 1
    Enabled = 2
    Unsupported = 0xFF


class CallibriMotionAssistantLimb(OrderedEnum):
    RightLeg = 0
    LeftLeg = 1
    RightArm = 2
    LeftArm = 3
    Unsupported = 0xFF


class SensorFilter(OrderedEnum):
    HPFBwhLvl1CutoffFreq1Hz = 0
    HPFBwhLvl1CutoffFreq5Hz = 1
    BSFBwhLvl2CutoffFreq45_55Hz = 2
    BSFBwhLvl2CutoffFreq55_65Hz = 3
    HPFBwhLvl2CutoffFreq10Hz = 4
    LPFBwhLvl2CutoffFreq400Hz = 5
    HPFBwhLvl2CutoffFreq80Hz = 6
    Unknown = 0xFF


class SensorExternalSwitchInput(OrderedEnum):
    ElectrodesRespUSB = 0
    Electrodes = 1
    USB = 2
    RespUSB = 3
    Short = 4
    Unknown = 0xFF


class SensorADCInput(OrderedEnum):
    Electrodes = 0
    Short = 1
    Test = 2
    Resistance = 3


@dataclass
class CallibriStimulatorMAState:
    StimulatorState: CallibriStimulatorState
    MAState: CallibriStimulatorState


@dataclass
class CallibriStimulationParams:
    Current: int
    PulseWidth: int
    Frequency: int
    StimulusDuration: int


@dataclass
class CallibriMotionAssistantParams:
    GyroStart: int
    GyroStop: int
    Limb: CallibriMotionAssistantLimb
    MinPauseMs: int


@dataclass
class CallibriMotionCounterParam:
    InsenseThresholdMG: int
    InsenseThresholdSample: int


class CallibriColorType(OrderedEnum):
    Red = 0
    Yellow = 1
    Blue = 2
    White = 3
    Unknown = 4


class CallibriSignalType(OrderedEnum):
    EEG = 0
    EMG = 1
    ECG = 2
    EDA = 3
    StrainGaugeBreathing = 4
    ImpedanceBreathing = 5
    TenzoBreathing = 6
    Unknown = 7


class CallibriElectrodeState(OrderedEnum):
    Normal = 0
    HighResistance = 1
    Detached = 2


@dataclass
class QuaternionData:
    PackNum: int
    W: float = 0
    X: float = 0
    Y: float = 0
    Z: float = 0


@dataclass
class FPGData:
    PackNum: int
    IrAmplitude: float
    RedAmplitude: float


class IrAmplitude(OrderedEnum):
    IrAmp0 = 0
    IrAmp14 = 1
    IrAmp28 = 2
    IrAmp42 = 3
    IrAmp56 = 4
    IrAmp70 = 5
    IrAmp84 = 6
    IrAmp100 = 7
    IrAmpUnsupported = 0xFF


class RedAmplitude(OrderedEnum):
    RedAmp0 = 0
    RedAmp14 = 1
    RedAmp28 = 2
    RedAmp42 = 3
    RedAmp56 = 4
    RedAmp70 = 5
    RedAmp84 = 6
    RedAmp100 = 7
    RedAmpUnsupported = 0xFF

    
@dataclass
class BrainBitSignalData:
    PackNum: int
    Marker: int
    O1: float
    O2: float
    T3: float
    T4: float


@dataclass
class BrainBitResistData:
    O1: float
    O2: float
    T3: float
    T4: float

    
@dataclass
class HeadbandSignalData:
    PackNum: int
    Marker: int
    O1: float
    O2: float
    T3: float
    T4: float


@dataclass
class HeadbandResistData:
    PackNum: int
    O1: float
    O2: float
    T3: float
    T4: float

    
@dataclass
class Headphones2SignalData:
    PackNum: int
    Marker: int
    Ch1: float
    Ch2: float
    Ch3: float
    Ch4: float


@dataclass
class Headphones2ResistData:
    PackNum: int
    Ch1: float
    Ch2: float
    Ch3: float
    Ch4: float


@dataclass
class Headphones2AmplifierParam:
    ChSignalUse1: bool
    ChSignalUse2: bool
    ChSignalUse3: bool
    ChSignalUse4: bool

    ChResistUse1: bool
    ChResistUse2: bool
    ChResistUse3: bool
    ChResistUse4: bool

    ChGain1: SensorGain
    ChGain2: SensorGain
    ChGain3: SensorGain
    ChGain4: SensorGain

    Current: GenCurrent

    
class SensorAmpMode(OrderedEnum):
    Invalid = 0
    PowerDown = 1
    Idle = 2
    Signal = 3
    Resist = 4
    SignalResist = 5
    Envelope = 6
@dataclass
class ResistRefChannelsData:
    PackNum: int
    Samples: list[float]
    Referents: list[float]


class BrainBit2ChannelMode(OrderedEnum):
    ChModeShort = 0,
    ChModeNormal = 1


@dataclass
class BrainBit2AmplifierParam:
    ChSignalMode: list[BrainBit2ChannelMode]
    ChResistUse: list[bool]
    ChGain: list[SensorGain]
    Current: GenCurrent

    
@dataclass
class SignalChannelsData:
    PackNum: int
    Marker: int
    Samples: list[float]


class EEGChannelId(OrderedEnum):
    EEGChIdUnknown = 0
    EEGChIdO1 = 1
    EEGChIdP3 = 2
    EEGChIdC3 = 3
    EEGChIdF3 = 4
    EEGChIdFp1 = 5
    EEGChIdT5 = 6
    EEGChIdT3 = 7
    EEGChIdF7 = 8

    EEGChIdF8 = 9
    EEGChIdT4 = 10
    EEGChIdT6 = 11
    EEGChIdFp2 = 12
    EEGChIdF4 = 13
    EEGChIdC4 = 14
    EEGChIdP4 = 15
    EEGChIdO2 = 16

    EEGChIdD1 = 17
    EEGChIdD2 = 18
    EEGChIdOZ = 19
    EEGChIdPZ = 20
    EEGChIdCZ = 21
    EEGChIdFZ = 22
    EEGChIdFpZ = 23
    EEGChIdD3 = 24


class EEGChannelType(OrderedEnum):
    EEGChTypeSingleA1 = 0
    EEGChTypeSingleA2 = 1
    EEGChTypeDifferential = 2
    EEGChTypeRef = 3


class EEGChannelMode(OrderedEnum):
	EEGChModeOff = 0
	EEGChModeShorted = 1
	EEGChModeSignalResist = 2
	EEGChModeSignal = 3
	EEGChModeTest = 4


@dataclass
class EEGChannelInfo:
    Id: EEGChannelId
    ChType: EEGChannelType
    Name: str
    Num: int


class SensorFSStatus(OrderedEnum):
    FSStatusOK = 0
    FSStatusNoInit = 1
    FSStatusNoDisk = 2
    FSStatusProtect = 3


class SensorFSIOStatus(OrderedEnum):
    FSIOStatusNoError = 0
    FSIOStatusIOError = 1
    FSIOStatusTimeout = 2


class SensorFSStreamStatus(OrderedEnum):
    FSStreamStatusClosed = 0
    FSStreamStatusWrite = 1
    FSStreamStatusRead = 2


@dataclass
class NeuroEEGFSStatus:
    FileName: str
    FileSize: int
    ModifiedYear: int
    ModifiedMonth: int
    ModifiedDayOfMonth: int
    ModifiedHour: int
    ModifiedMin: int
    ModifiedSec: int
    Attribute: int


@dataclass
class SensorFileData:
    OffsetStart: int
    DataAmount: int
    Data: list[int] # bytearray


class EEGRefMode(OrderedEnum):
    RefHeadTop = 1
    RefA1A2 = 2

@dataclass
class NeuroEEGAmplifierParam:
    ReferentResistMesureAllow: int
    Frequency: SensorSamplingFrequency
    ReferentMode: EEGRefMode
    ChannelMode: list[EEGChannelMode]
    ChannelGain: list[SensorGain]
    RespirationOn: bool


@dataclass
class ResistChannelsData:
    PackNum: int
    A1: float
    A2: float
    Bias: float
    Values: list[float]


class SensorStimulMode(OrderedEnum):
    StimulModeInvalid = 0
    StimulModeStopped = 1
    StimulModePendingSync = 2
    StimulModeSynchronized = 3
    StimulModeStimProgrammRuning = 4
    StimulModeError = 5


@dataclass
class StimulPhase:
    Frequency: float		# Stimulation frequency
    Power: float			# Stimulus power 0...100 %
    Pulse: float			# Duration of a single stimulation pulse
    StimulDuration: float	# Stimulation phase duration
    Pause: float			# Duration of pause after the stimulation phase
    FillingFrequency: float # Filling frequency of the signal for acoustic stimulation


class SensorStimulSyncState(OrderedEnum):
    StimulSyncNormal = 0
    StimulSyncTimeOut = 1


