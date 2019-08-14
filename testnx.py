# import nxlib.nxproxy as nx
from nxlib.nxproxy import NxLib, NxLibItem, NxLibCommand
import cv2

if __name__ == "__main__" :
    
    nxLib = NxLib('NxLib32.dll')

    # print (nxLib.translateReturnCode(1))

    # gridSpacing = NxLibItem()["Calibration"]["Pattern"]["GridSpacing"]
    # gridSpacing.setInt(13)
    # NxLibItem()["Calibration"]["Pattern"]["GridSpacing"] = 14

    #print(gridSpacing.asInt())

    # print(NxLibItem()["Calibration"]["Pattern"].asJson())

    root = NxLibItem()
    print(root.asJson())


    angle = NxLibItem()["DefaultParameters"]["RenderView"]["ViewPose"]["Rotation"]["Angle"]

    print(angle.asDouble())
  
    # print(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].asBool())

    # print(NxLibItem()["DefaultParameters"]["RenderView"].count())

    NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].setBool(False)
    # print(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].asBool())
    # print(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].asJson())
    # NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].setBool(True)
    # print(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].asBool())
    # print(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].asJson())

    # NxLibItem()["Images"]["RenderView"].getBinaryData(1000)
    # //Cameras/FileN20-Test2/Images/Raw/Left

    # item not compatible
    # width, height, channelCount, bytesPerElement, isFloat, timestamp = NxLibItem()["Cameras"]["FileN20-Test2"]["Images"]["Raw"]["Left"].getBinaryDataInfo()
    
    # width, height, channelCount, bytesPerElement, isFloat, timestamp = NxLibItem()["Cameras"]["FileN20-Test2"]["Images"]["Raw"]["Right"].getBinaryDataInfo()

    # print(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].asJson())

    # print(NxLibItem()["Cameras"]["FileN20-Test2"].asJson())

    # print(NxLibItem()["Cameras"]["FileN20-Test2"]["ImageFolder"].asString())

    # print(NxLibItem()["Cameras"].name())

    # print(NxLibItem()["Calibration"]["Pattern"]["Type"].asString())
    # NxLibItem()["Calibration"]["Pattern"]["Type"].setString('test')
    # print(NxLibItem()["Calibration"]["Pattern"]["Type"].asString())
    # NxLibItem()["Calibration"]["Pattern"]["Type"] = None

    # print(NxLibItem()["Calibration"]["Pattern"].asJsonMeta())

    # print(NxLibItem()["Cameras"]["FileN20-Test2"]["ImageFolder"].asString())

    # itemName, errorCode = nxLib.getName("Execute")

    print(NxLibItem()[1].name())

    cmd = NxLibCommand("Default")
    cmd.parameters()["Cameras"] = "FileN20-Test2"
    print(NxLibItem()["Execute"]["Default"].asJson())
    cmd.execute("Open",True)
    print(NxLibItem()["Execute"]["Default"].asJson())
    cmd.parameters()["Cameras"] = "FileN20-Test2"
    cmd.execute("Capture",True)

    imgL = NxLibItem()["Cameras"]["FileN20-Test2"]["Images"]["Raw"]["Left"].getBinaryData()
    cv2.imshow('raw left', imgL)
    # cv2.waitKey(0)

    imgR = NxLibItem()["Cameras"]["FileN20-Test2"]["Images"]["Raw"]["Right"].getBinaryData()
    cv2.imshow('raw right', imgR)
    # cv2.waitKey(0)

    NxLibItem()["Execute"]["Default"]["TestImage"].setBinaryData(imgL)

    imgT = NxLibItem()["Execute"]["Default"]["TestImage"].getBinaryData()
    cv2.imshow('test', imgT)
    cv2.waitKey(0)