from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_required, login_manager
from model import *


list = Blueprint(
    'list', __name__,
    template_folder='templates',
    static_folder='static'
)

@list.route('/movie-list', method=['GET'])
def movie_list():
    movie_lists = db.session.execute(db.select(MovieList).order_by(MovieList.text)).scalars()
    return render_template('home.html', movie_list=movie_lists)

@list.route('/add/<int:movie_id>',  method=['POST'])
def add_list(movie_id):
    movie = Movie.query.get_or_404(id)
    if MovieList.query.filter_by(user_id=current_user.id, movie_id=movie_id).first():
        flash('this movie is already added ')
    else:
        movie_list = MovieList(user_id=current_user.id, movie_id=movie_id)
        db.session.add(movie_list)
        db.session.commit()
        flash('movie added ')
    return redirect(url_for('user.movie_list'))

@list.route('/movie/remove/<int:movie_id>', methods=['POST'])
@login_required
def remove(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('movie removed.','success')
    return redirect(url_for('user.movie_list'))
