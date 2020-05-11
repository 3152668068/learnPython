from datetime import datetime,timedelta
import requests
import os
import win32api,win32con,win32gui

def imgDown():
    try:
        urlBase = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/"
        today = str((datetime.utcnow() - timedelta(minutes=60)).strftime("%Y/%m/%d/"))
        hour = str((datetime.utcnow() - timedelta(minutes=60)).strftime("%H").zfill(2))
        second = str((datetime.utcnow() - timedelta(minutes=60)).strftime("%M")[0] + "0")
        minute = "00"
        urlEnd = "_0_0.png"
        url = urlBase + today + hour + second + minute + urlEnd
        img=None
        img = requests.get(url,timeout=5)
        if img==None:
            return False
        with open("earth.png", "wb") as file:
            file.write(img.content)
    except:
        return False
    else:
        return True


def setWallpaper(imagepath):
    try:
        keyex = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, "0")
        win32api.RegSetValueEx(keyex, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, win32con.SPIF_SENDWININICHANGE)
    except:
        return False
    else:
        return True




if __name__=='__main__':
    imgDown()
    path=os.getcwd()
    setWallpaper(os.path.join(os.getcwd(),"earth.png"))
