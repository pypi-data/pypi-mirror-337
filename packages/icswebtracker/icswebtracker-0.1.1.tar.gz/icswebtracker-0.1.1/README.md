# ICSwebtracker

A simple, lightweight Django app for tracking website visitors without JavaScript.

## Features

- Track page visits with IP address, user agent, and other metadata
- Configurable exclusion rules for paths and IP addresses
- Easy-to-use admin interface for viewing visitor data
- Works with Django's built-in authentication system
- Optimized for low-traffic sites (less than 1,000 visitors per month)
- No JavaScript required - works server-side with Django middleware

## Installation

```bash
pip install icswebtracker
```

## Quick Start

1. Add 'icswebtracker' to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    # ...
    'icswebtracker',
]
```

2. Add the middleware:

```python
MIDDLEWARE = [
    # ...
    'icswebtracker.middleware.TrackMiddleware',
]
```

3. Run migrations:

```bash
python manage.py migrate icswebtracker
```

4. Configure settings (optional):

```python
WEBTRACKER_SETTINGS = {
    'ENABLED': True,
    'IGNORE_PATHS': ['/admin/', '/static/', '/media/'],
    'IGNORE_IPS': ['127.0.0.1'],
    'TRACK_AUTHENTICATED': True,
    'TRACK_ANONYMOUS': True,
    'RESOLVE_COUNTRY': False,
}
```

## Usage

Visit data is available in the Django admin interface. You can also query the data programmatically:

```python
from icswebtracker.models import Visit

# Get all visits
all_visits = Visit.objects.all()

# Get visits to a specific page
page_visits = Visit.objects.filter(path='/some/page/')

# Get visits from a specific country
country_visits = Visit.objects.filter(country='US')
```

## Configuration Options

- `ENABLED`: Enable or disable tracking (default: True)
- `IGNORE_PATHS`: Paths to exclude from tracking (default: ['/admin/', '/static/', '/media/'])
- `IGNORE_IPS`: IP addresses to exclude from tracking (default: [])
- `TRACK_AUTHENTICATED`: Whether to track authenticated users (default: True)
- `TRACK_ANONYMOUS`: Whether to track anonymous users (default: True)
- `RESOLVE_COUNTRY`: Enable IP to country resolution (default: False, requires GeoIP2)

## License

MIT