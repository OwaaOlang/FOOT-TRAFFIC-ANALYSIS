# Nakuru Dairy Co-op - Zone Collection Summary

A small data analysis project for Nakuru County dairy farmers. Calculates total milk collection, payout, and zone performance from daily collections.

### The Problem
The co-op collects milk daily from farmers in Rongai and Molo zones at different rates per litre. Need a quick report: total litres per zone, total payout, and top supplier.

### Dataset
- `farmers.csv` - 4 farmers with zone and rate (KES 42-45 per litre)
    - Rongai: Kamau H., Otieno P. @ 45 KES/L
    - Molo: Wanjiku J., Chebet A. @ 42 KES/L
- `collection.csv` - 19 records from 2026-11-01 to 2026-11-05
- `zone_summary.csv` - generated summary output

### How to Run
```bash
pip install pandas
python nakuru_dairy.py




#