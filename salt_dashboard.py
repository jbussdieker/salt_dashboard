# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/salt_dashboard.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/nodes')
def show_nodes():
    cur = g.db.execute('select name from nodes order by id desc')
    nodes = [dict(name=row[0]) for row in cur.fetchall()]
    return render_template('show_nodes.html', nodes=nodes, node_groups=[], node_classes=[])

@app.route('/nodes/<node>')
def show_node(node):
    cur = g.db.execute('select name from nodes where name = (?)', [node])
    node_obj = cur.fetchone()

    cur = g.db.execute('select id from nodes where name = (?)', [node])
    node_id = cur.fetchone()[0]

    cur = g.db.execute('select * from reports where node_id = (?)',
                 [node_id])
    reports = [dict(name=row[0]) for row in cur.fetchall()]
    return render_template('node.html', node=node_obj, reports=reports)

@app.route('/reports/upload', methods=['POST'])
def upload_report():
    cur = g.db.execute('select name from nodes where name = (?)', [request.json['id']])
    if cur.fetchone() == None:
      g.db.execute('insert into nodes (name) values (?)',
                   [request.json['id']])
      g.db.commit()

    cur = g.db.execute('select id from nodes where name = (?)', [request.json['id']])
    node_id = cur.fetchone()[0]

    g.db.execute('insert into reports (node_id) values (?)',
                 [node_id])
    g.db.commit()

    return redirect(url_for('show_nodes'))

if __name__ == '__main__':
    app.run()
