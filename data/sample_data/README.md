# Sample Data

This directory contains **realistic sample data** with intentional data quality issues.

## Files

### 1. equipment_metadata.csv (100 records)
Equipment master data for 100 machines across 4 factories.

**Columns:**
- `equipment_id`: Unique ID (EQ-0001 to EQ-0100)
- `equipment_type`: CNC_MACHINE, ROBOTIC_ARM, etc.
- `factory_location`: Factory_North/South/East/West
- `install_date`: When equipment was installed
- `status`: ACTIVE or MAINTENANCE

### 2. sensor_readings_10k.csv (10,000+ records)
IoT sensor readings with **realistic data quality issues** (~10% bad data).

**Columns:**
- `equipment_id`: FK to equipment_metadata
- `sensor_type`: temperature, vibration, pressure, power_consumption
- `timestamp`: ISO 8601 format
- `value`: Sensor reading (null if missing)
- `quality_flag`: GOOD, MISSING, INVALID, OUTLIER, CLOCK_DRIFT

**Data Quality Issues (Intentional):**
- 5% missing values (sensor failures)
- 3% wrong data types (strings instead of numbers)
- 2% outliers (sensor malfunctions)
- 1% negative values (impossible readings)
- 1% future timestamps (clock drift)
- 2% duplicates (network retries)

### 3. maintenance_history.csv (200 records)
Historical maintenance work orders.

**Columns:**
- `work_order_id`: Unique work order ID
- `equipment_id`: FK to equipment_metadata
- `maintenance_type`: PREVENTIVE, CORRECTIVE, EMERGENCY, INSPECTION
- `failure_type`: Type of failure (if applicable)
- `downtime_hours`: Equipment downtime
- `cost_usd`: Maintenance cost

## Generating More Data

To generate additional data:

```bash
python src/data_generators/iot_data_generator.py
```

You can modify parameters in the script to generate:
- More equipment (change `num_equipment`)
- More readings (change `num_records`)
- Cleaner data (set `introduce_issues=False`)