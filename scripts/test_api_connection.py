"""
Test TMDb API Connection
Purpose: Verify API key works and explore available endpoints
"""

import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get API credentials
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = os.getenv('TMDB_BASE_URL')

def test_api_connection():
    """Test basic API connection"""
    
    print("=" * 50)
    print("Testing TMDb API Connection...")
    print("=" * 50)
    
    # Check if API key is loaded
    if not TMDB_API_KEY:
        print("❌ ERROR: API key not found in .env file")
        return False
    
    print(f"✅ API Key loaded: {TMDB_API_KEY[:10]}...")
    print(f"✅ Base URL: {TMDB_BASE_URL}")
    print()
    
    # Test endpoint: Get configuration (doesn't require movie ID)
    url = f"{TMDB_BASE_URL}/configuration"
    params = {
        'api_key': TMDB_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for bad status codes
        
        print("✅ API Connection Successful!")
        print(f"Status Code: {response.status_code}")
        print()
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Connection Failed: {e}")
        return False

def get_sample_movies():
    """Fetch 5 popular movies to test data structure"""
    
    print("=" * 50)
    print("Fetching Sample Movies...")
    print("=" * 50)
    
    # Endpoint: Get popular movies
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'page': 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        movies = data['results'][:5]  # Get first 5 movies
        
        print(f"✅ Successfully retrieved {len(movies)} movies!\n")
        
        # Display sample movies
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
            print(f"   Genre IDs: {movie['genre_ids']}")
            print(f"   Popularity: {movie['popularity']}")
            print(f"   Vote Average: {movie['vote_average']}")
            print()
        
        return movies
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch movies: {e}")
        return None

def get_movie_details(movie_id):
    """Fetch detailed info for a specific movie (including budget & revenue)"""
    
    print("=" * 50)
    print(f"Fetching Detailed Info for Movie ID: {movie_id}")
    print("=" * 50)
    
    # Endpoint: Get movie details
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        movie = response.json()
        
        print(f"✅ Movie Details Retrieved!\n")
        print(f"Title: {movie['title']}")
        print(f"Release Date: {movie.get('release_date', 'N/A')}")
        print(f"Budget: ${movie.get('budget', 0):,}")
        print(f"Revenue: ${movie.get('revenue', 0):,}")
        print(f"Runtime: {movie.get('runtime', 'N/A')} minutes")
        print(f"Genres: {[g['name'] for g in movie.get('genres', [])]}")
        print(f"Production Companies: {[c['name'] for c in movie.get('production_companies', [])][:3]}")
        
        # Calculate ROI if budget > 0
        if movie.get('budget', 0) > 0:
            roi = ((movie.get('revenue', 0) - movie['budget']) / movie['budget']) * 100
            print(f"ROI: {roi:.2f}%")
        
        print()
        return movie
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch movie details: {e}")
        return None

def get_genre_list():
    """Fetch the official list of TMDb genres"""
    
    print("=" * 50)
    print("Fetching Genre List...")
    print("=" * 50)
    
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        genres = data['genres']
        
        print(f"✅ Retrieved {len(genres)} genres!\n")
        
        # Display genres
        for genre in genres:
            print(f"ID {genre['id']}: {genre['name']}")
        
        print()
        return genres
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch genres: {e}")
        return None

def main():
    """Run all API tests"""
    
    # Test 1: Basic connection
    if not test_api_connection():
        print("⚠️  Fix API connection before proceeding")
        return
    
    # Test 2: Get genre list (you'll need this for mapping genre IDs to names)
    genres = get_genre_list()
    
    # Test 3: Fetch popular movies
    movies = get_sample_movies()
    
    # Test 4: Get detailed info for first movie
    if movies:
        first_movie_id = movies[0]['id']
        get_movie_details(first_movie_id)
    
    print("=" * 50)
    print("✅ All API Tests Complete!")
    print("=" * 50)
    print("\nNext Steps:")
    print("1. Review the data structure above")
    print("2. Document which endpoints you'll use for your project")
    print("3. Start building your main data collection script")

if __name__ == "__main__":
    main()