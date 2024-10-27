# Djangify Portfolio & Blog

A modern full-stack web application built with Django and Next.js, showcasing portfolio projects and blog content.

## Tech Stack

### Backend
- Python 3.11.10
- Django with Django REST Framework
- PostgreSQL 14.13
- Poetry 1.8.4 for dependency management

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- Shadcn/ui components

### Development Tools
- Docker 27.3.1
- Node.js 20.18.0
- Yarn 1.22.22

## Project Structure

```
djangify/
├── djangify_backend/      # Django REST API
│   ├── apps/
│   │   ├── blog/         # Blog functionality
│   │   ├── portfolio/    # Portfolio projects
│   │   └── core/         # Shared functionality
│   └── config/           # Project configuration
└── djangify_frontend/    # Next.js frontend
    ├── src/
    │   ├── app/         # Next.js app router
    │   ├── components/  # React components
    │   └── lib/         # Utility functions
    └── public/          # Static assets
```

## Prerequisites

- Python 3.11.10
- Node.js 20.18.0
- PostgreSQL 14.13
- Poetry 1.8.4
- Docker 27.3.1

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/todiane/djangify.git
cd djangify
```

2. Backend Setup
```bash
# Install dependencies with Poetry
cd djangify_backend
poetry install

# Set up environment variables
cp .env.example .env

# Run migrations
poetry run python manage.py migrate
```

3. Frontend Setup
```bash
# Navigate to frontend directory
cd djangify_frontend

# Install dependencies
yarn install

# Start development server
yarn dev
```

4. Database Setup
```bash
# PostgreSQL Details
Database Name: djangify
User: djangify_user
Port: 5434
```

## Development

To start the development servers:

```bash
# Backend
cd djangify_backend
poetry run python manage.py runserver

# Frontend (in a new terminal)
cd djangify_frontend
yarn dev
```

## Features

- Dynamic portfolio project showcase
- Blog with categories and tags
- SEO optimization
- Responsive design
- Dark mode support
- Image optimization
- Admin dashboard

## Contributing

1. Create a branch
```bash
git checkout -b feature/feature-name
```

2. Make your changes and commit
```bash
git commit -m "Description of changes"
```

3. Push to the branch
```bash
git push origin feature/feature-name
```

4. Open a Pull Request



## Contact

Diane @ djangify.com
