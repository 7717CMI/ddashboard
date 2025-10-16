#!/usr/bin/env python3
"""
Script to create a comprehensive sample dataset for the Logistics Dashboard
"""

import json
import random
from datetime import datetime, timedelta

def generate_sample_data(num_records=100):
    """Generate comprehensive sample logistics data"""
    
    # Sample cities and states with coordinates
    cities = [
        {"city": "Chicago", "state": "IL", "lat": 41.8781, "lon": -87.6298},
        {"city": "New York", "state": "NY", "lat": 40.7128, "lon": -74.0060},
        {"city": "Los Angeles", "state": "CA", "lat": 34.0522, "lon": -118.2437},
        {"city": "Houston", "state": "TX", "lat": 29.7604, "lon": -95.3698},
        {"city": "Phoenix", "state": "AZ", "lat": 33.4484, "lon": -112.0740},
        {"city": "Philadelphia", "state": "PA", "lat": 39.9526, "lon": -75.1652},
        {"city": "San Antonio", "state": "TX", "lat": 29.4241, "lon": -98.4936},
        {"city": "San Diego", "state": "CA", "lat": 32.7157, "lon": -117.1611},
        {"city": "Dallas", "state": "TX", "lat": 32.7767, "lon": -96.7970},
        {"city": "San Jose", "state": "CA", "lat": 37.3382, "lon": -121.8863},
        {"city": "Austin", "state": "TX", "lat": 30.2672, "lon": -97.7431},
        {"city": "Jacksonville", "state": "FL", "lat": 30.3322, "lon": -81.6557},
        {"city": "Fort Worth", "state": "TX", "lat": 32.7555, "lon": -97.3308},
        {"city": "Columbus", "state": "OH", "lat": 39.9612, "lon": -82.9988},
        {"city": "Charlotte", "state": "NC", "lat": 35.2271, "lon": -80.8431},
        {"city": "San Francisco", "state": "CA", "lat": 37.7749, "lon": -122.4194},
        {"city": "Indianapolis", "state": "IN", "lat": 39.7684, "lon": -86.1581},
        {"city": "Seattle", "state": "WA", "lat": 47.6062, "lon": -122.3321},
        {"city": "Denver", "state": "CO", "lat": 39.7392, "lon": -104.9903},
        {"city": "Washington", "state": "DC", "lat": 38.9072, "lon": -77.0369}
    ]
    
    equipment_types = ["Dry Van", "Reefer", "Flatbed", "Power Only"]
    companies = [
        "Koola Logistics LLC",
        "Surge Transportation", 
        "JB Hunt",
        "Swift Transportation",
        "Schneider National",
        "Werner Enterprises",
        "Knight Transportation",
        "Prime Inc",
        "Covenant Transport",
        "USA Truck"
    ]
    
    load_postings = []
    
    # Base timestamp (recent date)
    base_timestamp = int(datetime.now().timestamp() * 1000)
    
    for i in range(num_records):
        # Random origin and destination
        origin = random.choice(cities)
        destination = random.choice(cities)
        
        # Ensure origin != destination
        while destination == origin:
            destination = random.choice(cities)
        
        # Calculate distance (rough approximation)
        lat_diff = abs(origin["lat"] - destination["lat"])
        lon_diff = abs(origin["lon"] - destination["lon"])
        distance = int((lat_diff + lon_diff) * 100)  # Rough miles
        
        # Generate realistic rates based on distance
        base_rate = distance * random.uniform(1.5, 3.0)  # $1.5-3.0 per mile
        rate_cents = int(base_rate * 100)
        rate_per_mile_cents = int(rate_cents / distance) if distance > 0 else 0
        
        # Random timestamps
        posted_timestamp = base_timestamp - random.randint(0, 7*24*60*60*1000)  # Last 7 days
        pickup_timestamp = posted_timestamp + random.randint(1*60*60*1000, 3*24*60*60*1000)  # 1 hour to 3 days later
        
        load_posting = {
            "id": 568188000 + i,
            "referenceNumber": f"REF{100000 + i}",
            "trackingNumber": f"TRK{100000 + i}",
            "postedTimestamp": posted_timestamp,
            "pickupTimestamp": pickup_timestamp,
            "dropoffTimestamp": None,
            "comments": f"Load {i+1} - Standard delivery",
            "rateCents": rate_cents,
            "rateCentsPerMile": rate_per_mile_cents,
            "originKey": random.randint(-2000000000, 2000000000),
            "originCity": origin["city"],
            "originState": origin["state"],
            "originLatitude": origin["lat"],
            "originLongitude": origin["lon"],
            "destinationKey": random.randint(-2000000000, 2000000000),
            "destinationCity": destination["city"],
            "destinationState": destination["state"],
            "destinationLatitude": destination["lat"],
            "destinationLongitude": destination["lon"],
            "distanceMiles": distance,
            "originDeadhead": None,
            "destinationDeadhead": None,
            "equipmentType": random.choice(equipment_types),
            "weight": random.randint(10000, 45000),
            "length": random.choice([48, 53]),
            "dotNumber": f"{random.randint(1000000, 9999999)}",
            "mcNumber": f"{random.randint(100000, 999999)}",
            "companyName": random.choice(companies),
            "companyEmail": f"ops@{random.choice(companies).lower().replace(' ', '').replace('.', '')}.com",
            "companyPhone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "contactName": None,
            "contactEmail": None,
            "contactPhone": f"{random.randint(2000000000, 9999999999)}",
            "value": random.uniform(0.05, 0.5),
            "viewed": random.choice([True, False]),
            "credit": random.choice([True, False])
        }
        
        load_postings.append(load_posting)
    
    return {
        "load_postings": load_postings,
        "timestamp": base_timestamp,
        "total": len(load_postings)
    }

if __name__ == "__main__":
    # Generate 100 sample records
    sample_data = generate_sample_data(100)
    
    # Save to file
    with open('sample_data.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"Generated {len(sample_data['load_postings'])} sample load postings")
    print("Saved to sample_data.json")
    
    # Print summary
    companies = set(post['companyName'] for post in sample_data['load_postings'])
    equipment = set(post['equipmentType'] for post in sample_data['load_postings'])
    
    print(f"\nSummary:")
    print(f"- Companies: {len(companies)}")
    print(f"- Equipment types: {len(equipment)}")
    print(f"- Rate range: ${min(post['rateCents'] for post in sample_data['load_postings'])/100:.0f} - ${max(post['rateCents'] for post in sample_data['load_postings'])/100:.0f}")
    print(f"- Distance range: {min(post['distanceMiles'] for post in sample_data['load_postings'])} - {max(post['distanceMiles'] for post in sample_data['load_postings'])} miles")
