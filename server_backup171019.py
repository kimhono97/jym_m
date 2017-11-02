from flask import Flask, render_template, request, session, url_for, redirect
from crawling_qt import getQT
from crawling_notice import getNotice

app = Flask(__name__)

@app.route("/qt", methods=["GET"])
def qt():
    err = True
    lang = 'kr'
    k = request.args.get("lang")
    if k != None :
        lang = k
        err = False
    qt = getQT(lang)
    return render_template("qt_page.html", qt=qt)

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

if __name__ == "__main__":
    app.debug = True
    app.run(host="58.233.248.29", port=80, threaded=True)
