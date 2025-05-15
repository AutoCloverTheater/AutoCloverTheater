from src.facades.Emulator.Emulator import ConnectEmulator, UpdateSnapShot, GetSnapShot
import pytesseract

from src.facades.Logx.Logx import logx

if __name__ == '__main__':
    ConnectEmulator()
    while True:
        UpdateSnapShot()
        img = GetSnapShot()
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'
        res = pytesseract.image_to_string(img, config=custom_config)
        logx.info(res)
        pass