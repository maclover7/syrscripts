import pandas as pd

IPEV_COLS = ['Registrant ID', 'Time']
MAIL_COLS = ['State ID', 'Last Received Delivery Status']
VOTER_COLS = [
    'State ID',
    'Birth date',
    'Party',
    'Town',
    'Village',
    'Voter History'
]

votersdf = pd.read_csv('voters-102526.CSV')
votersdf = votersdf[VOTER_COLS]
votersdf['voted_ge22'] = votersdf['Voter History'].str.contains('GE22')
votersdf['voted_ge24'] = votersdf['Voter History'].str.contains('GE24')
votersdf['age_ge26'] = ((pd.to_datetime('11/03/2026') - pd.to_datetime(votersdf['Birth date'])).dt.days / 365).astype(int)

ipevdf = pd.read_csv('ipev-110126.CSV')
ipevdf = ipevdf[IPEV_COLS]
ipevdf = ipevdf.rename(columns={'Registrant ID': 'State ID'})

maildf = pd.read_csv('mail-110126.CSV')
maildf = maildf[MAIL_COLS]

ipevdf = pd.merge(ipevdf, votersdf, on='State ID')
maildf = pd.merge(maildf, votersdf, on='State ID')

print("Mail by return status:")
mailstatusdf = maildf['Last Received Delivery Status'].value_counts().reset_index()
mailstatusdf['pct'] = 100 * mailstatusdf['count'] / len(maildf)
print(mailstatusdf.sort_values(by='pct'))

maildf = maildf[~maildf['Last Received Delivery Status'].isna()]

print("Average age for IPEV: %i" % ipevdf.age_ge26.mean())
print("Average age for Mail: %i" % maildf.age_ge26.mean())

print("IPEV who voted in GE22 & GE24: %i (of %i)" % (len(ipevdf[(ipevdf.voted_ge22) & (ipevdf.voted_ge24)]), len(ipevdf)))
print("Mail who voted in GE22 & GE24: %i (of %i)" % (len(maildf[(maildf.voted_ge22) & (maildf.voted_ge24)]), len(maildf)))

print("IPEV by party:")
ipevpartydf = ipevdf.Party.value_counts().reset_index()
ipevpartydf['pct'] = 100 * ipevpartydf['count'] / ipevpartydf['count'].sum()
print(ipevpartydf.sort_values(by='pct'))

print("IPEV who voted, or didn't, in GE22 & GE24:")
print(ipevdf.voted_ge22.value_counts())
print(ipevdf.voted_ge24.value_counts())
print(len(ipevdf[(~ipevdf.voted_ge22) & (~ipevdf.voted_ge24)]))
print(len(ipevdf))

print("Number of registered voters:")
print(len(votersdf))