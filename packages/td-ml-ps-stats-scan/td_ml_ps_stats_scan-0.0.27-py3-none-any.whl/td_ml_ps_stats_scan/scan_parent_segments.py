import pandas as pd
import numpy as np
import sys
import os
import pytd
import requests
import json
import datetime
import re
import csv

## Increase CSV Max Size Limit
csv.field_size_limit(sys.maxsize)

##-- Declare ENV Variables from YML file
apikey = os.environ['TD_API_KEY'] 
tdserver = os.environ['TD_API_SERVER']
sink_database = os.environ['SINK_DB']
output_table = os.environ['OUTPUT_TABLE']
folder_depth = os.environ['FOLDER_DEPTH']
v5_flag = os.environ['v5_flag']
apply_ps_filters = os.environ['apply_ps_filters']
ps_to_include = os.environ['ps_to_include']
folders_to_include = os.environ['folders_to_include']
segments_to_include = os.environ['segments_to_include']
journeys_to_include = os.environ['journeys_to_include']
segment_api = tdserver.replace('api', 'api-cdp')
headers= {"Authorization":'TD1 '+ apikey, "content-type": "application/json"}

############ Function to Read JSON #####################
def json_extract(url):
    #Get Segment Info JSON from Master Segment using TD API
    get_info = requests.get(url, headers=headers)

    return get_info.json()

############ Function to clean odd characters from strings #####################
def replace_characters(input_string):
    pattern = r"[',\"]"
    try:
        output_string = re.sub(pattern, '', input_string)
    except:
        output_string = input_string
    return output_string

##########Function to extract Parent Segment Info from V4 and V5 ###########
def get_ps_list():
    v4_segment_list = f'https://{segment_api}/audiences'
    v5_segments_list = f'https://{segment_api}/entities/parent_segments'
    v4_dic = dict(ps_id = [], ps_id_v4 = [], ps_name = [], ps_population = [], root_folder = [])
    v5_dic = dict(ps_id = [], ps_id_v4 = [], ps_name = [], ps_population = [], root_folder = [])
    
    if v5_flag=='0':
        v4_ps = json_extract(v4_segment_list)
        for item in v4_ps:
            v4_dic['ps_id'].append(item['id'])
            v4_dic['ps_id_v4'].append(item['id'])
            v4_dic['ps_name'].append(item['name'])
            v4_dic['ps_population'].append(item['population'])
            v4_dic['root_folder'].append(item['rootFolderId'])

        v4_df = pd.DataFrame(v4_dic)
        v4_df.fillna(0, inplace = True)
        v4_df['v5_flag'] = 0
        new_df = v4_df
        new_df.reset_index(drop = True, inplace = True)

    elif v5_flag=='1': 
        v5_ps = json_extract(v5_segments_list)
        v5_ps_data = v5_ps['data']
        for item in v5_ps_data:
            v5_dic['root_folder'].append(item['id'])
            v5_dic['ps_id_v4'].append(item['id'])
            v5_dic['ps_name'].append(item['attributes']['name'] + " Root")
            v5_dic['ps_population'].append(item['attributes']['population'])
            v5_dic['ps_id'].append(item['relationships']['parentSegmentFolder']['data']['id'])


        v5_df = pd.DataFrame(v5_dic)
        v5_df.fillna(0, inplace = True)
        v5_df['v5_flag'] = 1
        
        new_df = v5_df
        new_df.reset_index(drop = True, inplace = True)
        
    elif v5_flag=='1,0':
        v4_ps = json_extract(v4_segment_list)
        for item in v4_ps:
            v4_dic['ps_id'].append(item['id'])
            v4_dic['ps_id_v4'].append(item['id'])
            v4_dic['ps_name'].append(item['name'])
            v4_dic['ps_population'].append(item['population'])
            v4_dic['root_folder'].append(item['rootFolderId'])

        v4_df = pd.DataFrame(v4_dic)
        v4_df.fillna(0, inplace = True)
        v4_df['v5_flag'] = 0

        v5_ps = json_extract(v5_segments_list)
        v5_ps_data = v5_ps['data']
        for item in v5_ps_data:
            v5_dic['root_folder'].append(item['id'])
            v5_dic['ps_id_v4'].append(item['id'])
            v5_dic['ps_name'].append(item['attributes']['name'] + " Root")
            v5_dic['ps_population'].append(item['attributes']['population'])
            v5_dic['ps_id'].append(item['relationships']['parentSegmentFolder']['data']['id'])


        v5_df = pd.DataFrame(v5_dic)
        v5_df.fillna(0, inplace = True)
        v5_df['v5_flag'] = 1
        
        new_df = pd.concat([v4_df, v5_df])
        new_df.reset_index(drop = True, inplace = True)
    else:
        print("provide valid v5_flag")

    #check if only to return data for specific Parent Segments
    if apply_ps_filters == 'yes':
        new_df = new_df[new_df['ps_name'].astype(str).str.lower().str.contains(ps_to_include, regex=True)]

    return new_df


