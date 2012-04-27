import web
import zen_analytics

urls = (
    '/', 'index'
)

class index:
    def GET(self):
	return zen_analytics.start_zen_analytics()
        ##return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
