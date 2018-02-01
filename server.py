from flask import Flask, render_template, request, session, url_for, redirect
from crawling_qt import getQT
from crawling_notice import getNotice
from crawling_instagup import get_instagup
import datetime

app = Flask(__name__)

# ============================================================================

@app.route("/qt")
@app.route("/qt/<date>")
def qt(date="none"):
    if date == "none":
        now = datetime.datetime.now()
    else:
        date = date.split("-")
        now = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    prev = now - datetime.timedelta(days=1)
    next = now + datetime.timedelta(days=1)
    dates = {}
    dates['now'] = str(now.strftime("%Y-%m-%d"))
    dates['prev'] = str(prev.strftime("%Y-%m-%d"))
    dates['next'] = str(next.strftime("%Y-%m-%d"))
    
    all_qt = []
    for lang in ['kr', 'en', 'cn', 'jp']:
        all_qt.append( getQT(lang, dates['now']) )
        
    return render_template("qt_page.html", all_qt=all_qt, dates=dates)

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
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    lang = "kr"
    qt = getQT(lang, date)
    insta = get_instagup()
    notice = getNotice(3)
    return render_template("index.html", qt=qt, notice=notice, insta=insta)

# =============================================================================

if __name__ == "__main__":
    app.debug = True
    app.run(host="192.168.0.14", threaded=True)
    # AWS   : 172.31.44.210
    # JYM_c : 192.168.0.14 (175.193.125.177)