######## Function to extract Folder Info from V4 and V5 ################
def get_folder_list(ps_df):
    v4_ps = list(ps_df[ps_df.v5_flag == 0].ps_id)
    v5_ps = list(zip(list(ps_df[ps_df.v5_flag == 1].root_folder), list(ps_df[ps_df.v5_flag == 1].ps_id)))
    
    combined_folders = []

    for master_id in v4_ps:
        try:
            v4_url_folders = f'https://{segment_api}/audiences/{master_id}/folders'
            v4_json = json_extract(v4_url_folders)
            print("v4_json")
            print(v4_json)

            folders = [{'ps_id': master_id, 'folder_id': item['id'], 'folder_name': item['name']} for item in v4_json]
            combined_folders.extend(folders)
        except:
            print(f"No Audience Segments built V4 for Parent Segment - {master_id}")

    if len(v5_ps) > 0:
        for id_list in v5_ps:
            v5_url_folders = f'https://{segment_api}/audiences/{id_list[0]}/folders'
            v5_json = json_extract(v5_url_folders)
            folders = [{'ps_id': id_list[1], 'folder_id': item['id'], 'folder_name': item['name'],'parent_folder':item['parentFolderId']} for item in v5_json]
            combined_folders.extend(folders)
            
    combined_folders_df= pd.DataFrame(combined_folders)
    final_df = pd.DataFrame(combined_folders)
                
    def find_subfolders(df, parent_id):
        subfolders = df[df['parent_folder'] == parent_id]
        results = []
        for _, subfolder in subfolders.iterrows():
            results.append(subfolder)
            results.extend(find_subfolders(df, subfolder['folder_id']))
        return results

    if apply_ps_filters == 'yes':
        final_df = final_df[final_df['folder_name'].str.lower().str.contains(folders_to_include, regex=True)]
        for folder_id_to_search in  final_df['folder_id'].to_list():    
            subfolders = find_subfolders(combined_folders_df, folder_id_to_search)
            subfolders_df = pd.DataFrame(subfolders)
            final_df=pd.concat([final_df,subfolders_df ])

    return final_df


