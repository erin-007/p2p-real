# P2P Tutoring Scheduler

## Overview

P2P Tutoring Scheduler is a peer-to-peer tutoring platform built with Django that connects students seeking help (tutees) with those willing to teach (tutors). The application enables users to switch between two distinct roles—tutor and tutee—each with its own dashboard and feature set. Users can browse available tutors, book tutoring sessions, manage their schedules, and maintain profiles for both roles.

The platform emphasizes flexible scheduling, peer-to-peer learning, and easy session management through a clean, responsive web interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- HTML5 with Django Template Language
- Tailwind CSS (via CDN) for styling
- Alpine.js for minimal client-side interactivity
- Font Awesome for icons

**Design Pattern:**
- Template inheritance using a `base.html` parent template
- All page-specific templates extend the base and override the `{% block content %}` section
- Responsive-first design approach using Tailwind's utility classes
- Component-based UI elements (cards, forms, modals) for consistency

**Key Design Decisions:**
- **Problem:** Need for consistent navigation and styling across all pages
- **Solution:** Django template inheritance with a shared base template containing navbar, footer, and CDN includes
- **Rationale:** Reduces code duplication and ensures UI consistency while maintaining Django's server-side rendering benefits

- **Problem:** Interactive features without heavy JavaScript frameworks
- **Solution:** Alpine.js for lightweight reactivity (tabs, modals, role switching)
- **Rationale:** Keeps the frontend minimal while providing necessary interactivity for better UX

### Backend Architecture

**Framework:** Django (Python web framework)

**Application Structure:**
- Monolithic Django project named `p2p_tutoring`
- Views defined in `p2p_tutoring/views.py`
- URL routing in `p2p_tutoring/urls.py`
- Settings in `p2p_tutoring/settings.py`

**Key Components:**
- Django's built-in authentication system for user management
- Session-based state management
- Django Admin interface for administrative tasks
- Template rendering with context data passed from views

**View Layer:**
- Function-based views for simplicity
- Sample/mock data currently hardcoded in views for demonstration
- Context dictionaries passed to templates for rendering dynamic content

**Key Design Decisions:**
- **Problem:** Dual-role system where users can be both tutors and tutees
- **Solution:** Role selection through UI with separate dashboards and views for each role
- **Rationale:** Provides clear separation of concerns and distinct user experiences based on current role

- **Problem:** Need for rapid prototyping and demonstration
- **Solution:** Currently using hardcoded sample data in views instead of database models
- **Rationale:** Allows frontend development to proceed without backend implementation, but will need to be replaced with proper models and database queries

### Database & Data Layer

**Current State:**
- No database models defined yet
- No ORM queries implemented
- Using Django's default SQLite database (implied by lack of custom database configuration)
- Sample data hardcoded in view functions

**Expected Implementation:**
- User model (likely extending Django's AbstractUser)
- Tutor profile model with subjects, ratings, availability
- Tutee profile model
- Session/Booking model with relationships to users
- Potentially a Subject model for categorization

**Key Design Decisions:**
- **Problem:** Users need to maintain separate profiles for tutor and tutee roles
- **Solution:** Likely to implement separate profile models linked to the User model
- **Rationale:** Allows users to have different information, subjects, and settings for each role

### Authentication & Authorization

**Current Implementation:**
- Django's built-in authentication middleware enabled
- Session management configured
- CSRF protection enabled for form submissions
- Login and registration views created but not fully implemented

**Security Features:**
- CSRF tokens required on all forms
- Session-based authentication
- Secret key configuration via environment variable (SESSION_SECRET)

**Key Design Decisions:**
- **Problem:** Need for secure user authentication
- **Solution:** Leveraging Django's battle-tested authentication system
- **Rationale:** Avoids reinventing the wheel and provides robust, secure authentication out of the box

## External Dependencies

### Frontend Dependencies (CDN-hosted)

1. **Tailwind CSS** (cdn.tailwindcss.com)
   - Purpose: Utility-first CSS framework for styling
   - Used for: All UI components, responsive design, and layout

2. **Font Awesome** (cdnjs.cloudflare.com)
   - Purpose: Icon library
   - Used for: Navigation icons, feature indicators, and visual elements

3. **Alpine.js** (cdn.jsdelivr.net)
   - Purpose: Lightweight JavaScript framework for reactivity
   - Used for: Tabs, modals, dropdowns, and dynamic UI interactions

### Backend Dependencies

1. **Django** (Python package)
   - Purpose: Web framework
   - Version: Not specified in repository
   - Used for: Entire backend architecture, routing, templates, authentication

### Development & Deployment

**Environment Variables:**
- `SESSION_SECRET`: Django secret key (defaults to insecure dev key if not set)
- `DJANGO_SETTINGS_MODULE`: Points to `p2p_tutoring.settings`

**Configuration:**
- Debug mode: Enabled (DEBUG = True)
- Allowed hosts: All hosts allowed (not production-ready)
- Static files: Configured but directory not present in repository
- Templates: Located in `/templates` directory

**Missing Production Configuration:**
- No production-ready secret key management
- No database configuration for production
- No static file serving setup for production
- No environment-specific settings separation