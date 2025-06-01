# STL Collection Manager

A comprehensive Django web application for managing 3D STL file collections with modern UI, tagging system, and advanced search capabilities.

## Features

### Core Functionality
- **Image Upload System**: Upload and manage STL file images with metadata
- **Tag Management**: Create, edit, and organize tags for categorization
- **Advanced Search**: Filter by publisher, range, tags, and full-text search
- **Collection Gallery**: Browse images with pagination and responsive design
- **Image Details**: Detailed view with related images and metadata

### User Interface
- **Bootstrap 5**: Modern, responsive design with dark/light theme support
- **Bootstrap Icons**: Comprehensive icon set throughout the interface
- **Select2 Integration**: Enhanced multi-select dropdowns for tags
- **Mobile-Responsive**: Optimized for all device sizes
- **Admin Interface**: Django Unfold admin theme for backend management

### Technical Features
- **Django 5.2**: Latest Django framework with SQLite database
- **File Management**: Proper media handling and organized storage
- **Permission System**: Staff-only access for administrative functions
- **Form Validation**: Client and server-side validation with visual feedback
- **Pagination**: Efficient handling of large collections

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd stl-collection-v2
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Web Interface: http://127.0.0.1:8000/
   - Admin Interface: http://127.0.0.1:8000/admin/

## Usage

### Getting Started

1. **Login** as an admin user to access upload and management features
2. **Create Tags** in the tag management section for organizing your collection
3. **Upload Images** using the upload form with metadata and tag assignment
4. **Browse Collection** using the gallery with search and filter options
5. **Manage Content** through the admin interface or web forms

### Navigation

- **Collection**: Browse and search your image gallery
- **Upload**: Add new images (admin only)
- **Assign Tags**: Bulk tag assignment (admin only, coming soon)
- **Edit Tags**: Manage tag creation, editing, and deletion (admin only)
- **Ranges**: Product range management (admin only, coming soon)

### Search and Filtering

- **Text Search**: Search across names, publishers, ranges, and tags
- **Publisher Filter**: Filter by specific publishers
- **Range Filter**: Filter by product ranges
- **Tag Filter**: Multi-select tag filtering
- **Combined Filters**: Use multiple filters simultaneously

## Project Structure

```
stl-collection-v2/
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── bulk_operations.ps1         # PowerShell bulk import script
├── db.sqlite3                 # SQLite database (created after migration)
├── stl_collection/            # Main Django project
│   ├── settings.py            # Project settings
│   ├── urls.py                # URL routing
│   └── views.py               # Landing page view
├── image_upload/              # Image upload and management app
├── collection/                # Gallery and search functionality
├── tags/                      # Tag management system
├── ranges/                    # Range management (placeholder)
├── tag_assign/                # Bulk tag assignment (placeholder)
├── image_details/             # Detailed image views
├── templates/                 # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── landing_page.html      # Homepage
│   └── [app_templates]/       # App-specific templates
├── static/                    # Static files (CSS, JS, images)
└── media/                     # Uploaded files
    └── uploaded_images/       # Image uploads directory
```

## Apps Overview

### image_upload
- **Models**: Image model with fields for metadata and file storage
- **Forms**: Upload and edit forms with Bootstrap styling
- **Views**: Staff-only upload functionality
- **Admin**: Django admin integration with Unfold theme

### collection
- **Views**: Gallery with pagination, search, and filtering
- **Templates**: Responsive card-based layout
- **Features**: Advanced filtering and image editing

### tags
- **Models**: Tag model with many-to-many relationship to images
- **Views**: CRUD operations for tag management
- **Admin**: Tag administration interface

### image_details
- **Views**: Detailed image view with related images
- **Features**: Full metadata display and navigation

## Database Models

### Image Model
- `image`: ImageField for file uploads
- `name`: Image name/title
- `publisher`: Publisher information
- `range`: Product range
- `folder_location`: Original file location
- `upload_date`: Automatic timestamp
- `notes`: Optional description
- `tags`: Many-to-many relationship with Tag model

### Tag Model
- `name`: Unique tag name
- `created_at`: Creation timestamp

## Bulk Operations

The included PowerShell script (`bulk_operations.ps1`) provides:

### Features
- **Directory scanning**: Recursive image file discovery
- **Metadata extraction**: Automatic publisher/range detection from folder structure
- **Database integration**: Direct SQLite database operations
- **File copying**: Organized media directory management
- **Statistics reporting**: Database statistics and summaries

### Usage
```powershell
# View database statistics
.\bulk_operations.ps1 -Action List

# Bulk import from directory
.\bulk_operations.ps1 -Action Import -SourceDirectory "C:\MySTLFiles"
```

### Prerequisites
```powershell
Install-Module -Name PSSQLite -Scope CurrentUser
```

## Configuration

### Django Settings
- **Database**: SQLite (configured in `settings.py`)
- **Media Files**: Stored in `media/uploaded_images/`
- **Static Files**: Served from `static/` directory
- **Admin Theme**: Django Unfold for modern admin interface

### Security
- **CSRF Protection**: Enabled on all forms
- **Staff Permissions**: Administrative functions restricted to staff users
- **File Validation**: Image file type validation on uploads

## Development

### Adding New Features
1. Create new Django app: `python manage.py startapp app_name`
2. Add to `INSTALLED_APPS` in `settings.py`
3. Create models, views, and templates
4. Update URL routing
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Customization
- **Styling**: Modify Bootstrap variables in templates
- **Pagination**: Adjust page size in `collection/views.py`
- **File Types**: Update accepted file types in forms
- **Admin Interface**: Customize Unfold settings in `settings.py`

## Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py migrate --fake-initial
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Permission Denied on Uploads**
   - Check media directory permissions
   - Ensure proper file path configuration

4. **Database Locked**
   - Stop Django development server
   - Close any database connections
   - Restart server

### Development Tips
- Use `python manage.py shell` for database operations
- Enable Django debug mode for detailed error messages
- Check Django logs for troubleshooting
- Use browser developer tools for frontend issues

## License

This project is intended for personal/internal use. Modify and distribute according to your organization's policies.

## Support

For issues or questions:
1. Check Django documentation: https://docs.djangoproject.com/
2. Review Bootstrap documentation: https://getbootstrap.com/docs/
3. Consult Django Unfold documentation for admin customization
