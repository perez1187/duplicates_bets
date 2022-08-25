import pandas as pd
import gspread
import os
import actual_result
# import ipdb

def remove_file():
    try:
        os.remove('data/my_data.csv')
    except:
        pass

no_file = {'league': ['none'],
                'match': ['none'],
                'bet': ['none'],
                'outcome': ['none'],
                'sb': ['none'],
                'date': ['none'],
                'value (%)': ['none']
                }

def candidates():
    try:
        tenis = pd.read_excel(r"data\tenis.xlsx", sheet_name='sb')
        print(tenis)
    except:
        tenis = pd.DataFrame(no_file)
        print("chuj")
    try:
        pilka = pd.read_excel(r"data\pilka.xlsx", sheet_name='sb')
    except:
        pilka = pd.DataFrame(no_file)
    try:
        football_stats = pd.read_excel(r"data\football.xlsx", sheet_name='sb')
    except:
        football_stats = pd.DataFrame(no_file)

    df_concat = pd.DataFrame()
    df_concat['league'] = pd.concat([tenis['league'], pilka['league'], football_stats['league']])
    df_concat['match'] = pd.concat([tenis['match'], pilka['match'],football_stats['match']])
    df_concat['bet'] = pd.concat([tenis['bet'], pilka['bet'], football_stats['bet']])
    df_concat['outcome'] = pd.concat([tenis['outcome'], pilka['outcome'],football_stats['outcome']])
    df_concat['sb'] = pd.concat([tenis['sb'], pilka['sb'],football_stats['sb']])
    df_concat['date'] = pd.concat([tenis['date'], pilka['date'],football_stats['date']])
    df_concat['value (%)'] = pd.concat([tenis['value (%)'], pilka['value (%)'],football_stats['value (%)']])
    df_concat['active'] = 'candidates'

    return df_concat

def active_bets():
    gs = gspread.service_account(filename='creds.json')
    sh = gs.open('JAZDA Z KURWAMI 2022')  # name of google sheet
    active_worksheet = sh.worksheet('active_bets')
    df_active = pd.DataFrame(active_worksheet.get_all_values())
    #print(df_active[4])
    return df_active

def active_bets_pc():
    try:
        df_active_bets = pd.read_excel(r"data\active.xlsx", sheet_name='active_bets')
    except:
        df_active_bets = pd.DataFrame(no_file)
    return df_active_bets


def my_data(df_candidates, df_active):
    df_my_data = pd.DataFrame()
    df_my_data['status'] = pd.concat([df_active[0],df_candidates['active']])
    df_my_data['league'] = pd.concat([df_active[1],df_candidates['league']])
    df_my_data['match'] = pd.concat([df_active[2],df_candidates['match']])
    df_my_data['bet'] = pd.concat([df_active[3],df_candidates['bet']])
    df_my_data['outcome'] = pd.concat([df_active[4],df_candidates['outcome']])
    df_my_data['sb'] = pd.concat([df_active[5],df_candidates['sb']])
    df_my_data['date'] = pd.concat([df_active[7],df_candidates['date']])
    df_my_data['value (%)'] = pd.concat([df_active[10],df_candidates['value (%)']])
    #print(df_my_data.dtypes)
    return df_my_data

def my_data_PC(df_candidates, df_active):
    df_my_data = pd.DataFrame()
    # ipdb.set_trace()
    df_my_data['status'] = pd.concat([df_active['status'],df_candidates['active']])
    df_my_data['league'] = pd.concat([df_active['league'],df_candidates['league']])
    df_my_data['match'] = pd.concat([df_active['match'],df_candidates['match']])
    df_my_data['bet'] = pd.concat([df_active['bet'],df_candidates['bet']])
    df_my_data['outcome'] = pd.concat([df_active['outcome'],df_candidates['outcome']])
    df_my_data['sb'] = pd.concat([df_active['sb'],df_candidates['sb']])
    df_my_data['date'] = pd.concat([df_active['date'],df_candidates['date']])
    df_my_data['value (%)'] = pd.concat([df_active['value (%)'],df_candidates['value (%)']])
    #print(df_my_data)
    return df_my_data


def duplicates(df):
    df['duplicate'] = df.duplicated(subset=['match', 'bet', 'outcome'])

    try:
        os.remove(r'data\final_data.xlsx')
    except:
        pass
    df.to_excel(r'data\final_data.xlsx', index=False)
    #print(df)


def find_duplicates():
    df = pd.read_csv(r"data\active.csv")
    df2 = pd.read_csv(r"data\candidates.csv")
    df_main = pd.concat([df,df2])
    df_main['is_ok']=df_main.duplicated(subset=['match','bet', 'outcome'])
    df_main.to_csv(r'data/my_data.csv')
    #print (df_main)

def __main__():
    #find_duplicates() # old


    can = candidates()

    act = active_bets_pc()
    final_df = my_data_PC(can, act)
    duplicates(final_df)
    actual_result.df_all_coupons()
    print("done")

if __name__ == "__main__":
    __main__()

