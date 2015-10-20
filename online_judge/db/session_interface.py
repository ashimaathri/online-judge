from uuid import uuid4
from datetime import datetime, timedelta

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from online_judge.db import db

class MongoSession(CallbackDict, SessionMixin):

    def __init__(self, sid=None, initial=None):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)

        self.sid = sid
        self.modified = False

class MongoSessionInterface(SessionInterface):
    def __init__(self, collection='sessions'):
        self.store = db[collection]

    def generate_sid(self):
        return str(uuid4())

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        session = None

        if not sid:
            session = MongoSession(sid=self.generate_sid())

        else:
            stored_session = self.store.find_one({'sid': sid})

            if stored_session.get('expiration') > datetime.utcnow():
                session = MongoSession(initial=stored_session['data'],
                                       sid=stored_session['sid'])
            else:
                session = MongoSession(sid=self.generate_sid())

        return session

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)

        if not session:
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return

        expiration = self.get_expiration_time(app, session)

        if not expiration:
            expiration = datetime.utcnow() + timedelta(hours=1)

        self.store.update_one({'sid': session.sid},
                              {'$set': {'sid': session.sid, 'data': session, 'expiration': expiration}},
                              True)

        response.set_cookie(app.session_cookie_name,
                            session.sid,
                            expires=expiration,
                            httponly=True,
                            domain=domain)
