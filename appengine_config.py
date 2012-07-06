from gaesessions import SessionMiddleware 
def webapp_add_wsgi_middleware(app): 
	app = SessionMiddleware(app, cookie_key="dsijfb3459whefwiuhr39wfpwor209u30ru3wifjwj3f08wfuw08ef0384r38whf") 
	return app