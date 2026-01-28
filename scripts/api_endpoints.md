# TMDb API Endpoints for Project

## Key Endpoints We'll Use:

### 1. Get Genre List
**Endpoint:** `/genre/movie/list`
**Purpose:** Map genre IDs to genre names
**Data Needed:** genre ID, genre name

### 2. Discover Movies (Main Data Source)
**Endpoint:** `/discover/movie`
**Purpose:** Filter movies by year, genre, budget range
**Parameters:** 
- primary_release_date.gte / .lte (filter by year)
- with_genres (filter by genre ID)
- sort_by (popularity, revenue, etc.)
- page (pagination)

### 3. Movie Details
**Endpoint:** `/movie/{movie_id}`
**Purpose:** Get budget, revenue, runtime for ROI calculation
**Data Needed:** 
- budget
- revenue
- runtime
- genres
- release_date
- production_companies

### 4. Search Movies (Backup)
**Endpoint:** `/search/movie`
**Purpose:** Find specific movies by title
**Use Case:** Validation, filling gaps

## Data We'll Collect:
- Title
- Genre(s) - primary genre
- Budget
- Revenue (theatrical box office)
- Release date
- Runtime
- Production companies
- Popularity score
- Vote average

## Calculated Metrics:
- ROI = ((Revenue - Budget) / Budget) * 100
- Platform (Theatrical vs Streaming-first vs Both)
- Success tier (High/Medium/Low ROI)