################## Function to extract Segment Info from V4 and V5 #############
def get_segment_list(combined_df):
    v4_ps = list(set(combined_df[combined_df.v5_flag == 0].ps_id))
    v5_ps = list(set(combined_df[combined_df.v5_flag == 1].ps_id))
    folder_list = combined_df['folder_id'].unique().tolist()
    
    combined_segments = []

    for master_id in v4_ps:
        v4_url_segments = f'https://{segment_api}/audiences/{master_id}/segments'
        v4_json = json_extract(v4_url_segments)

        segments = [{'folder_id': item['segmentFolderId'], 'segment_id': item['id'], 'segment_name': item['name'],
            'segment_population': item['population'], 'realtime': item['realtime'], 'rule': item['rule'],
            'create_date':item['createdAt'],'num_syndications':item['numSyndications']} for item in v4_json]
        
        combined_segments.extend(segments)

    if len(v5_ps) > 0:
        for master_id in v5_ps:
            v5_url_segments = f'https://{segment_api}/entities/by-folder/{master_id}?depth=10'
            v5_json = json_extract(v5_url_segments)['data']
            segment_json = [item for item in v5_json if item['type'].startswith('segment-')]

            segments = [{'folder_id': item['relationships']['parentFolder']['data']['id'], 'segment_id': item['id'], 
                         'segment_name': item['attributes']['name'],'segment_population': item['attributes']['population'], 
                         'realtime': item['type'], 'rule': item['attributes']['rule'], 'create_date':item['attributes']['createdAt'],
                         'num_syndications':item['attributes']['numSyndications']} for item in segment_json]
            
            combined_segments.extend(segments)
            
    segment_df = pd.DataFrame(combined_segments)
    segment_df.realtime = [1 if item == True or str(item).startswith('segment-re') else 0 for item in list(segment_df.realtime)]
    segment_df['segment_type'] = ['regular' for item in list(segment_df.segment_id)]
    
    #check if only to return data for specific folders
    if apply_ps_filters == 'yes':
        segment_df = segment_df[segment_df['folder_id'].isin(folder_list) & segment_df['segment_name'].astype(str).str.lower().str.contains(segments_to_include, regex=True)]
            
    return segment_df

################## Function to extract CJO Journey Stages info from V5 #############
def get_journey_list(combined_df):
    #get list of Parent Segment IDs and list of distinct folder_ids
    ps_list = combined_df['ps_id'].unique().tolist()
    folder_ids = combined_df['folder_id'].unique().tolist()
    ps_names = combined_df['ps_name'].unique().tolist()
    folder_names = combined_df['folder_name'].unique().tolist()
    
    #create empty journey dictionary
    journey_info = dict(folder_id = [], segment_type = [], journey_id = [], journey_name = [], audience_id = [], 
                 state = [], stage_id = [], stage_idx = [], stage_name = [], segment_name = [], segment_id = [])
    
    #Loop through PS list and extract journey info
    for master_id in ps_list:
        journey_url = f'https://{segment_api}/entities/journeys?folder_id={master_id}'
        journeys_json = json_extract(journey_url)['data']
        
        for journey in journeys_json:
            #Only extract stats for 'Active' Journeys
            if journey['attributes']['state'] != 'draft':
                #Loop through Journey JSON and extract stages info
                for idx, stage in enumerate(journey['attributes']['journeyStages']):
                    journey_info['folder_id'].append(journey['relationships']['parentFolder']['data']['id'])
                    journey_info['segment_type'].append(journey['type'])
                    journey_info['journey_id'].append(journey['id'])
                    journey_info['journey_name'].append(journey['attributes']['name'])
                    journey_info['audience_id'].append(journey['attributes']['audienceId'])
                    journey_info['state'].append(journey['attributes']['state'])
                    journey_info['stage_id'].append(stage['id'])
                    journey_info['stage_idx'].append(idx)
                    journey_info['stage_name'].append(stage['name'])

                    #if entryCriteria exists extract it, otherwise use base stage info
                    try:
                        journey_info['segment_name'].append(stage['entryCriteria']['name'])
                        journey_info['segment_id'].append(stage['entryCriteria']['segmentId'])
                    except:
                        journey_info['segment_name'].append(stage['name'])
                        journey_info['segment_id'].append(stage['id'])

    journey_df = pd.DataFrame(journey_info)
    
    #check if only to return data for specific segments
    if apply_ps_filters == 'yes':
        journey_df = journey_df[journey_df['folder_id'].isin(folder_ids) & journey_df['journey_name'].astype(str).str.lower().str.contains(journeys_to_include, regex=True)]
    
    #extract segment population and query rule for journey stages
    segments_info = dict(segment_population = [], rule = [])
    
    for segment_id in journey_df.segment_id:
        
        if len(segment_id) > 5:
            segments_url = f'https://{segment_api}/entities/segments/{segment_id}'
            segments_json = json_extract(segments_url)['data']

            segments_info['segment_population'].append(segments_json['attributes']['population'])
            segments_info['rule'].append(segments_json['attributes']['rule'])
        else:
            segments_info['segment_population'].append(np.nan)
            segments_info['rule'].append(np.nan)
            
    journey_df['segment_population'] = segments_info['segment_population']
    journey_df['rule'] = segments_info['rule']
    
    #Extract Population for each stage from statistics API
    journey_stats = dict(journey_id = [], stage_id = [], stage_population = [])
    distinct_journeys =  journey_df['journey_id'].unique().tolist()

    if len(distinct_journeys) > 0:

        for journey_id in distinct_journeys:
            stats_url = f'https://{segment_api}/entities/journeys/{journey_id}/statistics'
            stats_json = json_extract(stats_url)['data']


            for stage in stats_json['attributes']['journeyStageStatistics']:
                journey_stats['journey_id'].append(journey_id)
                journey_stats['stage_id'].append(stage['id'])
                journey_stats['stage_population'].append(stage['history'][-1]['size'])

        #Create Stats DF
        stats_df = pd.DataFrame(journey_stats)

        #Merge Journey_df with stats DF
        final_df = pd.merge(journey_df, stats_df, on=['journey_id', 'stage_id'], how='left')

        #Add stage rule syntax
        stage_rules = []
        for row_tuple in final_df.itertuples(index=False):
            rule = f'SELECT cdp_customer_id FROM cdp_audience_{row_tuple[4]}.journey_{row_tuple[2]} WHERE intime_stage_{row_tuple[7]} IS NOT NULL AND outtime_stage_{row_tuple[7]} IS NULL'
            stage_rules.append(rule)
        #Add stage rule syntax
        final_df['stage_rule'] = stage_rules

        return final_df
    
    else:
        print(f'*** No Journeys Found in PS: {ps_names} OR in Segment Folders: {folder_names}')
        
        return journey_df 


