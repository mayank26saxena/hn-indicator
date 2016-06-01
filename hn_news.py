import os
import signal
import json
import webbrowser
import pygtk
import gtk
from urllib2 import Request, urlopen, URLError
import appindicator 
import pynotify
from hackernews import HackerNews


#KEYWORDS
APPINDICATOR_ID = 'hn-indicator'
PYNOTIFY_ID = 'hn-indicator'
LIMIT = 3
ONE_MINUTE = 1000*60
ONE_HOUR = 60
DURATION = 1
REFRESH_DURATION = ONE_MINUTE*ONE_HOUR*DURATION
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
    indicator = appindicator.Indicator(APPINDICATOR_ID, os.path.abspath('hackernews.png'), appindicator.CATEGORY_COMMUNICATIONS)
    indicator.set_status(appindicator.STATUS_ACTIVE)
    indicator.set_menu(build_menu())
    pynotify.init(APPINDICATOR_ID)
    gtk.main()
    #gtk.timeout_add(5000, update_widget)
    
def build_menu():
    menu = gtk.Menu()

    get_data()

    #print titles, points, urls

    global LIMIT
    print 'In build_menu() method and value of limit is - ' + str(LIMIT)
    news = ['?']*LIMIT
    item = ['?']*LIMIT
    
    for i in range(0,LIMIT):
        news[i] = str(titles[i]) + SPACE + DASH + SPACE + str(points[i]) + SPACE + POINTS
    
    for i in range(0,LIMIT):    
        item[i] = gtk.MenuItem(news[i])
        item[i].connect('activate', open_url,urls[i])
        menu.append(item[i])

    separator = gtk.SeparatorMenuItem()
    menu.append(separator)

    item_refresh_control = gtk.MenuItem("Adjust refresh time")
    menu_refresh_control = gtk.Menu()
    menu_refresh_control_items = []
    group = [None]
    time_interval_list = [1, 2, 3, 4]
    for i in time_interval_list:
        subitem = gtk.RadioMenuItem(group[0], str(i) + " hours")
        subitem.connect('activate', update_time_interval)
        menu_refresh_control.append(subitem)
        menu_refresh_control_items.append(subitem)
        group = subitem.get_group()
    item_refresh_control.set_submenu(menu_refresh_control)
    menu.append(item_refresh_control)

    item_feed_control = gtk.MenuItem("Adjust number of items in feed")
    menu_feed_control = gtk.Menu()
    menu_feed_control_items = []
    group2 = [None]
    number_of_items_list = [3,4,5]
    for i in number_of_items_list:
        subitem = gtk.RadioMenuItem(group2[0], str(i) + " items")
        subitem.connect('activate', update_number_of_items_in_feed)
        menu_feed_control.append(subitem)
        menu_feed_control_items.append(subitem)
        group2 = subitem.get_group()
    item_feed_control.set_submenu(menu_feed_control)
    menu.append(item_feed_control)

    separator2 = gtk.SeparatorMenuItem()
    menu.append(separator2)

    item_refresh = gtk.MenuItem('Refresh')
    item_refresh.connect('activate', refresh)
    menu.append(item_refresh)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
            
    menu.show_all()
    return menu


def update_time_interval(source):
    new_update_interval = int(source.get_label().split()[0])
    global REFRESH_DURATION
    print 'New time limit is : ' + str(new_update_interval)
    print 'Old refresh interval is ' + str(REFRESH_DURATION)
    print 'Old duration is ' + str(DURATION)
    DURATION = new_update_interval
    REFRESH_DURATION = ONE_MINUTE*ONE_HOUR*DURATION
    print 'New duration is ' + str(DURATION) 
    print 'New refresh interval is ' + str(REFRESH_DURATION)
    show_notification(None, "Settings updated!", "Successfully changed the refresh duration settings.")

def update_number_of_items_in_feed(source):
    new_items_limit = int(source.get_label().split()[0])
    global LIMIT
    print 'Old LIMIT is ' + str(LIMIT)
    print 'New number of items in feed is : ' + str(new_items_limit)
    LIMIT = new_items_limit
    print 'New LIMIT is ' + str(LIMIT)
    show_notification(None, "Settings updated!", "Successfully changed the number of items in feed settings.")
    refresh
    
def quit(widget):
    #notify.uninit()
    show_notification(None, "Quitting", "Exiting from hn-indicator.")
    gtk.main_quit()

def get_data():
    hn = HackerNews()
    #global LIMIT
    ids = hn.top_stories(limit=LIMIT)
    for i in range(0,LIMIT):
        b = hn.get_item(ids[i])
        titles.append(b.title.encode('utf8'))
        points.append(b.score)
        urls.append(b.url) 

    print titles
    print points
    print urls

def open_url(widget,url):
    webbrowser.open(url)

def show_notification(self, title="Title", msg="Message", timeout=1000):
		notification = pynotify.Notification(title, msg)
		notification.set_timeout(timeout)
		notification.show()

def refresh(widget):
    ids[:] = []
    titles[:] = []
    points[:] = []  
    urls[:] = []
    build_menu()
    show_notification(None,"Hacker News Widget updated!", "Click on the widget to view updated news feed.")


if __name__ == "__main__" :
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
