import csv
import sys
from fuzzywuzzy import fuzz
import re

assignee_file = 'inputs/assignee_locations_master_full.tsv'
orbis = 'inputs/orbis_final.tsv'
output_file_orbis = 'outputs/match_orbis.tsv'
remove_str = set()

def clean_str():
    
    #replace words with blanks
    with open('generic_words/generic_word_replacement.tsv', encoding='ISO-8859-1') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
           
            remove_str.add(row[0].lower())
    return remove_str

def check_result(row_dict):
          subsid = row_dict['subsidiary_matched'].lower()
          assig = row_dict['organization'].lower()
          comp = row_dict['company_matched'].lower()
   
          if comp != '' and (comp in assig):
   
              as_unprocessed = re.sub("[^\w]", " ",  row_dict['organization'].lower()).split()
              as_processed = []
              # ignore special char
              for word in as_unprocessed:
                  if not word in remove_str:
                      as_processed.append(word.lower())
                      
              asgn = ' '.join(as_processed)
              co_unprocessed = re.sub("[^\w]", " ",  row_dict['company_matched'].lower()).split()
              co_processed = []
              # ignore special char
              for word in co_unprocessed:
                  if not word in remove_str:
                      co_processed.append(word.lower())
                      
              comp = ' '.join(co_processed)
              # get rid of nonwhole words

              if len(comp.split()) == 1:
                  as_list = asgn.split()
                  if comp not in as_list:
                      return False
              
              if len(comp.split()) > 1:
                  as_list = asgn.split()
           
                  comp_list = comp.split()
                  if comp_list[0] not in as_list:
                      return False
              return True
                  
          if subsid != '' and (subsid in assig):
             
              # get rid of nonwhole words
              if len(subsid.split()) == 1:
                  as_list = assig.split()
             
                  if subsid not in as_list:
                      return False
              if len(subsid.split()) > 1:
                  as_list = assig.split()
                  sub_list = subsid.split()
                  if sub_list[0] not in as_list:
                      return False
              
              # get rid if generics
              sub_unprocessed = re.sub("[^\w]", " ",  row_dict['subsidiary_matched'].lower()).split()
              
              sub_processed = []
              as_unprocessed = re.sub("[^\w]", " ",  row_dict['organization'].lower()).split()
              as_processed = []
              
              # ignore special char
              for word in sub_unprocessed:
                  if not word in remove_str:
                      sub_processed.append(word.lower())
                      
              # ignore special char
              for word in as_unprocessed:
                  if not word in remove_str:
                      as_processed.append(word.lower())
                      
              sub = ' '.join(sub_processed)
              asgn = ' '.join(as_processed)
              if (fuzz.token_set_ratio(sub, asgn) != 100):
                  return False
              
              
              
              # get rid of nonessential words
              subsid_clean = sub.lower().replace('GMBH & CO', '')
              subsid_clean = subsid_clean.replace('square', '')
              subsid_clean = subsid_clean.replace('medicine', '')
              subsid_clean = subsid_clean.replace('welding', '')
              subsid_clean = subsid_clean.replace('outdoor', '')
              subsid_clean = subsid_clean.replace('network', '')
              subsid_clean = subsid_clean.replace('kg', '')
              subsid_clean = subsid_clean.replace('security', '')
              subsid_clean = subsid_clean.replace('business', '')
              subsid_clean = subsid_clean.replace('waters', '')
              subsid_clean = subsid_clean.replace('advanced', '')
              subsid_clean = subsid_clean.replace('midwest', '')
              subsid_clean = subsid_clean.replace('northern', '')
              subsid_clean = subsid_clean.replace('southern', '')
              subsid_clean = subsid_clean.replace('western', '')
              subsid_clean = subsid_clean.replace('eastern', '')
              subsid_clean = subsid_clean.replace('bright', '')
              subsid_clean = subsid_clean.replace('tokyo', '')
              subsid_clean = subsid_clean.replace('hangzhou', '')
              subsid_clean = subsid_clean.replace('beijing', '')
              subsid_clean = subsid_clean.replace('hong kong', '')
              subsid_clean = subsid_clean.replace('headquarters', '')
              subsid_clean = subsid_clean.replace('san francisco', '')
              subsid_clean = subsid_clean.replace('virtual', '')
              subsid_clean = subsid_clean.replace('concept', '')
              subsid_clean = subsid_clean.replace('independent', '')
              subsid_clean = subsid_clean.replace('dyanamics', '')
              subsid_clean = subsid_clean.replace('trs', '')
              subsid_clean = subsid_clean.replace('att', '')
              
              if (fuzz.token_set_ratio(subsid_clean, asgn) != 100):
                  return False
              
              return True
            
          else:
              return True
            



