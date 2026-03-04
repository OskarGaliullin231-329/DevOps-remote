"""
Sample data initialization script - OPTIONAL
This script populates the database with sample data for testing.
Run with: python init_data.py
"""

from app import app, db
from models import Host, Horse, Jockey, Race, RaceResult
from datetime import datetime, timedelta

def init_sample_data():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Check if data already exists
        if Host.query.first() is not None:
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Initializing sample data...")
        
        # Create hosts
        hosts = [
            Host(host_name="John", surname="Smith"),
            Host(host_name="Sarah", surname="Johnson"),
            Host(host_name="Michael", surname="Brown"),
            Host(host_name="Emma", surname="Wilson"),
        ]
        for host in hosts:
            db.session.add(host)
        db.session.commit()
        print(f"✓ Created {len(hosts)} hosts")
        
        # Create horses
        horses_data = [
            ("Thunder", 8, hosts[0]),
            ("Lightning", 8, hosts[0]),
            ("Midnight", 9, hosts[1]),
            ("Sunset", 8, hosts[1]),
            ("Storm", 9, hosts[2]),
            ("Golden Dream", 8, hosts[2]),
            ("Silver Moon", 8, hosts[3]),
            ("Wind Dance", 8, hosts[3]),
        ]
        
        horses = []
        for name, rating, host in horses_data:
            horse = Horse(horse_name=name, rating=rating, host_id=host.id)
            horses.append(horse)
            db.session.add(horse)
        db.session.commit()
        print(f"✓ Created {len(horses)} horses")
        
        # Create jockeys
        jockeys_data = [
            ("James Lewis", 9),
            ("Maria Garcia", 9),
            ("David Wilson", 8),
            ("Anna Martinez", 9),
            ("Robert Taylor", 8),
            ("Catherine Anderson", 9),
        ]
        
        jockeys = []
        for name, rating in jockeys_data:
            jockey = Jockey(jockey_name=name, rating=rating)
            jockeys.append(jockey)
            db.session.add(jockey)
        db.session.commit()
        print(f"✓ Created {len(jockeys)} jockeys")
        
        # Create races with entries
        base_date = datetime.now() - timedelta(days=10)
        
        # Race 1 - Finished
        race1 = Race(race_date=base_date.date())
        db.session.add(race1)
        db.session.flush()
        
        race1_entries = [
            RaceResult(race_id=race1.id, horse_id=horses[0].id, jockey_id=jockeys[0].id, place=1),
            RaceResult(race_id=race1.id, horse_id=horses[1].id, jockey_id=jockeys[1].id, place=2),
            RaceResult(race_id=race1.id, horse_id=horses[2].id, jockey_id=jockeys[2].id, place=3),
            RaceResult(race_id=race1.id, horse_id=horses[3].id, jockey_id=jockeys[3].id, place=4),
        ]
        for entry in race1_entries:
            db.session.add(entry)
        
        # Race 2 - Finished
        race2 = Race(race_date=(base_date + timedelta(days=2)).date())
        db.session.add(race2)
        db.session.flush()
        
        race2_entries = [
            RaceResult(race_id=race2.id, horse_id=horses[4].id, jockey_id=jockeys[4].id, place=1),
            RaceResult(race_id=race2.id, horse_id=horses[5].id, jockey_id=jockeys[5].id, place=2),
            RaceResult(race_id=race2.id, horse_id=horses[6].id, jockey_id=jockeys[0].id, place=3),
            RaceResult(race_id=race2.id, horse_id=horses[7].id, jockey_id=jockeys[1].id, place=4),
        ]
        for entry in race2_entries:
            db.session.add(entry)
        
        # Race 3 - Scheduled (no results)
        race3 = Race(race_date=(datetime.now() + timedelta(days=5)).date())
        db.session.add(race3)
        db.session.flush()
        
        race3_entries = [
            RaceResult(race_id=race3.id, horse_id=horses[0].id, jockey_id=jockeys[2].id, place=1),
            RaceResult(race_id=race3.id, horse_id=horses[3].id, jockey_id=jockeys[4].id, place=2),
            RaceResult(race_id=race3.id, horse_id=horses[5].id, jockey_id=jockeys[1].id, place=3),
        ]
        for entry in race3_entries:
            db.session.add(entry)
        
        db.session.commit()
        print(f"✓ Created 3 races with entries")
        
        print("\n✅ Sample data initialization complete!")
        print("\nYou can now log in and see:")
        print(f"  - {len(hosts)} hosts")
        print(f"  - {len(horses)} horses")
        print(f"  - {len(jockeys)} jockeys")
        print(f"  - 3 races (2 finished, 1 scheduled)")

if __name__ == '__main__':
    init_sample_data()
