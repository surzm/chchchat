from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import time, simplejson
from flaskr.db import get_db

bp = Blueprint('message', __name__, url_prefix='/message')


@bp.route('/', methods=('GET'))
def post():
    messages = []

    return render_template('message/index.html', messages)


@bp.route('/post', methods=('POST'))
def post():
    if request.method == 'POST':
        body = request.form['body']
        post_id = request.form['post_id']
        db = get_db()
        error = None

        if body is None:
            error = 'Text did not send'

        if post_id:
            if db.execute(
                'SELECT id FROM message WHERE id = ?', (post_id)
            ).fetchone() is None:
                error = 'Post {} not found'.format(post_id),

        if error is None:
            db.execute(
                'INSERT INTO message (body, user_id, reply_post_id, created_at) VALUES (?, ?, ?, ?)',
                (body, session.get('user_id'), post_id, time.time())
            )
            db.commit()
            result = {'result': True}
        else:
            result = {'result': False, 'error': error}

    return simplejson.dump(result)