################## Function to extract CJO Funnel Stages info from V5 #############
def get_funnel_list(ps_df):
    #get list of Parent Segment IDs
    ps_list = list(ps_df.root_folder)
    
    #create empty funnel dictionary
    funnel_info = dict(cdp_audience_id = [], funnel_id = [], funnel_name = [], funnel_population = [], folder_id = [], 
             stage_id = [], stage_name = [], segment_id = [], segment_name = [], segment_population = [], rule = [])
    
    #Loop through PS list and extract funnel info
    for master_id in ps_list:
        funnel_url = f'https://{segment_api}/entities/parent_segments/{master_id}/funnels'
        funnels_json = json_extract(funnel_url)['data']
        
        for funnel in funnels_json:
            
            for stage in funnel['attributes']['stages']:
                funnel_info['cdp_audience_id'].append(master_id)
                funnel_info['funnel_id'].append(funnel['id'])
                funnel_info['funnel_name'].append(funnel['attributes']['name'])
                funnel_info['funnel_population'].append(funnel['attributes']['population'])
                funnel_info['folder_id'].append(funnel['relationships']['parentFolder']['data']['id'])
                funnel_info['stage_id'].append(stage['id'])
                funnel_info['stage_name'].append(stage['name'])
                funnel_info['segment_id'].append(stage['segmentId'])
                funnel_info['segment_name'].append(stage['name'])
                funnel_info['segment_population'].append(stage['population'])
                
                #get query rule for creating stage segment
                segment_id = stage['segmentId']
                segment_url = f'https://{segment_api}/entities/segments/{segment_id}'
                segments_json = json_extract(segment_url)['data']
                funnel_info['rule'].append(segments_json['attributes']['rule'])  
                
    funnel_df = pd.DataFrame(funnel_info)
    funnel_df['funnel_flag'] = [1 for item in funnel_df.cdp_audience_id]
                
    return funnel_df

