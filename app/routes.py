# -*- coding: utf-8

from flask import render_template, flash, redirect, request, session, url_for
from app import app
from app.forms import SearchForm
from ges_search import get_results_for_edge
from visualize_data import visualize_image
import os



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Thomas'}
    return render_template('index.html',
            title='Visual Genome Semantic Image Search',
            user=user)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if request.method == 'POST':
        subject = request.form.get('subject', 'man')
        relationship = request.form.get('relationship', 'in')
        object = request.form.get('object', 'chair')
        edge = (subject, relationship, object)
        fnames = get_results_for_edge(edge)
        session['fnames'] = fnames
        return redirect(url_for('results'))
    else:
        return render_template('search.html', title='Search', form=form)#, fnames=fnames)

@app.route('/results', methods=['GET', 'POST'])
def results():
    fnames = session['fnames']
    # pwd = os.getcwd()
    # fnames = [os.path.join(pwd, fname) for fname in fnames]
    print(fnames)
    return render_template('results.html', fnames=fnames)
