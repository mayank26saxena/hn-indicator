import os
import signal
import json
import webbrowser
from urllib2 import Request, urlopen, URLError
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from hackernews import HackerNews

#KEYWORDS
APPINDICATOR_ID = 'hn-news-indicator'
LIMIT = 3
SPACE = ' '
DASH = '-'
POINTS = 'Points'

ids = []
titles = []
points = []
urls = []
news = ['?']*LIMIT
item = ['?']*LIMIT

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('hackernews.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()
    
def build_menu():
    menu = gtk.Menu()

    get_data()

    #print titles, points, urls

    for i in range(0,LIMIT):
        news[i] = str(titles[i]) + SPACE + DASH + SPACE + str(points[i]) + SPACE + POINTS
    
    for i in range(LIMIT):
        item[i] = gtk.MenuItem(news[i])
        item[i].connect('activate', open_url,urls[i])
        menu.append(item[i])

    separator = gtk.SeparatorMenuItem()
    menu.append(separator)

    item_refresh = gtk.MenuItem('Refresh')
    item_refresh.connect('activate' , main)
    menu.append(item_refresh)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
            
    menu.show_all()
    return menu

def quit(_):
    notify.uninit()
    gtk.main_quit()

def get_data():
    hn = HackerNews()
    ids = hn.top_stories(limit=LIMIT)
    for i in range(0,LIMIT):
        b = hn.get_item(ids[i])
        titles.append(b.title)
        points.append(b.score)
        urls.append(b.url) 

    print titles
    print points
    print urls

def open_url(widget,url):
    webbrowser.open(url)

if __name__ == "__main__" :
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
