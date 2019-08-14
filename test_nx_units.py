from nxlib.nxproxy import NxLib, NxLibItem
import unittest   # The test framework

class Test_TestIs(unittest.TestCase):
    def test_isBool(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].isBool(), True)
    def test_isNotBool(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"].isBool(), False)

    def test_isNumber(self):
        self.assertEqual(NxLibItem()["Calibration"]["Pattern"]["GridSpacing"].isNumber(), True)
    def test_isNotNumber(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].isNumber(), False)

    def test_isString(self):
        self.assertEqual(NxLibItem()["Calibration"]["Pattern"]["Type"].isString(), True)
    def test_isNotString(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"].isString(), False)

    def test_isNull(self):
        self.assertEqual(NxLibItem()["Calibration"]["AssemblyCalibration"].isNull(), True)
    def test_isNotNull(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"].isNull(), False)

    def test_isObject(self):
        self.assertEqual(NxLibItem()["Calibration"]["Pattern"].isObject(), True)
    def test_isNotObject(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"]["ShowCameras"].isObject(), False)

    def test_isArray(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"]["Size"].isArray(), True)
    def test_isNotArray(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"].isArray(), False)

    def test_type(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"]["Size"].type(), 5)

    def test_exists(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView"].exists(), True)
    def test_doesnt_exist(self):
        self.assertEqual(NxLibItem()["DefaultParameters"]["RenderView2"].exists(), False)

if __name__ == '__main__':
    NxLib('NxLib32.dll')
    
    unittest.main()