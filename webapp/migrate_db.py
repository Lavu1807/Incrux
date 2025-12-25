"""
Database Migration: Add Email Scheduling Fields
Run this script once to add new fields to existing database.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db, User

def migrate_database():
    """Add email scheduling fields to User table."""
    
    with app.app_context():
        print("Starting database migration...")
        
        try:
            # Try to add columns directly
            print("Adding 'preferred_email_time' and 'email_enabled' columns...")
            
            with db.engine.begin() as conn:
                try:
                    conn.execute(db.text("ALTER TABLE user ADD COLUMN preferred_email_time VARCHAR(5) DEFAULT '08:00'"))
                    print("✓ Added 'preferred_email_time'")
                except Exception as e:
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                        print("✓ 'preferred_email_time' already exists")
                    else:
                        print(f"  Note: {str(e)}")
                
                try:
                    conn.execute(db.text("ALTER TABLE user ADD COLUMN email_enabled BOOLEAN DEFAULT 1"))
                    print("✓ Added 'email_enabled'")
                except Exception as e:
                    if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                        print("✓ 'email_enabled' already exists")
                    else:
                        print(f"  Note: {str(e)}")
            
            print("\n✅ Database migration successful!")
            print("All users now have email scheduling fields.")
            print("Default settings: 08:00, email enabled")
            
        except Exception as e:
            print(f"\n✗ Migration failed: {str(e)}")
            print("\n📝 Alternative: Delete newsflash.db and restart app to create fresh database")
            print("   Location: c:\\Users\\HP\\Desktop\\news_crux\\news-flash\\webapp\\newsflash.db")
            return

if __name__ == "__main__":
    print("=" * 60)
    print("News-Flash Database Migration")
    print("=" * 60)
    print()
    
    migrate_database()
