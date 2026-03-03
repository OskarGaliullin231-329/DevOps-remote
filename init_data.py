"""
Sample data initialization script - OPTIONAL
This script populates the database with sample data for testing.
Run with: python init_data.py
"""

from app import app, db
from models import Owner, Horse, Jockey, Race, RaceEntry
from datetime import datetime, timedelta

def init_sample_data():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Check if data already exists
        if Owner.query.first() is not None:
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Initializing sample data...")
        
        # Create owners
        owners = [
            Owner(name="John Smith"),
            Owner(name="Sarah Johnson"),
            Owner(name="Michael Brown"),
            Owner(name="Emma Wilson"),
        ]
        for owner in owners:
            db.session.add(owner)
        db.session.commit()
        print(f"✓ Created {len(owners)} owners")
        
        # Create horses
        horses_data = [
            ("Thunder", 8.5, owners[0]),
            ("Lightning", 7.8, owners[0]),
            ("Midnight", 9.2, owners[1]),
            ("Sunset", 7.5, owners[1]),
            ("Storm", 8.9, owners[2]),
            ("Golden Dream", 8.3, owners[2]),
            ("Silver Moon", 8.1, owners[3]),
            ("Wind Dance", 7.9, owners[3]),
        ]
        
        horses = []
        for name, rating, owner in horses_data:
            horse = Horse(name=name, rating=rating, owner=owner)
            horses.append(horse)
            db.session.add(horse)
        db.session.commit()
        print(f"✓ Created {len(horses)} horses")
        
        # Create jockeys
        jockeys_data = [
            ("James Lewis", 8.7),
            ("Maria Garcia", 9.1),
            ("David Wilson", 8.4),
            ("Anna Martinez", 8.8),
            ("Robert Taylor", 7.9),
            ("Catherine Anderson", 8.6),
        ]
        
        jockeys = []
        for name, rating in jockeys_data:
            jockey = Jockey(name=name, rating=rating)
            jockeys.append(jockey)
            db.session.add(jockey)
        db.session.commit()
        print(f"✓ Created {len(jockeys)} jockeys")
        
        # Create races with entries
        base_date = datetime.now() - timedelta(days=10)
        
        # Race 1 - Finished
        race1 = Race(date=base_date)
        db.session.add(race1)
        db.session.flush()
        
        race1_entries = [
            RaceEntry(race=race1, horse=horses[0], jockey=jockeys[0], place=1),
            RaceEntry(race=race1, horse=horses[1], jockey=jockeys[1], place=2),
            RaceEntry(race=race1, horse=horses[2], jockey=jockeys[2], place=3),
            RaceEntry(race=race1, horse=horses[3], jockey=jockeys[3], place=4),
        ]
        for entry in race1_entries:
            db.session.add(entry)
        
        # Race 2 - Finished
        race2 = Race(date=base_date + timedelta(days=2))
        db.session.add(race2)
        db.session.flush()
        
        race2_entries = [
            RaceEntry(race=race2, horse=horses[4], jockey=jockeys[4], place=1),
            RaceEntry(race=race2, horse=horses[5], jockey=jockeys[5], place=2),
            RaceEntry(race=race2, horse=horses[6], jockey=jockeys[0], place=3),
            RaceEntry(race=race2, horse=horses[7], jockey=jockeys[1], place=4),
        ]
        for entry in race2_entries:
            db.session.add(entry)
        
        # Race 3 - Scheduled (no results)
        race3 = Race(date=datetime.now() + timedelta(days=5))
        db.session.add(race3)
        db.session.flush()
        
        race3_entries = [
            RaceEntry(race=race3, horse=horses[0], jockey=jockeys[2], place=None),
            RaceEntry(race=race3, horse=horses[3], jockey=jockeys[4], place=None),
            RaceEntry(race=race3, horse=horses[5], jockey=jockeys[1], place=None),
        ]
        for entry in race3_entries:
            db.session.add(entry)
        
        db.session.commit()
        print(f"✓ Created 3 races with entries")
        
        print("\n✅ Sample data initialization complete!")
        print("\nYou can now log in and see:")
        print(f"  - {len(owners)} owners")
        print(f"  - {len(horses)} horses")
        print(f"  - {len(jockeys)} jockeys")
        print(f"  - 3 races (2 finished, 1 scheduled)")

if __name__ == '__main__':
    init_sample_data()
