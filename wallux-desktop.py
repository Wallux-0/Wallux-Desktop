import eel
import os
import sys
import requests

baseurl = "https://raw.githubusercontent.com/Wallux-0/Wallpapers/main/"

eel.init('web')

@eel.expose
def download_wallpaper(wallfile):
    if os.name=='nt':
        req = requests.get(baseurl+wallfile, stream=True)
        if req:
            img = req.raw.read()
            path = os.path.expanduser("~")
            path=path+"\\Pictures\\Wallux"
            try:
                os.mkdir(path)
            except:
                pass
            path=path+'\\'+(wallfile.lstrip("wallpapers/"))
            with open(path, 'wb') as f:
                f.write(img)
            return "Wallpaper Saved to {}".format(path)
        else:
            return "Could not download wallpaper ;-;"
    else:
        req = requests.get(baseurl+wallfile, stream=True)
        if req:
            img = req.raw.read()
            path = os.path.expanduser("~")
            path=path+"/Pictures/Wallux"
            try:
                os.mkdir(path)
            except:
                pass
            path=path+'/'+(wallfile.lstrip("wallpapers/"))
            with open(path, 'wb') as f:
                f.write(img)
            return "Wallpaper Saved to {}".format(path)
        else:
            return "Could not download wallpaper ;-;"

@eel.expose
def set_wallpaper(wallfile):
    if os.name=="nt":
        import ctypes
        req = requests.get(baseurl+wallfile, stream=True)
        if req:
            img = req.raw.read()
            path = os.path.expanduser("~")
            path=path+"\\Pictures\\Wallux"
            try:
                os.mkdir(path)
            except:
                pass
            path=path+'\\'+(wallfile.lstrip("wallpapers/"))
            with open(path, 'wb') as f:
                f.write(img)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        else:
            return "Could not get wallpaper. Try again!"
    else:
        req = requests.get(baseurl+wallfile, stream=True)
        if req:
            img = req.raw.read()
            path = os.path.expanduser("~")
            path=path+"/Pictures/Wallux"
            try:
                os.mkdir(path)
            except:
                pass
            path=path+'/'+(wallfile.lstrip("wallpapers/"))
            with open(path, 'wb') as f:
                f.write(img)
        else:
            return "Could not get wallpaper. Try again!"
        os.system("""echo $(ps -e | grep -E -i "xfce|kde|gnome") > /tmp/wallux.file""")
        parseStr = ''
        with open("/tmp/wallux.file") as f:
            parseStr = f.read()
        os.remove("/tmp/wallux.file")
        de = {}
        de['kde'] = parseStr.lower().count("kde")
        de['gnome'] = parseStr.lower().count('gnome')
        de['xfce'] = parseStr.lower().count('xfce')
        if max(de, key=de.get) == "gnome":
            os.system(
                "gsettings set org.gnome.desktop.background picture-uri file://{}".format(path))
            return "Wallpaper Set Successfully!"
        elif max(de, key=de.get) == "kde":
            import dbus
            plugin = 'org.kde.image'
            jscript = """
            var allDesktops = desktops();
            print (allDesktops);
            for (i=0;i<allDesktops.length;i++) {
                d = allDesktops[i];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                d.writeConfig("Image", "file://%s")
            }
            """
            bus = dbus.SessionBus()
            plasma = dbus.Interface(bus.get_object(
                'org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
            plasma.evaluateScript(jscript % (plugin, plugin, path))
            return "Wallpaper Set Successfully!"
        else:
            return "Desktop Environment not yet supported. Please create an issue at Wallux-Desktop repository to get support!"
    return "Wallpaper Set Successfully"

@eel.expose
def closed():
    sys.exit()

if os.name=="nt":
    if '--no-kiosk' not in sys.argv:
        x=os.system("start firefox -kiosk -private-window http://127.0.0.1:60001")
        if x==1:
            x=os.system("start chrome -kiosk -private-window http://127.0.0.1:60001")
        if x==1:
            x=os.system("start msedge -kiosk -private-window http://127.0.0.1:60001")
    else:
        x=os.system("start firefox -private-window http://127.0.0.1:60001")
        if x==1:
            x=os.system("start chrome -private-window http://127.0.0.1:60001")
        if x==1:
            x=os.system("start msedge -private-window http://127.0.0.1:60001")
    eel.start('index.html', mode=None, port=60001)
else:
    if '--no-kiosk' not in sys.argv:
        x=os.system("google-chrome-stable -kiosk -private-window http://127.0.0.1:60001 &")
        if x==1:
            x=os.system("firefox -kiosk -private-window http://127.0.0.1:60001 &")
        if x==1:
            x=os.system("msedge -kiosk -private-window http://127.0.0.1:60001 &")
    else:
        x=os.system("google-chrome-stable -private-window http://127.0.0.1:60001 &")
        if x==1:
            x=os.system("firefox -private-window http://127.0.0.1:60001 &")
        if x==1:
            x=os.system("msedge -private-window http://127.0.0.1:60001 &")
    eel.start('index.html', mode=None, port=60001)
