from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/locations')
def locations():
    return render_template('locations.html')


@bp.route('/participants')
def participants():
    return render_template('participants.html')


@bp.route('/trends')
def trends():
    return render_template('trends.html')
