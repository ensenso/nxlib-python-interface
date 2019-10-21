import json
from nxlib import NxLibCommand, NxLibException, NxLibError
from .helper import convert_camel_to_upper_snake, fix_nxlib_prefix

NXLIB_ITEM_SEPARATOR = '/'
NXLIB_INDEX_ESCAPE_CHAR = '\\'
NXLIB_ITEM_FORBIDDEN_CHARS = "\r\n\"/\\\0"


NXLIB_BAD_REQUEST = 11
NXLIB_BUFFER_NOT_DIVISIBLE_BY_ELEMENT_SIZE = 16
NXLIB_BUFFER_TOO_SMALL = 15
NXLIB_CANNOT_CREATE_ITEM = 1
NXLIB_COMMAND_RUNNING = 19
NXLIB_CONNECTION_NOT_COMPATIBLE = 22
NXLIB_COULD_NOT_INTERPRET_JSON_TEXT = 2
NXLIB_COULD_NOT_LOAD_FUNCTION = 21
NXLIB_COULD_NOT_LOAD_LIBRARY = 20
NXLIB_COULD_NOT_OPEN_PORT = 6
NXLIB_DEBUG_MESSAGE_OVERFLOW = 18
NXLIB_EXECUTION_FAILED = 17
NXLIB_INITIALIZATION_NOT_ALLOWED = 23
NXLIB_INTERNAL_ERROR = 7
NXLIB_INVALID_BUFFER_SIZE = 14
NXLIB_ITEM_INEXISTENT = 3
NXLIB_ITEM_TYPE_NOT_COMPATIBLE = 13
NXLIB_METHOD_INVALID = 10
NXLIB_NESTING_LIMIT_REACHED = 24
NXLIB_NO_DEBUG_DATA = 5
NXLIB_NO_OPEN_PROFILE_BLOCK = 25
NXLIB_NOT_CONNECTED = 9
NXLIB_OPERATION_SUCCEEDED = 0
NXLIB_TIMEOUT = 8
CMD_ADAPTER_CONFIGURATION = "AdapterConfiguration"
CMD_ADD_PATTERN_BUFFER_VIEW = "AddPatternBufferView"
CMD_ADJUST_EXPOSURE_AND_GAIN = "AdjustExposureAndGain"
CMD_BREAK = "Break"
CMD_CALIBRATE = "Calibrate"
CMD_CALIBRATE_HAND_EYE = "CalibrateHandEye"
CMD_CALIBRATE_IN_BACKGROUND = "CalibrateInBackground"
CMD_CALIBRATE_PATTERN = "CalibratePattern"
CMD_CALIBRATE_UPDATE_PATTERNS = "CalibrateUpdatePatterns"
CMD_CALIBRATE_WORKSPACE = "CalibrateWorkspace"
CMD_CAPTURE = "Capture"
CMD_CHAIN_TRANSFORMATIONS = "ChainTransformations"
CMD_CLEAR_IMAGE_BUFFER = "ClearImageBuffer"
CMD_CLEAR_IMAGES = "ClearImages"
CMD_CLEAR_OVERLAY = "ClearOverlay"
CMD_CLOSE = "Close"
CMD_COLLECT_PATTERN = "CollectPattern"
CMD_COLLECT_PLANE_POINTS = "CollectPlanePoints"
CMD_COMPUTE_DISPARITY_MAP = "ComputeDisparityMap"
CMD_COMPUTE_IMAGE_CONTRAST = "ComputeImageContrast"
CMD_COMPUTE_NORMALS = "ComputeNormals"
CMD_COMPUTE_POINT_MAP = "ComputePointMap"
CMD_CONVERT_TRANSFORMATION = "ConvertTransformation"
CMD_CREATE_CAMERA = "CreateCamera"
CMD_DELETE_CAMERA = "DeleteCamera"
CMD_DISCARD_PATTERNS = "DiscardPatterns"
CMD_ESTIMATE_DISPARITY_SETTINGS = "EstimateDisparitySettings"
CMD_ESTIMATE_PATTERN_POSE = "EstimatePatternPose"
CMD_ETHERNET_CONFIGURATION = "EthernetConfiguration"
CMD_FILTER_PATTERN_BUFFER = "FilterPatternBuffer"
CMD_FIT_PRIMITIVE = "FitPrimitive"
CMD_FLASH = "Flash"
CMD_GENERATE_CALIBRATION_PATTERN = "GenerateCalibrationPattern"
CMD_GET_CONSTANTS = "GetConstants"
CMD_GET_MODEL_INFO = "GetModelInfo"
CMD_GET_PATTERN_BUFFER = "GetPatternBuffer"
CMD_GET_PATTERN_BUFFERS = "GetPatternBuffers"
CMD_GET_RAW_CALIBRATION_DATA = "GetRawCalibrationData"
CMD_INTERNAL_PWM = "InternalPwm"
CMD_LOAD_CALIBRATION = "LoadCalibration"
CMD_LOAD_IMAGE = "LoadImage"
CMD_LOAD_TEXT = "LoadText"
CMD_LOAD_U_EYE_PARAMETER_SET = "LoadUEyeParameterSet"
CMD_MEASURE_CALIBRATION = "MeasureCalibration"
CMD_NETWORK_CONTROL = "NetworkControl"
CMD_OPEN = "Open"
CMD_PATTERN_BUFFER_INFO = "PatternBufferInfo"
CMD_PROJECT_PATTERN = "ProjectPattern"
CMD_RECALIBRATE = "Recalibrate"
CMD_RECTIFY_IMAGES = "RectifyImages"
CMD_REDUCE_PATTERN_BUFFER = "ReducePatternBuffer"
CMD_REDUCE_PATTERNS = "ReducePatterns"
CMD_REMOVE_PATTERN_BUFFER_VIEW = "RemovePatternBufferView"
CMD_RENDER_DEPTH_MAP = "RenderDepthMap"
CMD_RENDER_POINT_MAP = "RenderPointMap"
CMD_RENDER_VIEW = "RenderView"
CMD_RETRIEVE = "Retrieve"
CMD_SAVE_IMAGE = "SaveImage"
CMD_SAVE_MODEL = "SaveModel"
CMD_SAVE_TEXT = "SaveText"
CMD_SET_PATTERN_BUFFER = "SetPatternBuffer"
CMD_SET_PATTERN_BUFFERS = "SetPatternBuffers"
CMD_SET_STATUS_LEDS = "SetStatusLeds"
CMD_SIMULATE_PHYSICS = "SimulatePhysics"
CMD_STORE_CALIBRATION = "StoreCalibration"
CMD_SYNCHRONIZE = "Synchronize"
CMD_TRIGGER = "Trigger"
CMD_UPDATE_FIRMWARE = "UpdateFirmware"
CMD_VISUALIZE_PATTERN_BUFFER = "VisualizePatternBuffer"
ERR_CALIBRATION_FAILED = "CalibrationFailed"
ERR_CAMERA_NOT_FOUND = "CameraNotFound"
ERR_CHANGED_MODEL = "ChangedModel"
ERR_COMMAND_NOT_ALLOWED = "CommandNotAllowed"
ERR_COMMAND_UNKNOWN = "CommandUnknown"
ERR_EMPTY_IMAGE = "EmptyImage"
ERR_INVALID_CALIBRATION_DATA = "InvalidCalibrationData"
ERR_INVALID_PAIRING_DATA = "InvalidPairingData"
ERR_INVALID_PATTERN_BUFFER = "InvalidPatternBuffer"
ERR_NO_WORKSPACE_LINK = "NoWorkspaceLink"
ERR_NOT_ENOUGH_POINTS_FOR_PRIMITIVE = "NotEnoughPointsForPrimitive"
ERR_OPERATION_CANCELED = "OperationCanceled"
ERR_PATTERN_BUFFER_LOCKED = "PatternBufferLocked"
ERR_PATTERN_DATA_INCOMPATIBLE = "PatternDataIncompatible"
ERR_PATTERN_NOT_DECODABLE = "PatternNotDecodable"
ERR_PATTERN_NOT_FOUND = "PatternNotFound"
ERR_SENSOR_NOT_COMPATIBLE = "SensorNotCompatible"
ERR_UNHANDLED_EXCEPTION = "UnhandledException"
ERR_WIRING_TEST_FAILED = "WiringTestFailed"
NXLIB_ITEM_TYPE_ARRAY = 5
NXLIB_ITEM_TYPE_BOOL = 4
NXLIB_ITEM_TYPE_INVALID = 0
NXLIB_ITEM_TYPE_NULL = 1
NXLIB_ITEM_TYPE_NUMBER = 2
NXLIB_ITEM_TYPE_OBJECT = 6
NXLIB_ITEM_TYPE_STRING = 3
ITM_ABSOLUTE_BLACK_LEVEL_OFFSET = "AbsoluteBlackLevelOffset"
ITM_ACTIVE = "Active"
ITM_ADAPTERS = "Adapters"
ITM_ADJUST_EXPOSURE = "AdjustExposure"
ITM_ADJUST_GAIN = "AdjustGain"
ITM_ALIGN_AXIS = "AlignAxis"
ITM_ALL = "All"
ITM_ALLOW_FIRMWARE_UPLOAD = "AllowFirmwareUpload"
ITM_AMBIENT = "Ambient"
ITM_AND = "And"
ITM_ANGLE = "Angle"
ITM_ANGLES = "Angles"
ITM_APERTURE = "Aperture"
ITM_API_ERRORS = "ApiErrors"
ITM_APPLICATION = "Application"
ITM_APPLY = "Apply"
ITM_ARCHITECTURE = "Architecture"
ITM_AREA_OF_INTEREST = "AreaOfInterest"
ITM_ASSEMBLY_CALIBRATION = "AssemblyCalibration"
ITM_ASSEMBLY_PATTERN = "AssemblyPattern"
ITM_ASYNCHRONOUSLY_TRIGGERED = "AsynchronouslyTriggered"
ITM_AUTO_BLACK_LEVEL = "AutoBlackLevel"
ITM_AUTO_EXPOSURE = "AutoExposure"
ITM_AUTO_FOCUS = "AutoFocus"
ITM_AUTO_GAIN = "AutoGain"
ITM_AUTO_SWAP = "AutoSwap"
ITM_AUTOMATIC = "Automatic"
ITM_AVAILABLE = "Available"
ITM_AVERAGE = "Average"
ITM_AVERAGE_POSE_ERROR = "AveragePoseError"
ITM_AXIS = "Axis"
ITM_BACKGROUND = "Background"
ITM_BANDWIDTH = "Bandwidth"
ITM_BANDWIDTH_LIMIT = "BandwidthLimit"
ITM_BASELINE = "Baseline"
ITM_BINARY_INFO = "BinaryInfo"
ITM_BINNING = "Binning"
ITM_BINNING_SHIFT = "BinningShift"
ITM_BLACK_LEVEL_OFFSET = "BlackLevelOffset"
ITM_BLACK_LEVEL_OFFSET_CALIBRATION = "BlackLevelOffsetCalibration"
ITM_BLIND = "Blind"
ITM_BLUR = "Blur"
ITM_BLUR_MIN_MAX = "BlurMinMax"
ITM_BOARD = "Board"
ITM_BOOTLOADER = "Bootloader"
ITM_BORDER_SPREAD = "BorderSpread"
ITM_BOUNDING_BOX = "BoundingBox"
ITM_BRIGHTNESS = "Brightness"
ITM_BUFFER = "Buffer"
ITM_BUFFER_COUNT = "BufferCount"
ITM_BUFFER_SIZE = "BufferSize"
ITM_BUILD = "Build"
ITM_BY_EEPROM_ID = "ByEepromId"
ITM_BY_SERIAL_NO = "BySerialNo"
ITM_CPU = "CPU"
ITM_CRC_ERROR_COUNT = "CRCErrorCount"
ITM_CUDA = "CUDA"
ITM_CAL_TAB_TYPE = "CalTabType"
ITM_CAL_TABS = "CalTabs"
ITM_CALCULATE_IP = "CalculateIp"
ITM_CALIBRATED = "Calibrated"
ITM_CALIBRATION = "Calibration"
ITM_CALIBRATION_FILE = "CalibrationFile"
ITM_CALIBRATION_HISTORY = "CalibrationHistory"
ITM_CAMERA = "Camera"
ITM_CAMERAS = "Cameras"
ITM_CAPTURE = "Capture"
ITM_CAPTURE_EVENTS = "CaptureEvents"
ITM_CENTER = "Center"
ITM_CHECK = "Check"
ITM_CHECK_DAEMON = "CheckDaemon"
ITM_CLEAR_IMAGE_BUFFER_ON_TRIGGER = "ClearImageBufferOnTrigger"
ITM_CLOCK_RATE = "ClockRate"
ITM_CODE_METER = "CodeMeter"
ITM_COLOR = "Color"
ITM_COLOR_OFFSET = "ColorOffset"
ITM_COLOR_REPETITION_DISTANCE = "ColorRepetitionDistance"
ITM_COMMAND = "Command"
ITM_COMMANDS = "Commands"
ITM_COMMON_ITEMS = "CommonItems"
ITM_COMMON_VALUES = "CommonValues"
ITM_COMPONENT_THRESHOLD = "ComponentThreshold"
ITM_COMPUTE_CAPABILITY = "ComputeCapability"
ITM_COMPUTE_DISPARITY_MAP = "ComputeDisparityMap"
ITM_CONFIGURATION = "Configuration"
ITM_CONNECTED = "Connected"
ITM_CONNECTED_CAMERAS = "ConnectedCameras"
ITM_CONNECTED_PATTERNS = "ConnectedPatterns"
ITM_CONTENT = "Content"
ITM_CONTRAST = "Contrast"
ITM_CORES = "Cores"
ITM_COST_SCALE = "CostScale"
ITM_COUNT = "Count"
ITM_DHCP = "DHCP"
ITM_DAY = "Day"
ITM_DEBUG = "Debug"
ITM_DECODE_DATA = "DecodeData"
ITM_DEFAULT = "Default"
ITM_DEFAULT_GATEWAY = "DefaultGateway"
ITM_DEFAULT_PARAMETERS = "DefaultParameters"
ITM_DEFINED_POSE = "DefinedPose"
ITM_DEPTH = "Depth"
ITM_DEPTH_CHANGE_COST = "DepthChangeCost"
ITM_DEPTH_STEP_COST = "DepthStepCost"
ITM_DESTINATION = "Destination"
ITM_DEVICE = "Device"
ITM_DEVICES = "Devices"
ITM_DIFFUSE = "Diffuse"
ITM_DIRECTION = "Direction"
ITM_DISPARITY = "Disparity"
ITM_DISPARITY_ACCURACY = "DisparityAccuracy"
ITM_DISPARITY_MAP = "DisparityMap"
ITM_DISPARITY_MAP_OFFSET = "DisparityMapOffset"
ITM_DISPARITY_STEP = "DisparityStep"
ITM_DISTANCE = "Distance"
ITM_DISTORTION = "Distortion"
ITM_DOWNLOAD_IMAGES = "DownloadImages"
ITM_DOWNSAMPLE = "Downsample"
ITM_DRAW_AXES = "DrawAxes"
ITM_DRAW_ONLY = "DrawOnly"
ITM_DRAW_ORIGIN = "DrawOrigin"
ITM_DRIVER = "Driver"
ITM_DURATION = "Duration"
ITM_DUTY_CYCLE = "DutyCycle"
ITM_DYNAMIC = "Dynamic"
ITM_DYNAMIC_CALIBRATION_LIMIT_REACHED = "DynamicCalibrationLimitReached"
ITM_DYNAMIC_OFFSETS = "DynamicOffsets"
ITM_EEPROM_FORMAT = "EepromFormat"
ITM_EEPROM_ID = "EepromId"
ITM_ENABLE_IP_FILTER = "EnableIpFilter"
ITM_ENABLED = "Enabled"
ITM_ENCODING = "Encoding"
ITM_EPIPOLAR = "Epipolar"
ITM_EPIPOLAR_ERROR = "EpipolarError"
ITM_ERROR_SYMBOL = "ErrorSymbol"
ITM_ERROR_TEXT = "ErrorText"
ITM_ERRORS = "Errors"
ITM_ESTIMATE_GRID_SPACING = "EstimateGridSpacing"
ITM_ETHERNET = "Ethernet"
ITM_ETHERNET_CONFIG_MODE = "EthernetConfigMode"
ITM_EXECUTE = "Execute"
ITM_EXPOSURE = "Exposure"
ITM_EXT = "Ext"
ITM_EXTENDED_TYPE = "ExtendedType"
ITM_FACTORY = "Factory"
ITM_FAILURE_PROBABILITY = "FailureProbability"
ITM_FAR = "Far"
ITM_FILE_OUTPUT = "FileOutput"
ITM_FILE_PREFIX = "FilePrefix"
ITM_FILENAME = "Filename"
ITM_FILL_XY_COORDINATES = "FillXYCoordinates"
ITM_FILLING = "Filling"
ITM_FILTER = "Filter"
ITM_FILTERS = "Filters"
ITM_FINAL_TRIGGER = "FinalTrigger"
ITM_FIRMWARE_UPLOAD = "FirmwareUpload"
ITM_FIRMWARE_VERSION = "FirmwareVersion"
ITM_FIXED = "Fixed"
ITM_FLAGS = "Flags"
ITM_FLASH_DELAY = "FlashDelay"
ITM_FLEX_VIEW = "FlexView"
ITM_FOCAL_LENGTH = "FocalLength"
ITM_FOCUS = "Focus"
ITM_FOCUS_DISTANCE = "FocusDistance"
ITM_FOLDER_PATH = "FolderPath"
ITM_FOLLOW_DYNAMIC_OFFSETS = "FollowDynamicOffsets"
ITM_FONT = "Font"
ITM_FORCE = "Force"
ITM_FORCE_GRAYSCALE = "ForceGrayscale"
ITM_FORCED_RAW_IMAGE_SIZE = "ForcedRawImageSize"
ITM_FORCED_RECTIFIED_IMAGE_SIZE = "ForcedRectifiedImageSize"
ITM_FREQUENCY = "Frequency"
ITM_FROM_DYNAMIC = "FromDynamic"
ITM_FRONT_LIGHT = "FrontLight"
ITM_GAIN = "Gain"
ITM_GAIN_BOOST = "GainBoost"
ITM_GATEWAY = "Gateway"
ITM_GENERATE_EMPTY_CALIBRATION = "GenerateEmptyCalibration"
ITM_GLOBAL_PATTERN_DATA_UPDATED = "GlobalPatternDataUpdated"
ITM_GLOBAL_SHUTTER = "GlobalShutter"
ITM_GLOW = "Glow"
ITM_GRAVITY = "Gravity"
ITM_GREEN = "Green"
ITM_GRID_SIZE = "GridSize"
ITM_GRID_SPACING = "GridSpacing"
ITM_GROUND_PLANE = "GroundPlane"
ITM_HUD = "HUD"
ITM_HALF_VERGENCE = "HalfVergence"
ITM_HARDWARE_FAILURE = "HardwareFailure"
ITM_HARDWARE_GAMMA = "HardwareGamma"
ITM_HAS_LICENSE = "HasLicense"
ITM_HASH = "Hash"
ITM_HDR = "Hdr"
ITM_HEIGHT = "Height"
ITM_HIGH_QUALITY_RENDERING = "HighQualityRendering"
ITM_HORIZONTAL = "Horizontal"
ITM_IO = "IO"
ITM_IGNORE_ENSENSO_PATTERN_ENCODING = "IgnoreEnsensoPatternEncoding"
ITM_IMAGE_BUFFER = "ImageBuffer"
ITM_IMAGE_DOWNLOAD_LIMIT = "ImageDownloadLimit"
ITM_IMAGE_FOLDER = "ImageFolder"
ITM_IMAGE_NAME = "ImageName"
ITM_IMAGE_OFFSET = "ImageOffset"
ITM_IMAGE_SET = "ImageSet"
ITM_IMAGE_SIZE = "ImageSize"
ITM_IMAGES = "Images"
ITM_INDEX = "Index"
ITM_INFO = "Info"
ITM_INFO_TIMEOUT = "InfoTimeout"
ITM_INITIAL_TRIGGER = "InitialTrigger"
ITM_INITIAL_VELOCITY = "InitialVelocity"
ITM_INLIER_COUNT = "InlierCount"
ITM_INLIER_FRACTION = "InlierFraction"
ITM_INLIER_THRESHOLD = "InlierThreshold"
ITM_INPUT = "Input"
ITM_INTEGRATED = "Integrated"
ITM_INTERFACE = "Interface"
ITM_INTERNAL_TRIGGER = "InternalTrigger"
ITM_INTERVAL = "Interval"
ITM_INVERSE = "Inverse"
ITM_INVERT = "Invert"
ITM_IP_ADDRESS = "IpAddress"
ITM_IP_BROADCAST = "IpBroadcast"
ITM_IP_SUBNET_MASK = "IpSubnetMask"
ITM_ITEM_TYPES = "ItemTypes"
ITM_ITEMS = "Items"
ITM_ITERATIONS = "Iterations"
ITM_K1 = "K1"
ITM_K2 = "K2"
ITM_K3 = "K3"
ITM_KEEP_ALIVE_TIMEOUT = "KeepAliveTimeout"
ITM_LED = "LED"
ITM_LATEST_MESSAGE = "LatestMessage"
ITM_LEFT = "Left"
ITM_LEFT_BOTTOM = "LeftBottom"
ITM_LEFT_TOP = "LeftTop"
ITM_LENS = "Lens"
ITM_LENSES = "Lenses"
ITM_LEVEL = "Level"
ITM_LIGHTING = "Lighting"
ITM_LINK = "Link"
ITM_LINKS = "Links"
ITM_LIST_CAL_TABS = "ListCalTabs"
ITM_LIST_LENSES = "ListLenses"
ITM_LIST_MODELS = "ListModels"
ITM_LIST_PATTERNS = "ListPatterns"
ITM_LIST_SENSORS = "ListSensors"
ITM_LOAD_CALIBRATION = "LoadCalibration"
ITM_LOCAL_EEPROM_FILE = "LocalEepromFile"
ITM_LOW_BANDWIDTH = "LowBandwidth"
ITM_MAC = "MAC"
ITM_MAC_ADDRESSES = "MacAddresses"
ITM_MAJOR = "Major"
ITM_MARK_FILTER_REGIONS = "MarkFilterRegions"
ITM_MARK_ONLY = "MarkOnly"
ITM_MASK = "Mask"
ITM_MASS = "Mass"
ITM_MASTER = "Master"
ITM_MATERIAL_BLUR = "MaterialBlur"
ITM_MAX = "Max"
ITM_MAX_EEPROM_FORMAT = "MaxEepromFormat"
ITM_MAX_FILE_SIZE = "MaxFileSize"
ITM_MAX_FLASH_TIME = "MaxFlashTime"
ITM_MAX_GAIN = "MaxGain"
ITM_MAX_POSE_ERROR = "MaxPoseError"
ITM_MAX_TOTAL_SIZE = "MaxTotalSize"
ITM_MAXIMUM_TRANSMISSION_UNIT = "MaximumTransmissionUnit"
ITM_MEASURE_CALIBRATION = "MeasureCalibration"
ITM_MEASURE_CONTRAST = "MeasureContrast"
ITM_MEASUREMENT_VOLUME = "MeasurementVolume"
ITM_MEDIAN_FILTER_RADIUS = "MedianFilterRadius"
ITM_MEMORY = "Memory"
ITM_MESSAGE = "Message"
ITM_MESSAGES = "Messages"
ITM_META_DATA = "MetaData"
ITM_META_INFO = "MetaInfo"
ITM_METHOD = "Method"
ITM_MIN = "Min"
ITM_MIN_DISPARITY = "MinDisparity"
ITM_MINIMUM_DISPARITY = "MinimumDisparity"
ITM_MINIMUM_VOLTAGE = "MinimumVoltage"
ITM_MINOR = "Minor"
ITM_MIRROR = "Mirror"
ITM_MODE = "Mode"
ITM_MODEL_NAME = "ModelName"
ITM_MODELS = "Models"
ITM_MONO_INTRINSIC = "MonoIntrinsic"
ITM_MONOCULAR = "Monocular"
ITM_MONOCULAR_CALIBRATION = "MonocularCalibration"
ITM_MONOCULAR_PATTERN_COUNT = "MonocularPatternCount"
ITM_MONTH = "Month"
ITM_MULTI_EXPOSURE_FACTOR = "MultiExposureFactor"
ITM_NAME = "Name"
ITM_NEAR = "Near"
ITM_NETWORK_ADAPTER = "NetworkAdapter"
ITM_NETWORK_ADAPTER_IP_ADDRESS = "NetworkAdapterIpAddress"
ITM_NETWORK_ADAPTER_IP_SUBNET_MASK = "NetworkAdapterIpSubnetMask"
ITM_NETWORK_TYPE = "NetworkType"
ITM_NODE = "Node"
ITM_NODES = "Nodes"
ITM_NOISE_LEVEL = "NoiseLevel"
ITM_NORMAL = "Normal"
ITM_NORMALS = "Normals"
ITM_NUMBER_OF_DISPARITIES = "NumberOfDisparities"
ITM_NUMBER_OF_IMAGE_SETS = "NumberOfImageSets"
ITM_NX_LIB = "NxLib"
ITM_OBJECT_POINTS = "ObjectPoints"
ITM_OBJECTS = "Objects"
ITM_OFFSET = "Offset"
ITM_OPEN = "Open"
ITM_OPEN_MP = "OpenMP"
ITM_OPERATING_SYSTEM = "OperatingSystem"
ITM_OPERATION = "Operation"
ITM_OPTICAL_AXIS = "OpticalAxis"
ITM_OPTIMIZATION_PROFILE = "OptimizationProfile"
ITM_OPTIONS = "Options"
ITM_OR = "Or"
ITM_OUTER_SIZE = "OuterSize"
ITM_OUTPUT = "Output"
ITM_OVERFLOW_POLICY = "OverflowPolicy"
ITM_OVERLAY = "Overlay"
ITM_OVERTEMPERATURE = "Overtemperature"
ITM_OVERWRITE_WITH_DYNAMIC = "OverwriteWithDynamic"
ITM_PACKETS_RESENT = "PacketsResent"
ITM_PADDING = "Padding"
ITM_PAIRED = "Paired"
ITM_PARAMETERS = "Parameters"
ITM_PATTERN = "Pattern"
ITM_PATTERN_BUFFER = "PatternBuffer"
ITM_PATTERN_COUNT = "PatternCount"
ITM_PATTERN_POSE = "PatternPose"
ITM_PATTERN_TYPE = "PatternType"
ITM_PATTERN_VOLUME = "PatternVolume"
ITM_PATTERNS = "Patterns"
ITM_PERSISTENT_OVERLAY = "PersistentOverlay"
ITM_PERSISTENT_PARAMETERS = "PersistentParameters"
ITM_PHASE_INTERPOLATION = "PhaseInterpolation"
ITM_PHYSICS = "Physics"
ITM_PIXEL_CLOCK = "PixelClock"
ITM_PIXEL_PITCH = "PixelPitch"
ITM_PIXEL_SIZE = "PixelSize"
ITM_PLANE = "Plane"
ITM_PLUGGED = "Plugged"
ITM_POINT_MAP = "PointMap"
ITM_POINTS = "Points"
ITM_POLARITY = "Polarity"
ITM_PORT = "Port"
ITM_POSE = "Pose"
ITM_POSE_ERROR = "PoseError"
ITM_POSES = "Poses"
ITM_POST_PROCESSING = "PostProcessing"
ITM_PRIMITIVE = "Primitive"
ITM_PROGRESS = "Progress"
ITM_PROGRESS_FACTOR = "ProgressFactor"
ITM_PROGRESS_GRID = "ProgressGrid"
ITM_PROGRESS_MASK = "ProgressMask"
ITM_PROGRESS_MASK_FACTOR = "ProgressMaskFactor"
ITM_PROGRESS_MODE = "ProgressMode"
ITM_PROJECTOR = "Projector"
ITM_PROJECTOR_DUTY_CYCLE = "ProjectorDutyCycle"
ITM_PROJECTOR_PATTERN = "ProjectorPattern"
ITM_PROJECTOR_POWER = "ProjectorPower"
ITM_PROPAGATION_DECAY = "PropagationDecay"
ITM_PROTECTION = "Protection"
ITM_RADIUS = "Radius"
ITM_RAW = "Raw"
ITM_RAW_AOI_INCREMENTS = "RawAoiIncrements"
ITM_RECALIBRATE = "Recalibrate"
ITM_RECTIFICATION = "Rectification"
ITM_RECTIFIED = "Rectified"
ITM_REDUCE = "Reduce"
ITM_REDUCED = "Reduced"
ITM_REFINEMENT = "Refinement"
ITM_REGION = "Region"
ITM_REGION_FILTER_DOWNSAMPLING = "RegionFilterDownsampling"
ITM_REGION_SIZE = "RegionSize"
ITM_RELATIVE = "Relative"
ITM_RELATIVE_AVERAGE_POSE_ERROR = "RelativeAveragePoseError"
ITM_RELATIVE_MAX_POSE_ERROR = "RelativeMaxPoseError"
ITM_REMOTE = "Remote"
ITM_RENDER_DEPTH_MAP = "RenderDepthMap"
ITM_RENDER_GROUND_TRUTH = "RenderGroundTruth"
ITM_RENDER_POINT_MAP = "RenderPointMap"
ITM_RENDER_POINT_MAP_TEXTURE = "RenderPointMapTexture"
ITM_RENDER_VIEW = "RenderView"
ITM_REPROJECTION = "Reprojection"
ITM_REPROJECTION_ERROR = "ReprojectionError"
ITM_REPROJECTION_ERROR_SCALE = "ReprojectionErrorScale"
ITM_RESET_CLOCK = "ResetClock"
ITM_RESIDUAL = "Residual"
ITM_RESTART_DAEMON = "RestartDaemon"
ITM_RESULT = "Result"
ITM_RETRIEVED = "Retrieved"
ITM_RETURN_ALL_PATTERN = "ReturnAllPattern"
ITM_REVERSE_PATH_FILTERING = "ReversePathFiltering"
ITM_RIGHT = "Right"
ITM_RIGHT_BOTTOM = "RightBottom"
ITM_RIGHT_TOP = "RightTop"
ITM_ROTATE = "Rotate"
ITM_ROTATION = "Rotation"
ITM_RUNNING = "Running"
ITM_RX = "Rx"
ITM_RY = "Ry"
ITM_SCALED_AREA_OF_INTEREST = "ScaledAreaOfInterest"
ITM_SCALED_MEASUREMENT_VOLUME = "ScaledMeasurementVolume"
ITM_SCALED_MINIMUM_DISPARITY = "ScaledMinimumDisparity"
ITM_SCALED_NUMBER_OF_DISPARITIES = "ScaledNumberOfDisparities"
ITM_SCALING = "Scaling"
ITM_SCORE = "Score"
ITM_SENSOR = "Sensor"
ITM_SENSORS = "Sensors"
ITM_SERIAL_NUMBER = "SerialNumber"
ITM_SETUP = "Setup"
ITM_SHADOWING_THRESHOLD = "ShadowingThreshold"
ITM_SHININESS = "Shininess"
ITM_SHOW_CAMERAS = "ShowCameras"
ITM_SHOW_GRID = "ShowGrid"
ITM_SHOW_OBJECT_POINTS = "ShowObjectPoints"
ITM_SHOW_PATTERN = "ShowPattern"
ITM_SHOW_PATTERN_POINTS = "ShowPatternPoints"
ITM_SHOW_PATTERNS = "ShowPatterns"
ITM_SHOW_RECTIFIED_AREA = "ShowRectifiedArea"
ITM_SHOW_SURFACE = "ShowSurface"
ITM_SHOW_USER_DEFINED_MODELS = "ShowUserDefinedModels"
ITM_SINK = "Sink"
ITM_SIZE = "Size"
ITM_SKEW = "Skew"
ITM_SOURCE = "Source"
ITM_SPECKLE_REMOVAL = "SpeckleRemoval"
ITM_SPECULAR = "Specular"
ITM_SPLIT_ROTATION = "SplitRotation"
ITM_START_DAEMON = "StartDaemon"
ITM_STATIC_BUFFER_COUNT = "StaticBufferCount"
ITM_STATIC_BUFFERS = "StaticBuffers"
ITM_STATUS = "Status"
ITM_STEREO = "Stereo"
ITM_STEREO_CALIBRATION = "StereoCalibration"
ITM_STEREO_CALIBRATION_ONLY = "StereoCalibrationOnly"
ITM_STEREO_EXTRINSIC = "StereoExtrinsic"
ITM_STEREO_INTRINSIC = "StereoIntrinsic"
ITM_STEREO_MATCHING = "StereoMatching"
ITM_STEREO_PATTERN_COUNT = "StereoPatternCount"
ITM_STOP_DAEMON = "StopDaemon"
ITM_SUBSAMPLING = "Subsampling"
ITM_SUBSET = "Subset"
ITM_SURFACE_CONNECTIVITY = "SurfaceConnectivity"
ITM_SYMBOL = "Symbol"
ITM_SYSTEM_INFO = "SystemInfo"
ITM_T1 = "T1"
ITM_T2 = "T2"
ITM_TARGET = "Target"
ITM_TARGET_BRIGHTNESS = "TargetBrightness"
ITM_TEMPERATURE = "Temperature"
ITM_TEMPORARY = "Temporary"
ITM_TEXT = "Text"
ITM_TEXTURE = "Texture"
ITM_THICKNESS = "Thickness"
ITM_THREADS = "Threads"
ITM_TILT_DIRECTION = "TiltDirection"
ITM_TIME = "Time"
ITM_TIME_EXECUTE = "TimeExecute"
ITM_TIME_FINALIZE = "TimeFinalize"
ITM_TIME_PREPARE = "TimePrepare"
ITM_TIMEOUT = "Timeout"
ITM_TIMESTAMP = "Timestamp"
ITM_TOLERANCE = "Tolerance"
ITM_TOP = "Top"
ITM_TRANSFORMATION = "Transformation"
ITM_TRANSFORMATIONS = "Transformations"
ITM_TRANSLATION = "Translation"
ITM_TRANSPORT_LAYER = "TransportLayer"
ITM_TRIGGER_DELAY = "TriggerDelay"
ITM_TRIGGER_MODE = "TriggerMode"
ITM_TRIGGERED = "Triggered"
ITM_TYPE = "Type"
ITM_U_EYE = "UEye"
ITM_USB = "USB"
ITM_UNIQUE_NAME = "UniqueName"
ITM_UNIQUENESS_OFFSET = "UniquenessOffset"
ITM_UNIQUENESS_RATIO = "UniquenessRatio"
ITM_UPDATE_GLOBAL_PATTERN_DATA = "UpdateGlobalPatternData"
ITM_UPDATER = "Updater"
ITM_URL = "Url"
ITM_USE_BUFFERED_PATTERNS = "UseBufferedPatterns"
ITM_USE_DISPARITY_MAP_AREA_OF_INTEREST = "UseDisparityMapAreaOfInterest"
ITM_USE_FLOAT16 = "UseFloat16"
ITM_USE_MODEL = "UseModel"
ITM_USE_OPEN_GL = "UseOpenGL"
ITM_USE_RECALIBRATOR = "UseRecalibrator"
ITM_USE_STEREO_TEXTURES = "UseStereoTextures"
ITM_USER = "User"
ITM_VALID_FIRMWARE = "ValidFirmware"
ITM_VALID_IP_ADDRESS = "ValidIpAddress"
ITM_VALID_REGION = "ValidRegion"
ITM_VALUE = "Value"
ITM_VALUES = "Values"
ITM_VERGENCE = "Vergence"
ITM_VERSION = "Version"
ITM_VERTICAL = "Vertical"
ITM_VIEW_POSE = "ViewPose"
ITM_VIGNETTING = "Vignetting"
ITM_WAIT_FOR = "WaitFor"
ITM_WAIT_FOR_PROJECTOR = "WaitForProjector"
ITM_WAIT_FOR_RECALIBRATION = "WaitForRecalibration"
ITM_WIDTH = "Width"
ITM_WIRING_TEST = "WiringTest"
ITM_WITH_OVERLAY = "WithOverlay"
ITM_WORLD_COORDINATES = "WorldCoordinates"
ITM_WRITE_FREQUENCY = "WriteFrequency"
ITM_YEAR = "Year"
ITM_YELLOW = "Yellow"
ITM_Z_BUFFER_ONLY = "ZBufferOnly"
VAL_ADD = "Add"
VAL_ALIGNED = "Aligned"
VAL_ALIGNED_AND_DIAGONAL = "AlignedAndDiagonal"
VAL_ALL = "All"
VAL_ALLOW = "Allow"
VAL_ARRAY = "Array"
VAL_ASSEMBLY = "Assembly"
VAL_AUTO = "Auto"
VAL_AVAILABLE = "Available"
VAL_AXIS = "Axis"
VAL_BINARY = "Binary"
VAL_BLOCK_MATCHING = "BlockMatching"
VAL_BOOLEAN = "Boolean"
VAL_BOTTOM = "Bottom"
VAL_BOX = "Box"
VAL_BUFFER = "Buffer"
VAL_CONSOLE = "Console"
VAL_CONTINUOUS = "Continuous"
VAL_CORRELATION = "Correlation"
VAL_CUBE = "Cube"
VAL_CUBOID = "Cuboid"
VAL_CYLINDER = "Cylinder"
VAL_DHCP = "DHCP"
VAL_DEBUG = "Debug"
VAL_DEBUG_OUT = "DebugOut"
VAL_DELAYED = "Delayed"
VAL_DIAGONAL = "Diagonal"
VAL_DISCARD_NEW = "DiscardNew"
VAL_DISCARD_OLD = "DiscardOld"
VAL_DOWN = "Down"
VAL_ENSENSO = "Ensenso"
VAL_ETHERNET = "Ethernet"
VAL_EUCLIDEAN = "Euclidean"
VAL_FALLING_EDGE = "FallingEdge"
VAL_FILE = "File"
VAL_FIXED = "Fixed"
VAL_FLEX_VIEW2 = "FlexView2"
VAL_FLEXIBLE = "Flexible"
VAL_FLOAT = "Float"
VAL_FORCE = "Force"
VAL_GRID_HEIGHT = "GridHeight"
VAL_GRID_SPACING = "GridSpacing"
VAL_GRID_WIDTH = "GridWidth"
VAL_HALCON = "Halcon"
VAL_HAND = "Hand"
VAL_HIDDEN = "Hidden"
VAL_HIGH = "High"
VAL_HIGH_ACTIVE = "HighActive"
VAL_IMAGE_POSITION = "ImagePosition"
VAL_IMMEDIATE = "Immediate"
VAL_IN_USE = "InUse"
VAL_INDEX = "Index"
VAL_INFO = "Info"
VAL_ITEM = "Item"
VAL_LEFT = "Left"
VAL_LEFT_TO_RIGHT = "LeftToRight"
VAL_LINK = "Link"
VAL_LINK_HIDDEN = "LinkHidden"
VAL_LOCKED = "Locked"
VAL_LOW = "Low"
VAL_LOW_ACTIVE = "LowActive"
VAL_MASK = "Mask"
VAL_MONOCULAR = "Monocular"
VAL_MOVING = "Moving"
VAL_NETWORK_TYPE_A = "NetworkTypeA"
VAL_NETWORK_TYPE_B = "NetworkTypeB"
VAL_NETWORK_TYPE_C = "NetworkTypeC"
VAL_NEW = "New"
VAL_NONE = "None"
VAL_NOT_SPECIFIED = "NotSpecified"
VAL_NULL = "Null"
VAL_NUMBER = "Number"
VAL_OBJECT = "Object"
VAL_OFF = "Off"
VAL_OPEN = "Open"
VAL_ORIGIN = "Origin"
VAL_PWM = "PWM"
VAL_PATTERN = "Pattern"
VAL_PERSISTENT = "Persistent"
VAL_PLANE = "Plane"
VAL_PROJECTOR = "Projector"
VAL_RANDOM = "Random"
VAL_RAW = "Raw"
VAL_RECTIFIED = "Rectified"
VAL_REPROJECTION_ERROR = "ReprojectionError"
VAL_RIGHT = "Right"
VAL_RIGHT_TO_LEFT = "RightToLeft"
VAL_RISING_EDGE = "RisingEdge"
VAL_SERIAL_NUMBER = "SerialNumber"
VAL_SGM_ALIGNED = "SgmAligned"
VAL_SGM_ALIGNED_AND_DIAGONAL = "SgmAlignedAndDiagonal"
VAL_SGM_DIAGONAL = "SgmDiagonal"
VAL_SINGLE = "Single"
VAL_SINGLE_CUSTOM = "SingleCustom"
VAL_SOFTWARE = "Software"
VAL_SPHERE = "Sphere"
VAL_STANDARD = "Standard"
VAL_STATIC = "Static"
VAL_STEREO = "Stereo"
VAL_STRING = "String"
VAL_STRUCTURE_LOCKED = "StructureLocked"
VAL_SUCCESSFUL = "Successful"
VAL_T_PIECE = "TPiece"
VAL_TILT_DIRECTION = "TiltDirection"
VAL_TOP = "Top"
VAL_TRACE = "Trace"
VAL_TRIGGERED = "Triggered"
VAL_TYPE = "Type"
VAL_USB = "USB"
VAL_UNKNOWN = "Unknown"
VAL_UNTRIGGERED = "Untriggered"
VAL_UP = "Up"
VAL_VALIDATE = "Validate"
VAL_VIRTUAL = "Virtual"
VAL_WORKSPACE = "Workspace"
VAL_X = "X"
VAL_XYZ = "XYZ"
VAL_Y = "Y"
VAL_Z = "Z"
VAL_ZYX = "ZYX"
# updated / overriden nxLib constants that are defined within the current loaded nxLib
CONSTANTS_PREFIX = {'Commands': 'cmd', 'Errors': 'err', 'Items': 'itm',
                    'Values': 'val', 'ApiErrors': 'NxLib', 'ItemTypes': 'NxLib'}

GET_CONSTANTS_CMD = "GetConstants"


def _update_constants_module():
    try:
        cmd = NxLibCommand(GET_CONSTANTS_CMD)
        cmd.execute()
        result = cmd.result()

        itm = result.as_json()
        json_object = json.loads(itm)

        for constant_type in json_object:
            if(isinstance(json_object[constant_type], list)):
                prefix = CONSTANTS_PREFIX[constant_type]
                for constant in json_object[constant_type]:
                    variable_name = None
                    value = None
                    if isinstance(constant, dict):
                        variable_name = prefix + constant['Name']
                        value = constant['Value']
                    else:
                        variable_name = prefix + constant
                        value = str(constant)
                    variable_name = convert_camel_to_upper_snake(variable_name)
                    if variable_name.startswith('NX_LIB'):
                        variable_name = fix_nxlib_prefix(variable_name)
                    globals()[variable_name] = value
    except:
        raise NxLibError("Could not load current nxlib constants. "
                         "It may be that your nxlib version does not support updating.")


try:
    _update_constants_module()
except NxLibException:
    pass
except:
    pass
