"""
Add Streaming Platform Data to Theatrical Movies
Purpose: Enrich theatrical data with streaming availability from TMDb API
Author: Alexandra Lugo
Date: January 2026
"""

import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time
from pathlib import Path
import json

#load environment variables
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = os.getenv('TMDB_BASE_URL')

#API rate limiting
REQUEST_DELAY = 0.26


class StreamingEnricher:
    """Add streaming platform data to theatrical movies"""
    
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        
    def get_watch_providers(self, movie_id):
        """
        Get streaming platform availability for a movie
        Focus on US market (region=US)
        """
        url = f"{self.base_url}/movie/{movie_id}/watch/providers"
        params = {'api_key': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            time.sleep(REQUEST_DELAY)
            
            data = response.json()
            
            #get US providers (you can change to other regions if needed)
            us_providers = data.get('results', {}).get('US', {})
            
            return us_providers
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error fetching providers for movie {movie_id}: {e}")
            return {}
    
    def parse_providers(self, providers_data):
        """
        Parse provider data into usable categories
        """
        #initialize return dictionary
        parsed = {
            'available_on_streaming': False,
            'streaming_platforms': [],
            'available_to_rent': False,
            'available_to_buy': False,
            'on_netflix': False,
            'on_prime': False,
            'on_disney': False,
            'on_hulu': False,
            'on_hbo': False,
            'total_platforms': 0
        }
        
        #check flatrate (subscription streaming)
        if 'flatrate' in providers_data:
            parsed['available_on_streaming'] = True
            platforms = [p['provider_name'] for p in providers_data['flatrate']]
            parsed['streaming_platforms'] = platforms
            parsed['total_platforms'] = len(platforms)
            
            #check specific platforms
            parsed['on_netflix'] = any('Netflix' in p for p in platforms)
            parsed['on_prime'] = any('Prime' in p or 'Amazon' in p for p in platforms)
            parsed['on_disney'] = any('Disney' in p for p in platforms)
            parsed['on_hulu'] = any('Hulu' in p for p in platforms)
            parsed['on_hbo'] = any('HBO' in p or 'Max' in p for p in platforms)
        
        #check rent/buy options
        parsed['available_to_rent'] = 'rent' in providers_data
        parsed['available_to_buy'] = 'buy' in providers_data
        
        return parsed
    
    def categorize_release_strategy(self, row):
        """
        Categorize movie's release strategy based on revenue and streaming availability
        """
        revenue = row.get('revenue', 0)
        budget = row.get('budget', 0)
        on_streaming = row.get('available_on_streaming', False)
        
        #high theatrical revenue (>$50M) → Theatrical-first
        if revenue > 50_000_000:
            if on_streaming:
                return 'Theatrical → Streaming'
            else:
                return 'Theatrical Only'
        
        #low theatrical revenue (<$10M) but has budget → Likely streaming-first
        elif revenue < 10_000_000 and budget > 0:
            if on_streaming:
                return 'Streaming-First'
            else:
                return 'Limited Theatrical'
        
        #medium revenue → Mixed strategy
        else:
            if on_streaming:
                return 'Theatrical → Streaming'
            else:
                return 'Theatrical Only'
    
    def enrich_dataset(self, df):
        """
        Add streaming data to entire dataset
        """
        print("="*60)
        print("Adding Streaming Platform Data")
        print("="*60)
        print(f"Processing {len(df)} movies...\n")
        
        #initialize new columns
        streaming_cols = [
            'available_on_streaming',
            'streaming_platforms', 
            'available_to_rent',
            'available_to_buy',
            'on_netflix',
            'on_prime',
            'on_disney',
            'on_hulu',
            'on_hbo',
            'total_platforms',
            'release_strategy'
        ]
        
        for col in streaming_cols[:-1]:  #all except release_strategy
            df[col] = None
        
        #process each movie
        for idx, row in df.iterrows():
            movie_id = row['movie_id']
            
            #progress indicator
            if (idx + 1) % 50 == 0:
                print(f"  Processed {idx + 1}/{len(df)} movies...")
            
            #get provider data
            providers = self.get_watch_providers(movie_id)
            
            #parse providers
            parsed = self.parse_providers(providers)
            
            #update dataframe
            for key, value in parsed.items():
                df.at[idx, key] = value
        
        #add release strategy categorization
        df['release_strategy'] = df.apply(self.categorize_release_strategy, axis=1)
        
        print(f"\n✅ Streaming data added to all {len(df)} movies!")
        
        return df


def main():
    """Main workflow"""
    
    print("="*60)
    print("Theatrical + Streaming Data Integration")
    print("="*60)
    
    #load theatrical data
    theatrical_file = project_root / 'data' / 'raw' / 'theatrical_data_raw.csv'
    
    if not theatrical_file.exists():
        print(f"❌ Error: {theatrical_file} not found!")
        print("Please run collect_theatrical_data.py first.")
        return
    
    print(f"\n📂 Loading theatrical data from: {theatrical_file}")
    df = pd.read_csv(theatrical_file)
    print(f"✅ Loaded {len(df)} theatrical movies")
    
    #initialize enricher
    enricher = StreamingEnricher(TMDB_API_KEY, TMDB_BASE_URL)
    
    #add streaming data
    start_time = time.time()
    df_enriched = enricher.enrich_dataset(df)
    elapsed_time = time.time() - start_time
    
    #summary statistics
    print(f"\n{'='*60}")
    print("Streaming Data Summary")
    print(f"{'='*60}")
    
    print(f"\nMovies available on streaming: {df_enriched['available_on_streaming'].sum()}")
    print(f"Movies NOT on streaming: {(~df_enriched['available_on_streaming']).sum()}")
    
    print(f"\nPlatform breakdown:")
    print(f"  Netflix: {df_enriched['on_netflix'].sum()}")
    print(f"  Prime Video: {df_enriched['on_prime'].sum()}")
    print(f"  Disney+: {df_enriched['on_disney'].sum()}")
    print(f"  Hulu: {df_enriched['on_hulu'].sum()}")
    print(f"  HBO Max: {df_enriched['on_hbo'].sum()}")
    
    print(f"\nRelease strategy breakdown:")
    print(df_enriched['release_strategy'].value_counts())
    
    #show sample of enriched data
    print(f"\n{'='*60}")
    print("Sample Enriched Data")
    print(f"{'='*60}")
    sample_cols = ['title', 'release_year', 'revenue', 'available_on_streaming', 
                   'on_netflix', 'on_prime', 'release_strategy']
    print(df_enriched[sample_cols].head(10).to_string())
    
    #save enriched dataset
    output_file = project_root / 'data' / 'raw' / 'theatrical_streaming_combined.csv'
    df_enriched.to_csv(output_file, index=False)
    
    print(f"\n✅ Enriched data saved to: {output_file}")
    print(f"⏱️  Processing time: {elapsed_time/60:.1f} minutes")
    
    #create a summary for interviews
    print(f"\n{'='*60}")
    print("🎤 KEY INSIGHTS FOR INTERVIEWS")
    print(f"{'='*60}")
    
    #calculate average ROI by release strategy
    roi_by_strategy = df_enriched.groupby('release_strategy')['roi'].agg(['mean', 'count'])
    print("\nAverage ROI by Release Strategy:")
    print(roi_by_strategy)
    
    #most common genres on each platform
    print("\n📊 Ready for genre-by-platform analysis!")
    print("Next step: Clean this data and build your dashboard (Day 5)")


if __name__ == "__main__":
    main()