################## Function to extract CJO Historic Funnel Population Stats #############
def get_funnel_stats(funnel_df):
    funnel_list = list(zip(funnel_df.cdp_audience_id, funnel_df.funnel_id, funnel_df.funnel_name))
    
    funnel_info = dict(time = [], tstamp = [], ps_id = [], funnel_id = [], funnel_name = [], 
                        stage_id = [],  population = [])
    
    for funnels in funnel_list:
        ps_id = funnels[0]
        funnel_id = funnels[1]
        funnel_stats = f'https://{segment_api}/audiences/{ps_id}/funnels/{funnel_id}/statistics'
        stats_json = json_extract(funnel_stats)
        
        for stage in stats_json['stages']:
            for date in stage['history']:
                funnel_info['time'].append(int(date[0]))
                timestamp = datetime.datetime.fromtimestamp(date[0])
                funnel_info['tstamp'].append(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                funnel_info['ps_id'].append(ps_id)
                funnel_info['funnel_id'].append(funnel_id)
                funnel_info['funnel_name'].append(funnels[2])
                funnel_info['stage_id'].append(stage['id'])
                funnel_info['population'].append(date[1])
    
    
    stats_df = pd.DataFrame(funnel_info)
    stages_df = funnel_df[['stage_id', 'stage_name']]
    stages_df['stage_id'] = stages_df['stage_id'].astype('int64')
    stats_final = pd.merge(stats_df, stages_df, on='stage_id', how = 'left')
    
    return stats_final

##################### GET NESTED SEGMENTS FUNCTION #####################################
#Function Below extract IDs of Segments used as Include/Exclude rules of another Segment
def get_nested_segments(final_df):
    #get list of segment rules
    rules_list = [str(item) for item in list(final_df['rule'])]
    
    #define RegExp Patterns
    exclude_pattern = r"'exclude': True, 'id':|'include': False, 'id':"
    include_pattern = r"'include': True, 'id':|'exclude': False, 'id':"
    extract_ids = re.compile("'id': '(\d+)")


    exclude_flag = [1 if re.search(exclude_pattern, item) else 0 for item in rules_list]
    include_flag = [1 if re.search(include_pattern, item) else 0 for item in rules_list]
    nested_segments = [extract_ids.findall(item) for item in rules_list]
    
    final_df['exclude_flag'] = exclude_flag
    final_df['include_flag'] = include_flag
    final_df['nested_segments'] = nested_segments
    
    return final_df

##################### FINAL FUNCTION THAT RUNS ALL CODE #####################################

def extract_segment_stats():

    #get Parent Segment DF
    ps_df = get_ps_list()

    #get Folder Info DF
    folders_df = get_folder_list(ps_df)

    #Merge both DFs on ps_id
    combined_df = pd.merge(ps_df, folders_df, on="ps_id", how = 'left')

    #Get Folder Segments Info
    segments_df = get_segment_list(combined_df)
    
    #Get CJO Journeys Info
    journey_df = get_journey_list(combined_df)

    #If CJO Journeys exist, combine segments and funnel DFs and get funnel stats
    if len(journey_df) > 0:
        journey_final = journey_df[['folder_id', 'journey_name', 'segment_id', 'segment_name', 'segment_population', 'segment_type', 'rule', 'stage_name', 'stage_id', 'stage_idx',  'stage_population', 'stage_rule']]
        segments_df = pd.concat([segments_df, journey_final])
        segments_df.reset_index(drop=True, inplace=True)
    #If no CJO journeys, add empty columns with NaN values for Journey stats
    else:
        df_len = len(segments_df)
        segments_df['journey_name'] = [np.nan] * df_len
        segments_df['stage_name'] = [np.nan] * df_len
        segments_df['stage_id'] = [np.nan] * df_len
        segments_df['stage_idx'] = [np.nan] * df_len
        segments_df['stage_population'] = [np.nan] * df_len
        segments_df['stage_rule'] = [np.nan] * df_len

    #Merge Segments DF into combined on folder_id
    final_df = pd.merge(combined_df, segments_df, on="folder_id", how = 'inner')

    # Apply the 'replace_characters' function to cleanup names of Segments for Dashboard
    final_df['ps_name'] = final_df['ps_name'].apply(replace_characters)
    final_df['folder_name'] = final_df['folder_name'].apply(replace_characters)
    final_df['segment_name'] = final_df['segment_name'].apply(replace_characters)
    final_df['journey_name'] = final_df['journey_name'].apply(replace_characters)
    final_df['stage_name'] = final_df['stage_name'].apply(replace_characters)

    #Replace NaN with 0 for numeric columns and drop duplicate columns caused by v4/v5 segment name overlap
    final_df.segment_population.fillna(0, inplace = True)
    final_df.realtime.fillna(0, inplace = True)
    final_df.dropna(subset = ['segment_id'], inplace = True)
    final_df.drop_duplicates(subset=['root_folder', 'folder_id', 'folder_name', 'segment_id', 'segment_name'], keep='first', inplace=True, ignore_index=False)

    #Ensure population columns are written as INTEGER
    final_df['segment_population'] = pd.to_numeric(final_df['segment_population'], errors='coerce').astype('Int64')
    
    try:
        final_df['stage_population'] = pd.to_numeric(final_df['stage_population'], errors='coerce').astype('Int64')
    except:
        print(f'######## No Journey Segments Were Found in Parent Segment ID: {list(combined_df.ps_name)} ########')

    #Get Nested Segment Flags and Ids
    final_df = get_nested_segments(final_df)
    final_df.info()

    #Write final_df to TD
    client = pytd.Client(apikey=apikey, endpoint=tdserver, database=sink_database)
    client.load_table_from_dataframe(final_df, output_table, writer='bulk_import', if_exists='overwrite')
    
    #If CJO JOurneys Exist, write separate table to track journey stats daily
    if len(journey_df) > 0:
        #Merge joruney DF into combined on folder_id
        journey_final = pd.merge(combined_df, journey_df, on="folder_id", how = 'inner')

        #Replace NaN with 0 for numeric columns and drop duplicate columns caused by v4/v5 segment name overlap
        journey_final.segment_population.fillna(0, inplace = True)
        journey_final.dropna(subset = ['segment_id'], inplace = True)
        journey_final.drop_duplicates(subset=['root_folder', 'folder_id', 'folder_name', 'segment_id', 'segment_name'], keep='first', inplace=True, ignore_index=False)
        
        #Write final table to TD
        client = pytd.Client(apikey=apikey, endpoint=tdserver, database=sink_database)
        client.load_table_from_dataframe(journey_final, 'segment_analytics_journey_stats', writer='bulk_import', if_exists='append')
        
    else:
        print(f'No CJO journeys were found in Parent Segments:  {list(combined_df.ps_name)}')


def extract_journey_stats():
    #get Parent Segment DF
    ps_df = get_ps_list()

    #get Folder Info DF
    folders_df = get_folder_list(ps_df)

    #Merge both DFs on ps_id
    combined_df = pd.merge(ps_df, folders_df, on="ps_id", how = 'left')

    #Get CJO Funnels Info
    journey_df = get_journey_list(combined_df)

    #If CJO Funnels exist, combine segments and journey info into a final+df
    if len(journey_df) > 0:
        #Merge joruney DF into combined on folder_id
        final_df = pd.merge(combined_df, journey_df, on="folder_id", how = 'inner')

        #Replace NaN with 0 for numeric columns and drop duplicate columns caused by v4/v5 segment name overlap
        final_df.segment_population.fillna(0, inplace = True)
        final_df.dropna(subset = ['segment_id'], inplace = True)
        final_df.drop_duplicates(subset=['root_folder', 'folder_id', 'folder_name', 'segment_id', 'segment_name'], keep='first', inplace=True, ignore_index=False)
        
        #write table to TD
        client = pytd.Client(apikey=apikey, endpoint=tdserver, database=sink_database)
        client.load_table_from_dataframe(final_df, 'segment_analytics_journey_stats', writer='bulk_import', if_exists='append')
        
    else:
        print(f'No CJO journeys were found in Parent Segments:  {list(combined_df.ps_name)}')
