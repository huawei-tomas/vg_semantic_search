from flask import render_template, flash, redirect, request
from app import app
from app.forms import SearchForm
from search import query_for_edge, get_graph
from visualize_data import visualize_image




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
    subject = request.form.get('subject', 'man')
    relationship = request.form.get('relationship', 'in')
    object = request.form.get('object', 'chair')
    edge = (subject, relationship, object)
    g = get_graph()
    q = query_for_edge(g, edge)
    fname = []
    for x in q:
        visualize_image(x, edges=[edge])
    print(edge)
    print(q)

    return render_template('search.html', title='Search', form=form)
