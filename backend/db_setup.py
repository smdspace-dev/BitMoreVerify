#!/usr/bin/env python3
"""
Database setup script for Bitmore application
This script helps manage the PostgreSQL database for the Bitmore application.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}")
        print(f"Error: {e.stderr}")
        return False

def create_database():
    """Create the newbitmoredb database."""
    print("=== Creating New Database ===")
    
    # Check if PostgreSQL is running
    print("Checking PostgreSQL connection...")
    
    # Create database
    create_db_cmd = 'psql -U postgres -c "CREATE DATABASE newbitmoredb OWNER bitmoreuser;"'
    if run_command(create_db_cmd, "Creating newbitmoredb database"):
        print("✓ Database 'newbitmoredb' created successfully")
    else:
        print("Database might already exist or there was an error")

def setup_django():
    """Set up Django migrations and superuser."""
    print("\n=== Setting up Django ===")
    
    # Make migrations
    run_command("python manage.py makemigrations", "Creating migrations")
    
    # Apply migrations
    run_command("python manage.py migrate", "Applying migrations")
    
    print("\n=== Database setup completed! ===")
    print("Your application is now using the new database: newbitmoredb")
    print("\nTo create a superuser, run:")
    print("python manage.py createsuperuser")
    print("\nTo start the server, run:")
    print("python manage.py runserver")

def main():
    """Main function to set up the database."""
    print("Bitmore Database Setup Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("Error: This script should be run from the Django backend directory")
        print("Please navigate to the backend directory first")
        sys.exit(1)
    
    choice = input("\nWhat would you like to do?\n1. Create new database\n2. Setup Django migrations\n3. Both\nEnter choice (1/2/3): ")
    
    if choice == "1":
        create_database()
    elif choice == "2":
        setup_django()
    elif choice == "3":
        create_database()
        setup_django()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
