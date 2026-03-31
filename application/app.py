from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from datetime import datetime
from config import Config
from models import db, Host, Horse, Jockey, Race, RaceResult

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.context_processor
def inject_now():
    """Make now() available in templates"""
    return {'now': datetime.utcnow}


@app.route('/')
def index():
    """Main page - list all races"""
    races = Race.query.all()
    return render_template('index.html', races=races)


@app.route('/hosts')
def hosts():
    """List all hosts (owners)"""
    hosts_list = Host.query.all()
    return render_template('hosts.html', hosts=hosts_list)


@app.route('/hosts/add', methods=['GET', 'POST'])
def add_host():
    """Add a new host (owner)"""
    if request.method == 'POST':
        first = request.form.get('host_name')
        last = request.form.get('surname')
        if not first or not last:
            flash('Please enter both first name and surname', 'error')
            return redirect(url_for('add_host'))
        
        # check duplicate by full name
        existing = Host.query.filter_by(host_name=first, surname=last).first()
        if existing:
            flash('Host already exists', 'error')
            return redirect(url_for('add_host'))
        
        new_host = Host(host_name=first, surname=last)
        db.session.add(new_host)
        db.session.commit()
        flash(f'Host {new_host.name} added successfully', 'success')
        return redirect(url_for('hosts'))
    
    return render_template('add_host.html')


@app.route('/horses')
def horses():
    """List all horses"""
    horses_list = Horse.query.all()
    return render_template('horses.html', horses=horses_list)


@app.route('/horses/add', methods=['GET', 'POST'])
def add_horse():
    """Add new horse"""
    hosts_list = Host.query.all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        rating = request.form.get('rating', 0)
        host_id = request.form.get('host_id')
        
        if not name or not host_id:
            flash('Please fill all fields', 'error')
            return redirect(url_for('add_horse'))
        
        if Horse.query.filter_by(horse_name=name).first():
            flash('Horse already exists', 'error')
            return redirect(url_for('add_horse'))
        
        try:
            new_horse = Horse(horse_name=name, rating=int(rating), host_id=int(host_id))
            db.session.add(new_horse)
            db.session.commit()
            flash(f'Horse {name} added successfully', 'success')
            return redirect(url_for('horses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('add_horse'))
    
    return render_template('add_horse.html', hosts=hosts_list)


@app.route('/jockeys')
def jockeys():
    """List all jockeys"""
    jockeys_list = Jockey.query.all()
    return render_template('jockeys.html', jockeys=jockeys_list)


@app.route('/jockeys/add', methods=['GET', 'POST'])
def add_jockey():
    """Add new jockey"""
    if request.method == 'POST':
        name = request.form.get('name')
        rating = request.form.get('rating', 0)
        
        if not name:
            flash('Please enter jockey name', 'error')
            return redirect(url_for('add_jockey'))
        
        if Jockey.query.filter_by(name=name).first():
            flash('Jockey already exists', 'error')
            return redirect(url_for('add_jockey'))
        
        try:
            new_jockey = Jockey(name=name, rating=float(rating))
            db.session.add(new_jockey)
            db.session.commit()
            flash(f'Jockey {name} added successfully', 'success')
            return redirect(url_for('jockeys'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('add_jockey'))
    
    return render_template('add_jockey.html')


@app.route('/races')
def races():
    """List all races"""
    races_list = Race.query.all()
    return render_template('races.html', races=races_list)


@app.route('/races/add', methods=['GET', 'POST'])
def add_race():
    """Add new race"""
    horses_list = Horse.query.all()
    jockeys_list = Jockey.query.all()
    
    if request.method == 'POST':
        date_str = request.form.get('date')
        
        if not date_str:
            flash('Please enter race date', 'error')
            return redirect(url_for('add_race'))
        
        try:
            race_date = datetime.fromisoformat(date_str)
            # ``Race`` expects a date object (field is race_date)
            new_race = Race(race_date=race_date.date())
            db.session.add(new_race)
            db.session.flush()  # Get the race ID
            
            # Add race entries
            entries_added = 0
            for i in range(10):  # Support up to 10 entries
                horse_id = request.form.get(f'horse_{i}')
                jockey_id = request.form.get(f'jockey_{i}')
                
                if horse_id and jockey_id:
                    entry = RaceResult(
                        race_id=new_race.id,
                        horse_id=int(horse_id),
                        jockey_id=int(jockey_id),
                        place=None
                    )
                    db.session.add(entry)
                    entries_added += 1
            
            if entries_added == 0:
                db.session.rollback()
                flash('Please add at least one horse-jockey pair', 'error')
                return redirect(url_for('add_race'))
            
            db.session.commit()
            flash(f'Race created successfully with {entries_added} entries', 'success')
            return redirect(url_for('races'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('add_race'))
    
    return render_template('add_race.html', horses=horses_list, jockeys=jockeys_list)


@app.route('/races/<int:race_id>')
def race_detail(race_id):
    """View race details"""
    race = Race.query.get_or_404(race_id)
    return render_template('race_detail.html', race=race)


@app.route('/races/<int:race_id>/edit-results', methods=['GET', 'POST'])
def edit_race_results(race_id):
    """Edit race results (placements)"""
    race = Race.query.get_or_404(race_id)
    
    if request.method == 'POST':
        try:
            for entry in race.results:
                place_str = request.form.get(f'place_{entry.id}')
                if place_str:
                    entry.place = int(place_str)
            
            db.session.commit()
            flash('Race results updated successfully', 'success')
            return redirect(url_for('race_detail', race_id=race_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('edit_race_results.html', race=race)


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Only call ``create_all`` when using the default sqlite backend.  The
    # PostgreSQL database should be created (and tables migrated) via the
    # `db/init_db.sql` script and Alembic; running ``create_all`` against a
    # production Postgres instance may inadvertently drop or modify data.
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if uri.startswith('sqlite'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
