from functools import wraps

from flask import session, flash, render_template, redirect, url_for, request

__author__ = 'jslvtr'


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('user_blueprint.login', next=request.path))
        elif session['email'] == 'reservations@northerngrand.ca':
            message = ''
            if request.path != '/lostAndFound/':
                message = 'Access to Housekeeping Only'
                return render_template('user/login.html', message=message)
            return render_template('lostAndFound/lostAndFound_home.html')
        return f(*args, **kwargs)
    return decorated_function