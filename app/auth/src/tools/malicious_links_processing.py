import pandas as pd
df = pd.read_csv('./resources/malicious_phish.csv')
rows = df.shape[0]
for i in range(rows):

    if "http://" in df['url'][i]:
        index = df['url'][i].find('http://')
        df['url'][i] = df['url'][i][index+7:]
    elif "https://" in df['url'][i]:
        index = df['url'][i].find('https://')
        df['url'][i] = df['url'][i][index+8:]

df.to_csv('./resources/links_without_http_https.csv')