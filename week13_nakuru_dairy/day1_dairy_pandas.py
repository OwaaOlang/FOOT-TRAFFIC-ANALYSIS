import pandas as pd

# STEP 1: Create sample data - 2 DataFrames like the exercise says
farmers_df = pd.DataFrame({
    'farmer_name': ['Kamau M.', 'Wanjiku J.', 'Otieno P.', 'Chebet A.', 'Mwangi K.', 'Akinyi S.',
                    'Kipchoge R.', 'Njeri L.', 'Omondi T.', 'Muthoni B.', 'Kiprono D.', 'Atieno F.'],
    'zone': ['Bahati', 'Bahati', 'Bahati', 'Bahati', 'Dundori', 'Dundori', 'Dundori', 'Dundori', 'Subukia', 'Subukia', 'Subukia', 'Subukia'],
    'rate_per_litre': [52, 52, 52, 52, 55, 55, 55, 55, 50, 50, 50, 50]
})

collection_df = pd.DataFrame([
    ['Kamau M.', '2026-11-01', 45], ['Kamau M.', '2026-11-02', 48], ['Kamau M.', '2026-11-03', 50], ['Kamau M.', '2026-11-04', 42], ['Kamau M.', '2026-11-05', 46],
    ['Wanjiku J.', '2026-11-01', 30], ['Wanjiku J.', '2026-11-02', 32], ['Wanjiku J.', '2026-11-03', 28], ['Wanjiku J.', '2026-11-04', 31],
    ['Otieno P.', '2026-11-01', 60], ['Otieno P.', '2026-11-02', 62], ['Otieno P.', '2026-11-03', 58], ['Otieno P.', '2026-11-04', 65], ['Otieno P.', '2026-11-05', 61],
    ['Chebet A.', '2026-11-01', 20], ['Chebet A.', '2026-11-02', 22], ['Chebet A.', '2026-11-03', 18], ['Chebet A.', '2026-11-04', 21],
    ['Mwangi K.', '2026-11-01', 55], ['Mwangi K.', '2026-11-02', 58], ['Mwangi K.', '2026-11-03', 60], ['Mwangi K.', '2026-11-04', 57], ['Mwangi K.', '2026-11-05', 59],
    ['Akinyi S.', '2026-11-01', 40], ['Akinyi S.', '2026-11-02', 42], ['Akinyi S.', '2026-11-03', 38], ['Akinyi S.', '2026-11-04', 41],
    ['Kipchoge R.', '2026-11-01', 70], ['Kipchoge R.', '2026-11-02', 72], ['Kipchoge R.', '2026-11-03', 68], ['Kipchoge R.', '2026-11-04', 71], ['Kipchoge R.', '2026-11-05', 69],
    ['Njeri L.', '2026-11-01', 35], ['Njeri L.', '2026-11-02', 33], ['Njeri L.', '2026-11-03', 36], ['Njeri L.', '2026-11-04', 34],
    ['Omondi T.', '2026-11-01', 48], ['Omondi T.', '2026-11-02', 50], ['Omondi T.', '2026-11-03', 52], ['Omondi T.', '2026-11-04', 49], ['Omondi T.', '2026-11-05', 51],
    ['Muthoni B.', '2026-11-01', 25], ['Muthoni B.', '2026-11-02', 27], ['Muthoni B.', '2026-11-03', 26], ['Muthoni B.', '2026-11-04', 24],
    ['Kiprono D.', '2026-11-01', 80], ['Kiprono D.', '2026-11-02', 82], ['Kiprono D.', '2026-11-03', 78], ['Kiprono D.', '2026-11-04', 79], ['Kiprono D.', '2026-11-05', 81],
    ['Atieno F.', '2026-11-01', 15], ['Atieno F.', '2026-11-02', 18], ['Atieno F.', '2026-11-03', 16], ['Atieno F.', '2026-11-04', 17],
], columns=['farmer_name','date','litres'])

# STEP 2: MERGE on farmer_name
merged = pd.merge(collection_df, farmers_df, on='farmer_name', how='left')
merged['payout_kes'] = merged['litres'] * merged['rate_per_litre']

# STEP 5: GROUPBY with multiple agg at once
summary = merged.groupby('zone').agg(
    total_litres=('litres', 'sum'),
    total_payout_kes=('payout_kes', 'sum')
)

# Get top farmer per zone
top = merged.groupby(['zone','farmer_name'])['litres'].sum().reset_index()
top = top.loc[top.groupby('zone')['litres'].idxmax()]
top = top.set_index('zone')[['farmer_name','litres']].rename(columns={'farmer_name':'top_farmer','litres':'top_farmer_litres'})

final_report = pd.concat([summary, top], axis=1)
final_report = final_report[['total_litres','total_payout_kes','top_farmer','top_farmer_litres']]

print("=== NAKURU DAIRY CO-OP - MONTHLY ZONE SUMMARY ===\n")
print(final_report)
