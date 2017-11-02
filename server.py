from flask import Flask, render_template, request, session, url_for, redirect
from crawling_qt import getQT
from crawling_notice import getNotice
from FIO_qt import writeQTpage
import time

app = Flask(__name__)

def getTime():
    t = time.strftime("%x", time.localtime(time.time())).split("/")
    t = t[2] + t[0] + t[1]
    return t

# ============================================================================

@app.route("/qt")
def qt():
    now = int(getTime())
    f = open("qt_date.txt", "r")
    date = int(f.readline())
    f.close()
#    if now != date:
#        all_qt = {}
#        for lang in ['kr', 'en', 'cn', 'jp']:
#            all_qt[lang] = getQT(lang)
#        writeQTpage(now, render_template("qt_page.html", all_qt=all_qt))
#        f = open("qt_date.txt", "w")
#        f.write(now)
#        f.close()
#    return render_template("qt_page_done.html")
    all_qt = []
    for lang in ['kr', 'en', 'cn', 'jp']:
        all_qt.append( getQT(lang) )
    return render_template("qt_page.html", all_qt=all_qt)

@app.route("/pc_mode")
def pc_mode():
    return redirect("http://jym.or.kr/?r=home&_page=&_make=main&a=pcmode")

@app.route("/notice")
def notice():
    notice = getNotice(20)
    return render_template("notice_page.html", notice=notice)

@app.route("/boot")
def boot_test():
    return render_template("bootstrap1.html")

@app.route("/timetable")
def time_table():
    return render_template("timetable.html")

@app.route("/timetable_demo")
def time_table_demo():
    return render_template("timetable_demo.html")

@app.route("/")
def root():
    lang = "kr"
    qt = getQT(lang)
    notice = getNotice(3)
    return render_template("index.html", qt=qt, notice=notice)

# =============================================================================

if __name__ == "__main__":
    f = open("qt_date.txt", "w")
    f.write("0")
    f.close()
    app.debug = True
    app.run(host="192.168.0.138", port=80, threaded=True)
