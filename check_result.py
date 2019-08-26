import csv
import re
from fuzzywuzzy import fuzz

remove_str = set()
#replace words with blanks
with open('generic_words/generic_word_replacement.tsv', encoding='ISO-8859-1') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
       
        remove_str.add(row[0].lower())


with open('inputs/match_orbis_v1.tsv', encoding='ISO-8859-1') as tsvfile:
    with open('outputs/matched_result_v1_clean.tsv', 'w', newline="\n", encoding='utf-8-sig') as out_file: 
        csv_writer = csv.writer(out_file, delimiter='\t')
        reader = csv.DictReader(tsvfile, delimiter='\t')
      
        header = ['company_name', 'assignee_id', 'assignee_name', 'city', 'state', 'country', 'latitude', 'longitude', 'company_matched', 'subsidiary_matched','subsidiary_US_sic_text_description']
        csv_writer.writerow(header)
        for row in reader:
            row_dict = dict(row)
            subsid = row_dict['subsidiary_matched'].lower()
            assig = row_dict['assignee_name'].lower()
            comp = row_dict['company_matched'].lower()

            if comp != '' and (comp in assig):
  
           
                as_unprocessed = re.sub("[^\w]", " ",  row['assignee_name'].lower()).split()
                as_processed = []
                # ignore special char
                for word in as_unprocessed:
                    if not word in remove_str:
                        as_processed.append(word.lower())
                        
                asgn = ' '.join(as_processed)
                co_unprocessed = re.sub("[^\w]", " ",  row['company_matched'].lower()).split()
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
                        continue
                
                if len(comp.split()) > 1:
                    as_list = asgn.split()
             
                    comp_list = comp.split()
                    if comp_list[0] not in as_list:
                        continue
                output_list = []
                for ele, info in row_dict.items():
                    output_list.append(info)
              
                csv_writer.writerow(output_list)
                    
            if (subsid in assig):
                # get rid of nonwhole words
                if len(subsid.split()) == 1:
                    as_list = assig.split()
               
                    if subsid not in as_list:
                        
                        continue
                if len(subsid.split()) > 1:
                    as_list = assig.split()
                    sub_list = subsid.split()
                    if sub_list[0] not in as_list:
                        
                        continue
                
                # get rid if generics
                sub_unprocessed = re.sub("[^\w]", " ",  row['subsidiary_matched'].lower()).split()
                sub_processed = []
                as_unprocessed = re.sub("[^\w]", " ",  row['assignee_name'].lower()).split()
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
                    continue
                
                
                
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
                
                if (fuzz.token_set_ratio(subsid_clean, asgn) != 100):
                    continue
                
                output_list = []
                for ele, info in row_dict.items():
                    output_list.append(info)
                csv_writer.writerow(output_list)
              
            else:
                output_list = []
                for ele, info in row_dict.items():
                    output_list.append(info)
                csv_writer.writerow(output_list)
            