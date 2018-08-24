from flask import render_template, flash, redirect, request, session, url_for
from app import app
from app.forms import SearchForm
from search import query_for_edge, get_graph
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
        g = get_graph()
        q = query_for_edge(g, edge)
        fnames = []
        for x in q:
            fnames.append(visualize_image(x, edges=[edge]))
        print(edge)
        print(q)
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
