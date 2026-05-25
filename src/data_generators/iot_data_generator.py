"""
IoT Sensor Data Generator
Generates realistic sensor data with REAL-WORLD ISSUES:
- Missing values
- Wrong data types
- Outliers
- Duplicates
- Late arrivals
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from faker import Faker

fake = Faker()


class IoTDataGenerator:
    """Generate realistic IoT sensor data with quality issues"""
    
    def __init__(self, num_equipment=100, seed=42):
        """
        Args:
            num_equipment: Number of equipment/machines to simulate
            seed: Random seed for reproducibility
        """
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
        
        self.num_equipment = num_equipment
        self.equipment_ids = [f"EQ-{str(i).zfill(4)}" for i in range(1, num_equipment + 1)]
        self.sensor_types = ['temperature', 'vibration', 'pressure', 'power_consumption']
        
        # Equipment metadata
        self.equipment_types = ['CNC_MACHINE', 'ROBOTIC_ARM', 'CONVEYOR_BELT', 
                               'HYDRAULIC_PRESS', 'ASSEMBLY_ROBOT']
        self.factories = ['Factory_North', 'Factory_South', 'Factory_East', 'Factory_West']
        self.production_lines = ['Line_A', 'Line_B', 'Line_C', 'Line_D']
        
    def generate_equipment_metadata(self):
        """Generate equipment master data"""
        equipment_data = []
        
        for eq_id in self.equipment_ids:
            equipment_data.append({
                'equipment_id': eq_id,
                'equipment_name': f"{random.choice(self.equipment_types)} {eq_id}",
                'equipment_type': random.choice(self.equipment_types),
                'manufacturer': fake.company(),
                'model': f"Model-{random.randint(1000, 9999)}",
                'serial_number': fake.bothify('SN-########'),
                'install_date': fake.date_between(start_date='-5y', end_date='-1y'),
                'factory_location': random.choice(self.factories),
                'production_line': random.choice(self.production_lines),
                'status': random.choice(['ACTIVE', 'ACTIVE', 'ACTIVE', 'MAINTENANCE']),  # 75% active
                'criticality': random.choice(['HIGH', 'MEDIUM', 'LOW']),
                'last_maintenance_date': fake.date_between(start_date='-90d', end_date='today'),
            })
        
        return pd.DataFrame(equipment_data)
    
    def generate_sensor_readings(self, num_records=1000, start_time=None, 
                                introduce_issues=True):
        """
        Generate sensor readings with realistic issues
        
        Args:
            num_records: Number of sensor readings to generate
            start_time: Starting timestamp (default: now - 1 hour)
            introduce_issues: If True, add data quality issues
        """
        if start_time is None:
            start_time = datetime.now() - timedelta(hours=1)
        
        readings = []
        
        for _ in range(num_records):
            equipment_id = random.choice(self.equipment_ids)
            sensor_type = random.choice(self.sensor_types)
            
            # Generate timestamp (some will be out of order!)
            timestamp = start_time + timedelta(
                seconds=random.randint(0, 3600),
                microseconds=random.randint(0, 999999)
            )
            
            # Generate sensor value based on type
            value = self._generate_sensor_value(sensor_type)
            
            reading = {
                'equipment_id': equipment_id,
                'sensor_type': sensor_type,
                'timestamp': timestamp.isoformat(),
                'value': value,
                'unit': self._get_unit(sensor_type),
                'sensor_id': f"{equipment_id}-{sensor_type}-001",
                'data_source': 'SCADA_v2.3',
                'quality_flag': 'GOOD'
            }
            
            # Introduce realistic data quality issues
            if introduce_issues:
                reading = self._introduce_issues(reading)
            
            readings.append(reading)
        
        df = pd.DataFrame(readings)
        
        # Add some duplicates (network retries)
        if introduce_issues:
            duplicate_count = int(num_records * 0.02)  # 2% duplicates
            duplicates = df.sample(n=duplicate_count)
            df = pd.concat([df, duplicates], ignore_index=True)
        
        return df.sort_values('timestamp').reset_index(drop=True)
    
    def _generate_sensor_value(self, sensor_type):
        """Generate realistic sensor values"""
        if sensor_type == 'temperature':
            # Normal: 40-80°C, with occasional spikes
            return round(np.random.normal(60, 10), 2)
        
        elif sensor_type == 'vibration':
            # Normal: 0.01-0.05 mm/s, with occasional high vibration
            return round(np.random.exponential(0.03), 4)
        
        elif sensor_type == 'pressure':
            # Normal: 80-120 PSI
            return round(np.random.normal(100, 10), 2)
        
        elif sensor_type == 'power_consumption':
            # Normal: 50-200 kW
            return round(np.random.gamma(2, 50), 2)
        
        return 0.0
    
    def _get_unit(self, sensor_type):
        """Get measurement unit for sensor type"""
        units = {
            'temperature': 'celsius',
            'vibration': 'mm_per_sec',
            'pressure': 'psi',
            'power_consumption': 'kw'
        }
        return units.get(sensor_type, 'unknown')
    
    def _introduce_issues(self, reading):
        """Introduce realistic data quality issues"""
        issue_type = random.random()
        
        # 5% missing values
        if issue_type < 0.05:
            reading['value'] = None
            reading['quality_flag'] = 'MISSING'
        
        # 3% wrong data type (string instead of number)
        elif issue_type < 0.08:
            reading['value'] = "N/A"
            reading['quality_flag'] = 'INVALID'
        
        # 2% extreme outliers (sensor malfunction)
        elif issue_type < 0.10:
            reading['value'] = reading['value'] * random.choice([10, -10, 100])
            reading['quality_flag'] = 'OUTLIER'
        
        # 1% negative values (impossible for some sensors)
        elif issue_type < 0.11:
            reading['value'] = -abs(reading['value'])
            reading['quality_flag'] = 'INVALID'
        
        # 1% future timestamps (clock drift)
        elif issue_type < 0.12:
            future_time = datetime.fromisoformat(reading['timestamp']) + timedelta(hours=2)
            reading['timestamp'] = future_time.isoformat()
            reading['quality_flag'] = 'CLOCK_DRIFT'
        
        return reading
    
    def generate_maintenance_history(self, num_records=200):
        """Generate maintenance work order history"""
        maintenance_data = []
        
        maintenance_types = [
            'PREVENTIVE', 'CORRECTIVE', 'EMERGENCY', 'INSPECTION'
        ]
        
        failure_types = [
            'BEARING_FAILURE', 'OVERHEATING', 'VIBRATION_ANOMALY', 
            'PRESSURE_DROP', 'POWER_SURGE', 'MECHANICAL_WEAR'
        ]
        
        for _ in range(num_records):
            maintenance_date = fake.date_time_between(start_date='-2y', end_date='now')
            
            maintenance_data.append({
                'work_order_id': fake.bothify('WO-########'),
                'equipment_id': random.choice(self.equipment_ids),
                'maintenance_date': maintenance_date.isoformat(),
                'maintenance_type': random.choice(maintenance_types),
                'failure_type': random.choice(failure_types) if random.random() > 0.3 else None,
                'downtime_hours': round(random.uniform(0.5, 48), 1),
                'cost_usd': round(random.uniform(500, 25000), 2),
                'technician': fake.name(),
                'description': fake.text(max_nb_chars=200),
                'parts_replaced': random.choice([True, False]),
                'resolved': random.choice([True, True, True, False])  # 75% resolved
            })
        
        return pd.DataFrame(maintenance_data)
    
    def save_to_csv(self, df, filename, directory='data/sample_data'):
        """Save dataframe to CSV"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = f"{directory}/{filename}"
        df.to_csv(filepath, index=False)
        print(f"✅ Saved {len(df)} records to {filepath}")
        return filepath
    
    def save_to_json(self, df, filename, directory='data/sample_data'):
        """Save dataframe to JSON (line-delimited for streaming)"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = f"{directory}/{filename}"
        df.to_json(filepath, orient='records', lines=True)
        print(f"✅ Saved {len(df)} records to {filepath}")
        return filepath


# Example usage
if __name__ == "__main__":
    print("🏭 IoT Data Generator - Creating Sample Data\n")
    
    # Initialize generator
    generator = IoTDataGenerator(num_equipment=100, seed=42)
    
    # Generate equipment metadata
    print("1️⃣ Generating equipment metadata...")
    equipment_df = generator.generate_equipment_metadata()
    generator.save_to_csv(equipment_df, 'equipment_metadata.csv')
    print(f"   Equipment types: {equipment_df['equipment_type'].unique()}\n")
    
    # Generate sensor readings (with issues!)
    print("2️⃣ Generating sensor readings (WITH data quality issues)...")
    sensors_df = generator.generate_sensor_readings(
        num_records=10000, 
        introduce_issues=True
    )
    generator.save_to_csv(sensors_df, 'sensor_readings_10k.csv')
    generator.save_to_json(sensors_df, 'sensor_readings_10k.json')
    
    # Show quality issues
    quality_summary = sensors_df['quality_flag'].value_counts()
    print("\n   Data Quality Summary:")
    print(quality_summary)
    print(f"\n   Total issues: {len(sensors_df[sensors_df['quality_flag'] != 'GOOD'])} / {len(sensors_df)}")
    
    # Generate maintenance history
    print("\n3️⃣ Generating maintenance history...")
    maintenance_df = generator.generate_maintenance_history(num_records=200)
    generator.save_to_csv(maintenance_df, 'maintenance_history.csv')
    
    print("\n✅ Sample data generation complete!")
    print(f"\n📁 Files created in data/sample_data/:")
    print("   - equipment_metadata.csv (100 equipment)")
    print("   - sensor_readings_10k.csv (10,000 readings with issues)")
    print("   - sensor_readings_10k.json (same data, JSON format)")
    print("   - maintenance_history.csv (200 work orders)")