# Bitmore Application Database Setup

## Database Configuration

The application has been configured to use a new PostgreSQL database to avoid conflicts with other applications.

### Current Database Configuration

- **Database Name**: `newbitmoredb` (changed from `bitmoredb`)
- **Database User**: `bitmoreuser`
- **Database Password**: `bitmorepass`
- **Host**: `localhost`
- **Port**: `5432`

## What Changed

1. **Database Name Updated**: Changed from `bitmoredb` to `newbitmoredb` in `backend/settings.py`
2. **New Database Created**: Created `newbitmoredb` in PostgreSQL
3. **Migrations Applied**: All Django migrations have been applied to the new database
4. **Superuser Created**: A superuser account has been created for admin access

## Files Modified

- `backend/backend/settings.py` - Updated DATABASES configuration

## Files Added

- `backend/db_setup.py` - Database management script
- `README_DATABASE.md` - This documentation file

## Quick Start

1. **Start the Django server**:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Access the application**:
   - Frontend: Your React application should work as before
   - Admin panel: http://127.0.0.1:8000/admin/
   - API endpoints: http://127.0.0.1:8000/api/

## Database Management

### To reset the database:
```bash
# Drop and recreate the database
psql -U postgres -c "DROP DATABASE IF EXISTS newbitmoredb;"
psql -U postgres -c "CREATE DATABASE newbitmoredb OWNER bitmoreuser;"

# Reapply migrations
python manage.py migrate

# Create a new superuser
python manage.py createsuperuser
```

### To backup the database:
```bash
pg_dump -U bitmoreuser -h localhost newbitmoredb > backup.sql
```

### To restore from backup:
```bash
psql -U bitmoreuser -h localhost newbitmoredb < backup.sql
```

## Troubleshooting

1. **Connection Issues**: Ensure PostgreSQL is running and the user `bitmoreuser` exists
2. **Permission Issues**: Make sure `bitmoreuser` has proper permissions on `newbitmoredb`
3. **Migration Issues**: If migrations fail, check the database connection in settings.py

## Environment Variables (Optional)

For better security, consider moving database credentials to environment variables:

```python
# In settings.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'newbitmoredb'),
        'USER': os.getenv('DB_USER', 'bitmoreuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'bitmorepass'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

Then create a `.env` file in the backend directory:
```
DB_NAME=newbitmoredb
DB_USER=bitmoreuser
DB_PASSWORD=bitmorepass
DB_HOST=localhost
DB_PORT=5432
```

## Next Steps

1. Test all application functionality with the new database
2. Update any deployment scripts to use the new database name
3. Consider implementing database backups for production use
4. Update your team about the database change
