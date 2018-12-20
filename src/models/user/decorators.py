from functools import wraps

from flask import session, flash, render_template, redirect, url_for, request

__author__ = 'jslvtr'


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            flash(u'You need to be signed in for this page.')
            return redirect('/#/login')
        elif session['email'] == 'reservations@northerngrand.ca':
            print(request.path)
            if request.path != '/lostAndFound/':
                return redirect('/#/login')
            return redirect('/#/lost')
        return f(*args, **kwargs)
    return decorated_function
