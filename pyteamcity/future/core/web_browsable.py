import webbrowser


class WebBrowsable(object):
    def open_web_browser(self):
        webbrowser.open(self.web_url)