def process_orbis_input():
    orbis_dict = {} #dictionary mapping acquirer to subsidiaries (in dict)
    #returns a dictionary from acquiring company to set of subsidiary and city pairs
    with open(orbis, encoding='ISO-8859-1') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        acquirer = ''
        for row in reader:
            if row['acquirer_name'] != '':
                acquirer = row['acquirer_name'].lower()
            
            if acquirer in orbis_dict:
                orbis_dict[acquirer].append(dict(row))
            else:
                orbis_dict[acquirer] = [dict(row)]

    return orbis_dict


if __name__ == '__main__':

    clean_str()
    orbis_dict = process_orbis_input()
    output_dict = {} #dictionary of list of dictionary
    #check with orbis
    with open(assignee_file, encoding='latin-1') as tsvfile:
        with open(output_file_orbis, 'w', newline="\n", encoding='utf-8-sig') as out_file: 
            csv_writer = csv.writer(out_file, delimiter='\t')
            header = ['company_name', 'company_id',  'company_bvd_id,', 'assignee_name', 'assignee_id', 'matched_subsidiary/branch_name', 'matched_sibsidiary/branch_id',  'subsidiary_branch_SIC', 'subsidiary_branch_SIC_txt', 
                      'subsidiary_branch', 'assignee_city', 'assignee_state', 'assignee_country', 'assignee_latitude', 'assignee_longitude']
            
            #header = ['company_name', 'country_iso_code', 'bvd_id_number', 'no_of_companies_in_corporate_group', 'assignee_id', 'assignee_name', 'state', 'city', 'country', 'latitude', 'longitude', 'company_matched', 'subsidiary_matched','subsidiary_US_sic_text_description', 'branch_matched','branch_US_sic_text_description']
            #csv_writer.writerow(header)
            
            reader = csv.DictReader(tsvfile, delimiter='\t')
        
            for row in reader:
                print(reader.line_num)
                assignee = row['organization']
                city = row['city']
                state= row['state']
                country = row['country']
                lat = row['latitude']
                lng = row['longitude']
                
                as_unprocessed = re.sub("[^\w]", " ",  assignee.lower()).split()
                as_processed = []
                # ignore special char
                for word in as_unprocessed:
                    if not word in remove_str:
                        as_processed.append(word.lower())
                      
                asgn = ' '.join(as_processed)
                for company, subs in orbis_dict.items():
                    # process remove words in company
                    co_unprocessed = re.sub("[^\w]", " ",  company.lower()).split()
                    co_processed = []
                    # ignore special char
                    for word in co_unprocessed:
                        if not word in remove_str:
                            co_processed.append(word.lower())
                          
                    comp = ' '.join(co_processed)
                    comp_list = comp.split()
                    as_list = asgn.split()
                    # if all generic words then do the following:
                
                    if (comp.isspace() or comp == '') and len(co_unprocessed) > 1:
                        print(company)
                        first_2_words = co_unprocessed[0] + co_unprocessed[1]
                        if first_2_words in assignee.lower():
                            row_dict = dict(row)
                            row_dict['company_matched'] = company.lower()
                            row_dict['subsidiary_matched'] = ''
                            row_dict['acquirer_uuid'] = sub['acquirer_uuid']
                            row_dict['BVD_id'] = sub['BvD_ID']
                            row_dict['N_companies_group'] = sub['N_companies_group']
                            row_dict['N_subsidiaries'] = sub['N_subsidiaries']
                            
                            
                            row_dict['subsidiary_branch_cntry'] = ''
                            row_dict['subsidiary_branch_state'] = ''
                            row_dict['subsidiary_branch_city'] = ''
                            row_dict['subsidiary_branch_SIC'] = ''
                            row_dict['subsidiary_branch_SIC_txt'] = ''
                            row_dict['subsidiary_branch'] = ''
                         
                            row_dict['row_id'] = sub['row_id']
                            
                            if company in output_dict:
                                output_dict[company].append(row_dict)
                            else:
                                output_dict[company] = [row_dict]
                            continue
                    if (len(comp_list) == 1 and comp in as_list) or (len(comp_list) > 1 and comp_list[0] in as_list):
                  
                        
                        row_dict = dict(row)
                        row_dict['company_matched'] = company.lower()
                        row_dict['subsidiary_matched'] = ''
                        row_dict['acquirer_uuid'] = sub['acquirer_uuid']
                        row_dict['BVD_id'] = sub['BvD_ID']
                        row_dict['N_companies_group'] = sub['N_companies_group']
                        row_dict['N_subsidiaries'] = sub['N_subsidiaries']
                        
                        
                        row_dict['subsidiary_branch_cntry'] = ''
                        row_dict['subsidiary_branch_state'] = ''
                        row_dict['subsidiary_branch_city'] = ''
                        row_dict['subsidiary_branch_SIC'] = ''
                        row_dict['subsidiary_branch_SIC_txt'] = ''
                        row_dict['subsidiary_branch'] = ''
                     
                        row_dict['row_id'] = sub['row_id']
                        
                        if company in output_dict:
                            output_dict[company].append(row_dict)
                        else:
                            output_dict[company] = [row_dict]
                    else:
                        for sub in subs:
                            row_dict = dict(row)
                            if sub['subsidiary_branch_name'] != '':
                                sub_unprocessed = re.sub("[^\w]", " ",  sub['subsidiary_branch_name'].lower()).split()
                                sub_processed = []
                                # ignore special char
                                for word in sub_unprocessed:
                                    if not word in remove_str:
                                        sub_processed.append(word.lower())
                          
                                subsid = ' '.join(sub_processed)
                              
                                
                                if subsid.isspace() or subsid == '':
                                    continue
                                if sub['subsidiary_branch_name'].lower() in assignee.lower():
             
                                    idx = assignee.lower().find(sub['subsidiary_branch_name'].lower())
                                    
                                    if idx != 0 and idx+len(sub['subsidiary_branch_name']) != len(assignee):
                                        if (not assignee[idx-1].isspace()) and (not assignee[idx+len(sub['subsidiary_branch_name'])].isspace()):
                                            continue
                                    else:  
                                        row_dict['company_matched'] = ''
                                        row_dict['subsidiary_matched'] = sub['subsidiary_branch_name']
                                   
                                        row_dict['acquirer_uuid'] = sub['acquirer_uuid']
                                        row_dict['BVD_id'] = sub['BvD_ID']
                                        row_dict['N_companies_group'] = sub['N_companies_group']
                                        row_dict['N_subsidiaries'] = sub['N_subsidiaries']
                                        
                                      
                                        row_dict['subsidiary_branch_cntry'] = sub['subsidiary_branch_cntry']
                                        row_dict['subsidiary_branch_state'] = sub['subsidiary_branch_state']
                                        row_dict['subsidiary_branch_city'] = sub['subsidiary_branch_city']
                                        row_dict['subsidiary_branch_SIC'] = sub['subsidiary_branch_SIC']
                                        row_dict['subsidiary_branch_SIC_txt'] = sub['subsidiary_branch_SIC_txt']
                                        row_dict['subsidiary_branch'] = sub['subsidiary_branch']
                                        row_dict['row_id'] = sub['row_id']
                                        
                                        
                                        
                                        if company in output_dict:
                                            output_dict[company].append(row_dict)
                                        else:
                                            output_dict[company] = [row_dict]
                                
                                elif fuzz.token_set_ratio(sub['subsidiary_branch_name'].lower(), assignee.lower()) >= 60:
                                    if sub['subsidiary_branch_city'] == '' or city == '':
                                        continue
                                    elif sub['subsidiary_branch_city'].lower() == city:
                                        row_dict['company_matched'] = ''
                                        row_dict['subsidiary_matched'] = sub['subsidiary_branch_name']
                                        row_dict['BVD_id'] = sub['BvD_ID']
                                        row_dict['acquirer_uuid'] = sub['acquirer_uuid']
                                        row_dict['corporate_name'] = sub['corporate_name']
                                        row_dict['N_companies_group'] = sub['N_companies_group']
                                        row_dict['N_subsidiaries'] = sub['N_subsidiaries']
                                        
                                        row_dict['subsidiary_branch_cntry'] = sub['subsidiary_branch_cntry']
                                        row_dict['subsidiary_branch_state'] = sub['subsidiary_branch_state']
                                        row_dict['subsidiary_branch_city'] = sub['subsidiary_branch_city']
                                        row_dict['subsidiary_branch_SIC'] = sub['subsidiary_branch_SIC']
                                        row_dict['subsidiary_branch_SIC_txt'] = sub['subsidiary_branch_SIC_txt']
                                        row_dict['subsidiary_branch'] = sub['subsidiary_branch']
                                        row_dict['row_id'] = sub['row_id']
                                        if company in output_dict:
                                            output_dict[company].append(row_dict)
                                        else:
                                            output_dict[company] = [row_dict]
                                        
                       
                            
            for company, subs in output_dict.items():
                
                for sub in subs:
                    output_list = [company]
                    if check_result(sub):
                        print(sub)
                        output_list.append(sub['acquirer_uuid'])
                        output_list.append(sub['BVD_id'])
                        output_list.append(sub['organization'])
                        output_list.append(sub['id'])
                        output_list.append(sub['subsidiary_matched'])
                        output_list.append(sub['row_id'])
                        output_list.append(sub['subsidiary_branch_SIC'])
                        output_list.append(sub['subsidiary_branch_SIC_txt'])
                        output_list.append(sub['subsidiary_branch'])
                        output_list.append(sub['city'])
                        output_list.append(sub['state'])
                        output_list.append(sub['country'])
                        output_list.append(sub['latitude'])
                        output_list.append(sub['longitude'])
                            
                        '''output_list.append(fuzz.token_set_ratio(company.lower(), sub['organization'].lower()))
                        if sub['subsidiary_matched'] != '':
                            output_list.append(fuzz.token_set_ratio(sub['subsidiary_matched'].lower(), sub['organization'].lower()))
                        '''
                        csv_writer.writerow(output_list)
                                
                        
                            
                