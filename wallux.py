import webview
import requests
from flask import Flask, after_this_request
import os
import threading
import sys
from functools import partial
import signal

app=Flask(__name__)
app.secret_key=os.urandom(12)

baseurl = "https://raw.githubusercontent.com/Wallux-0/Wallpapers/main/"
tempbaseurl = "https://raw.githubusercontent.com/Wallux-0/Wallpapers/main/compressed/"
req = requests.get(
    "https://raw.githubusercontent.com/Wallux-0/Wallux/main/static/tags.json")

errorHTML="""<html><style>html{background: rgba(2, 0, 36, 0.432); background: linear-gradient(47deg, rgba(2, 0, 36, 0.438) 0%, rgba(93, 7, 106, 0.438) 39%, rgba(112, 9, 121, 0.438) 59%, rgba(255, 0, 187, 0.432) 100%); backdrop-filter: blur(5px); color: #f5f5f5;}</style><body> <center> <h2>Oops. Internet not available<br>Connect to a valid connection and try again!</h2> </center></body></html>
"""
homeHTML0="""
<html><script src="https://code.jquery.com/jquery-3.6.0.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/notify/0.4.2/notify.min.js" integrity="sha512-efUTj3HdSPwWJ9gjfGR71X9cvsrthIA78/Fvd/IN+fttQVy7XWkOAXb295j8B3cmm/kFKVxjiNYzKw9IQJHIuQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script><style>@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap'); @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap'); body{background: linear-gradient(77deg, #d616c686, #030303, #56167477, #0e287e77, #640a3581, #000000); background-size: 1200% 1200%; -webkit-animation: GradientBg 30s ease infinite; -moz-animation: GradientBg 30s ease infinite; animation: GradientBg 30s ease infinite; font-family: 'Roboto', sans-serif; color: #f5f5f5bb;}@-webkit-keyframes GradientBg{0%{background-position: 0% 35%}50%{background-position: 100% 66%}100%{background-position: 0% 35%}}@-moz-keyframes GradientBg{0%{background-position: 0% 35%}50%{background-position: 100% 66%}100%{background-position: 0% 35%}}@keyframes GradientBg{0%{background-position: 0% 35%}50%{background-position: 100% 66%}100%{background-position: 0% 35%}}.title{display: inline-block; font-family: 'Montserrat', sans-serif; color: #f5f5f5; font-size: 80; font-weight: bolder; text-align: center;}.description{font-size: 23; text-align: center;}::placeholder{color: hsl(0, 0%, 79%);}.search{text-align: center; font-family: 'Montserrat', sans-serif; color: hsl(0, 0%, 79%); font-weight: lighter; font-size: 28; margin-top: 2vh; background-color: rgba(255, 255, 255, 0.233); border: none; border-radius: 0.5vh; outline: none; -webkit-box-shadow: none; -moz-box-shadow: none; box-shadow: none; width: 30vh;}.searchBtn{color: hsl(0, 0%, 79%); background-color: rgba(255, 255, 255, 0); border: none; -webkit-box-shadow: none; -moz-box-shadow: none; box-shadow: none; font-size: 28; cursor: pointer;}.container{margin: 1vh; margin-top: 5vh;}.glassyContainer{display: inline-block; background: rgba( 255, 255, 255, 0.20); backdrop-filter: blur( 2.0px); -webkit-backdrop-filter: blur( 2.0px); border-radius: 0.5vh; width: auto; height: auto; padding: 5 5 5 5; margin: 1vh;}.imgDisp{width: 40vh;}.imgText{margin-top: 0.4vh; text-align: center;}a{color: #ee82ee; cursor: pointer;}.close{display: inline-block;}</style><script>function setWall(wallid){try{$.get("http://127.0.0.1:45555/setWallpaper/" + wallid); $.notify("Wallpaper will be set in a few moments. Please don't close app until then.", "success");}catch{$.notify("Could not set wallpaper ;(", "error");}}</script><body> <div class="close"> <a href="http://127.0.0.1:45555/close" class="imgText">Exit</a> </div><center> <div class="title"> Wallux </div><br>
"""
homeHTML1="""</center></body></html>"""

if req:
    content = eval(req.content)
    content = content['wallpaper']
else:
    webview.create_window("Wallux", html=errorHTML, width=900, height=100, transparent=True)
    webview.start()

@app.route("/setWallpaper/<walluxid>", methods=["GET"])
def setWallpaper(walluxid):
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    for w in content:
        if str(walluxid) == ''.join([n for n in w['path'] if n.isdigit()]):
            req = requests.get(baseurl+w['path'], stream=True)
            success=False
            while not success:
                if req:
                    img = req.raw.read()
                    path = os.path.expanduser(
                        "~/Documents/"+w['path'].lstrip("wallpapers/").strip())
                    try:
                        os.remove(path)
                    except:
                        pass
                    with open(path, 'wb') as f:
                        f.write(img)
                    success=True
            break
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
        print("[SUCCESS] Enjoy your new wallpaper!")
        exit()
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
        exit()
    return {"error": 0}

@app.route("/close", methods=["GET"])
def closed():
    window.destroy()
    for line in os.popen("ps ax | grep wallux | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)
    sys.exit()

t=''
for wall in content:
    tags=''
    for tag in wall['tags']:
        tags+=tag
        tags+=", "
    tags.rstrip(", ")
    t+='<div class="glassyContainer">'
    t+='<img src="{}" class="imgDisp" loading=lazy>'.format(tempbaseurl+wall['path'])
    t+='<div class="imgText">{}</div>'.format(wall['name'])
    t+='<div class="imgText">{}</div>'.format(wall['description'])
    t+='<div class="imgText">{}</div>'.format(tags)
    t+="""<div class="imgText"><a onclick="setWall({})">Set Wallpaper</a></div>""".format(''.join([n for n in wall['path'] if n.isdigit()]))
    t+="</div></div>"
homeHTML=homeHTML0+t+homeHTML1

window=webview.create_window("Wallux", html=homeHTML, fullscreen=True, transparent=True)
partial_run=partial(app.run, port=45555, debug=False, use_reloader=False)
thrd=threading.Thread(target=partial_run)
thrd.start()
webview.start(window)
