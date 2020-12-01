#controllers/index.py
import config, copy, json
from flask import render_template, redirect, session, request
from flask_classful import FlaskView, route
from controllers.post import Post

class Index(FlaskView):
    def __init__(self):
        self.post = Post()

    @route('/')
    def index(self):
        session['page'] = 0
        vdict = self.post.get_post()
        return render_template('index.html', data=vdict)

    @route('/panel')
    def get_post(self):
        nav = request.args.get('nav', 0, type=str)

        if nav == 'previous':
            session['page'] += 1
        elif nav == 'next':
            if session['page'] > 0:
                session['page'] -= 1
        else:
            session['page'] = 0

        vdict = self.post.get_post(page=session['page'])
        
        if not vdict['posts']:
            session['page'] -= 1

        return json.dumps(vdict)

    @route('/favicon.ico')
    def favicon(self):
        redirect('/static/images/site_logo.png')

    @route('/post/<id>')
    def get_single_post(self, id):
        vdict = self.post.get_single_post(id)
        return render_template('post.html', data=vdict)

    @route('/post/load/<label>')
    def load_post(self, label):
        vdict = self.post.get_post(config.vdict['post_max_category'], category=label)
        return vdict

    @route('/post/load/ajax/<label>')
    def load_post(self, label):
        ajax = request.args.get('ajax', 0, type=int)
        
        vdict = self.post.get_post(config.vdict['post_max_category'], category=label, page=ajax)
        return vdict

    @route('/category/<label>')
    def get_post_category(self, label):
        vdict = self.post.get_post(config.vdict['post_max_category'], category=label)
        return render_template('category.html', data=vdict)