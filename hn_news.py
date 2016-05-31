import os
import signal
import json
import webbrowser
import pygtk
import gtk
from urllib2 import Request, urlopen, URLError
#from gi.repository import Gtk as gtk
#from gi.repository import AppIndicator3 as appindicator
import appindicator 
#from gi.repository import Notify as notify
import pynotify
from hackernews import HackerNews


#KEYWORDS
APPINDICATOR_ID = 'hn-indicator'
PYNOTIFY_ID = 'hn-indicator'
LIMIT = 3
ONE_MINUTE = 1000*60
DURATION = 30
REFRESH_DURATION = ONE_MINUTE*DURATION
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
    indicator.set_menu(build_menu(LIMIT))
    pynotify.init(APPINDICATOR_ID)
    gtk.main()
    #gtk.timeout_add(5000, update_widget)
    
def build_menu(LIMIT):
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

    item_change_refresh_duration = gtk.MenuItem('Change Refresh Duration')
    item_change_refresh_duration.connect('activate', get_refesh_duration)
    menu.append(item_change_refresh_duration)

    item_change_no_in_feed = gtk.MenuItem('Change number of items displayed in list')
    item_change_no_in_feed.connect('activate', get_feed_entry_number)
    menu.append(item_change_no_in_feed)

    separator2 = gtk.SeparatorMenuItem()
    menu.append(separator2)

    item_refresh = gtk.MenuItem('Refresh')
    item_refresh.connect('activate' , refresh)
    menu.append(item_refresh)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
            
    menu.show_all()
    return menu

def quit(_):
    #notify.uninit()
    show_notification(None, "Quitting", "Exiting from hn-indicator.")
    gtk.main_quit()

def get_data():
    hn = HackerNews()
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

#def show_notification(title, message):
#    notify.Notification.new(title, message, None).show()

def show_notification(self, title="Title", msg="Message", timeout=1000):
		notification = pynotify.Notification(title, msg)
		notification.set_timeout(timeout)
		notification.show()

def refresh(widget, limit):
    ids[:] = []
    titles[:] = []
    points[:] = []  
    urls[:] = []
    build_menu(limit)
    show_notification("Hacker News Widget updated!", "Click on the widget to view updated news feed.")


def get_refesh_duration(widget):
    DURATION = get_dialog_entry(None, "Enter duration after which feed should be refreshed (in mins): ")
    REFRESH_DURATION = DURATION*ONE_MINUTE
    print 'New refresh duration is - ' + REFRESH_DURATION
    show_notification(widget, "Settings updated!", "Successfully changed the refresh duration settings.")

def get_feed_entry_number(widget):
    LIMIT = get_dialog_entry(None, "Enter number of list items in feed (<10): ")
    print 'New limit is - ' + str(LIMIT)
    show_notification(widget, "Settings updated!", "Successfully changed the number of items in feed settings.")
    refresh(widget, LIMIT)

def get_dialog_entry(parent, message, default=''):
    """
    Display a dialog with a text entry.
    Returns the text, or None if canceled.
    """
    d = gtk.MessageDialog(parent,
                          gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                          gtk.MESSAGE_QUESTION,
                          gtk.BUTTONS_OK_CANCEL,
                          message)
    entry = gtk.Entry()
    entry.set_text(default)
    entry.show()
    d.vbox.pack_end(entry)
    entry.connect('activate', lambda _: d.response(gtk.RESPONSE_OK))
    d.set_default_response(gtk.RESPONSE_OK)

    r = d.run()
    text = entry.get_text().decode('utf8')
    d.destroy()
    if r == gtk.RESPONSE_OK:
        return text
    else:
        return None



if __name__ == "__main__" :
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
