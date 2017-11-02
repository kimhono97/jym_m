def writeQTpage(now, txt):
    txt = str(txt)
    f = open("templates\\qt_page_done.html", "w")
    f.write(txt)
    f.close()
    return

            
