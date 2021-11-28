var theWallpaperDict = {};

var ScrollCounter = 0;

function onScrollFunction() {
    elem = document.getElementById('fullimg');
    elem.style.top = window.scrollY + 120;
    elem = document.getElementById('settingwallpaper');
    elem.style.top = window.scrollY + 140;
    elem = document.getElementById('downloadingwallpaper');
    elem.style.top = window.scrollY + 140;
    elem = document.getElementById('noInternet');
    elem.style.top = window.scrollY + 140;
}

window.addEventListener('scroll', function(event) { onScrollFunction() });

function shuffle(array) {
    var currentIndex = array.length,
        randomIndex;
    while (currentIndex != 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]
        ];
    }

    return array;
}

function openfullimage(id) {
    tagstr = '';
    id = parseInt(id);
    for (i in theWallpaperDict) {
        if (theWallpaperDict[i]['path'].replace(/\D/g, "") == id) {
            elem = theWallpaperDict[i];
        }
    }
    arr = elem['tags'];
    for (j in arr) {
        tagstr += arr[j];
        tagstr += ", ";
    }
    tagstr = tagstr.slice(0, -2);
    document.getElementById("fulldisp_img").src = "https://raw.githubusercontent.com/Wallux-0/Wallpapers/main/" + elem['path'];
    document.getElementById("fullimagedisplay_name").innerHTML = elem['name'];
    document.getElementById("fullimagedisplay_desc").innerHTML = elem['description'];
    document.getElementById("fullimagedisplay_id").innerHTML = "Wallux ID: " + elem['path'].replace(/\D/g, "");
    document.getElementById("fullimagedisplay_tags").innerHTML = tagstr;
    document.getElementById("fullimagedisplay_link_download_primary").onclick = function(){document.getElementById('downloadingwallpaper').style.display='block'; eel.download_wallpaper(elem['path'])(function(message){document.getElementById('downloadingwallpaper').style.display='none'; window.alert(message);});}
    document.getElementById("fullimagedisplay_link_set_as_wallpaper").onclick = function(){document.getElementById('settingwallpaper').style.display='block'; eel.set_wallpaper(elem['path'])(function(message){document.getElementById('settingwallpaper').style.display='none'; window.alert(message);});}
    document.getElementById("fullimagedisplay_link_set_as_wallpaper_secondary").onclick = function(){document.getElementById('settingwallpaper').style.display='block'; eel.set_wallpaper(elem['path'])(function(message){document.getElementById('settingwallpaper').style.display='none'; window.alert(message);});}
    document.getElementById("fullimagedisplay_link_download_secondary").onclick = function(){document.getElementById('downloadingwallpaper').style.display='block'; eel.download_wallpaper(elem['path'])(function(message){document.getElementById('downloadingwallpaper').style.display='none'; window.alert(message);});}
    document.getElementById("fullimg").style.display = 'block';
}

function onlyTags(tag) {
    final_array = shuffle(theWallpaperDict);
    var container_ = document.getElementById("randomContainer");
    container_.innerHTML = '';
    for (i in final_array) {
        tagstr = '';
        arr = final_array[i]['tags'];
        if (arr.indexOf(tag) >= 0) {
            for (j in arr) {
                tagstr += arr[j];
                tagstr += ", ";
            }
            tagstr = tagstr.slice(0, -2);
            container_.innerHTML +=
                "<div class=\"glassyContainer\" onclick=openfullimage(" + final_array[i]['path'].replace(/\D/g, "") + ")> <img class = \"imgDisp\" loading=\"lazy\" src = \"https://raw.githubusercontent.com/Wallux-0/Wallpapers/main/compressed/" + final_array[i]['path'] + "\"><div class=\"imgText\"> <b>" + final_array[i]['name'] + "</b><br>Description: " + final_array[i]['description'] + "<br>" + tagstr + "</b></div></div>"; //<br>Wallux ID: <b>" + final_array[i]['path'].replace(/\D/g, "") + 
        }
    }
}

function workwithdata(data) {
    var final_array = [];
    final_array = shuffle(data['wallpaper']);
    var container_ = document.getElementById("randomContainer");
    container_.innerHTML = '';
    for (i in final_array) {
        tagstr = '';
        arr = final_array[i]['tags'];
        for (j in arr) {
            tagstr += arr[j];
            tagstr += ", ";
        }
        tagstr = tagstr.slice(0, -2);
        container_.innerHTML +=
            "<div class=\"glassyContainer\" onclick=openfullimage(" + final_array[i]['path'].replace(/\D/g, "") + ")> <img class = \"imgDisp\" loading=\"lazy\" src = \"https://raw.githubusercontent.com/Wallux-0/Wallpapers/main/compressed/" + final_array[i]['path'] + "\"><div class=\"imgText\"> <b>" + final_array[i]['name'] + "</b><br>Description: " + final_array[i]['description'] + "<br>" + tagstr + "</b></div></div>"; //"<br>Wallux ID: <b>" + final_array[i]['path'].replace(/\D/g, "") +
    }
    var tagContainer = document.getElementById("tagContainer");
    tagContainer.innerHTML = '';
    tags = '';
    tarr = [];
    for (i in final_array) {
        arr = final_array[i]['tags'];
        for (j in arr) {
            if (tarr.indexOf(arr[j]) < 0) {
                tarr.push(arr[j]);
                tags += "<a onclick=\"onlyTags(\'" + arr[j] + "\')\"> <div class=\"tag\">" + arr[j] + "</div> </a>";
            }
        }
    }
    tagContainer.innerHTML = tags;
    theWallpaperDict = final_array;
};

window.addEventListener('offline', ()=>document.getElementById('noInternet').style.display='block')
if (window.navigator.onLine===false) {document.getElementById('noInternet').style.display='block'}
window.addEventListener('online', ()=>document.getElementById('noInternet').style.display='none')

$.ajax({
    url: "https://raw.githubusercontent.com/Wallux-0/Wallux/main/static/tags.json",
    success: function(data) {
        workwithdata(data);
    },
    error: function(data) {
        document.getElementById("noInternet").style.display = "block";
    },
    dataType: "json",
    timeout: 3000
});

window.addEventListener('mouseup', function(event) {
    var pol = document.getElementById('fullimg');
    if (event.target != pol && event.target.parentNode != pol) {
        document.getElementById("fulldisp_img").src = "";
        pol.style.display = 'none';
    }
});

$(window).bind('beforeunload', function() {eel.closed()})
