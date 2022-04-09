#!/usr/bin/env python3
# coding: utf-8

import os
import re
import pandas as pd
import warnings
from datetime import date
from timeis import timeis, yellow, red, green, line

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

today = date.today()
date = today.strftime("%d")

print(f"{timeis()} {yellow}sets generator") 
print(f"{timeis()} {line}")

def setup_dpd_df():
	print(f"{timeis()} {green}setting up dpd dataframe")
	global dpd_df, dpd_df_length

	dpd_df = pd.read_csv ("../csvs/dpd-full.csv", sep="\t", dtype=str)
	dpd_df = dpd_df.fillna("")
	dpd_df_length = len(dpd_df)

def extract_list_of_set_name():
	print(f"{timeis()} {green}extracting list of set names")
	global set_names_list

	set_names_list = []
	set_names_string = ""

	for row in range(dpd_df_length):
		set_cell = dpd_df.loc[row, "Category"]
		if set_cell != "":
			set_names_string += set_cell + "; "

	set_names_list = list(set(set_names_string.split("; ")))
	set_names_list.remove('')
	set_names_list.sort()

	with open("output/set_names_list.txt", "w") as f:
		for item in set_names_list:
			f.write(f"{item}\n")

def generate_set_html():
	global exceptions
	print(f"{timeis()} {green}generating sets html")

	dpd_df.loc[dpd_df["Meaning IN CONTEXT"] == "", "Meaning IN CONTEXT"] = dpd_df["Buddhadatta"] + "*"
	dpd_df.loc[dpd_df["Literal Meaning"] != "", "Meaning IN CONTEXT"] += "; lit. " + dpd_df["Literal Meaning"]
	
	# exceptions = ["books", "chapters", "suttas", "vaggas", "dps", "ncped"]
	set_name_length = len(set_names_list)
	counter = 0

	for set_name in set_names_list:

		if counter % 25 == 0:
			print(f"{timeis()} {counter}/{set_name_length}\t{set_name}")

		exception_flag = False
		# for exception in exceptions:
		# 	if re.findall(exception, set_name):
		# 		exception_flag = True

		if exception_flag == False:
			test1 = dpd_df["Category"].str.contains(f"{set_name}")
			test2 =  dpd_df["Meaning IN CONTEXT"] != ""
			filter = test1 & test2
			set_df = dpd_df.loc[filter, ["Pāli1", "POS", "Meaning IN CONTEXT"]]
			# set_df = set_df.sort_values(by=["Meaning IN CONTEXT", "Pāli1"])
			set_df = set_df.set_index("Pāli1")
			set_df.index.name = None
			set_html = set_df.to_html(escape=False, header = None, index = True)
			set_html = re.sub ('table border="1" class="dataframe"', 'table class="table1"', set_html)

			with open(f"output/html/{set_name}.html", "w") as f:
				f.write(set_html)
		
		counter += 1
	

def delete_unused_files():
	print(f"{timeis()} {green}deleting unused files")
	
	for root, dirs, files in os.walk("output/html/", topdown=True):
		for file in files:
			try:
				file_clean = re.sub(".html", "", file)
				if file_clean not in set_names_list:
					os.remove(f"output/html/{file_clean}.html")
					print(f"{timeis()} {file}")
			except:
				print(f"{timeis()} {red}{file} not found")

setup_dpd_df()
extract_list_of_set_name()
generate_set_html()
delete_unused_files()

print(f"{timeis()} {line}")

# print(f"{timeis()} {green}generating synonyms stop set")
    
    # stop_set1 = {"a", "and", "of", "or", "the", "from", "not", "to", "no", "be", "has", "who", "with", "as", "for", "by", "they", "he", "she", "it", "in", "on", "is", "was", "out", "did", "gram", "comm", "something", "one's", "a", "an", "at", "you", "about", "against", "all", "being", "having", "etc.", "fact", "which", "could", "would", "can", "one", "", "way", "I", "me", "will", "towards"}

    # # generating list of pali words in english meaning
    
    # pali_word_string = ""
    # english_word_string = ""
    # for row in range(df_length):
    #     w = DpdWord(df, row)
    #     pali_word_string += w.pali_clean + " "
    #     meaning = w.meaning.lower()
    #     meaning_clean = re.sub("[^A-Za-zāīūṭḍḷñṅṇṃ1234567890\-'’ ]", "", meaning)
    #     english_word_string += meaning_clean + " "

    # pali_word_set = set(pali_word_string.split(" "))
    # english_word_set = set(english_word_string.split(" "))
    # stop_set2 = pali_word_set & english_word_set
    # stop_set2 = set(sorted(stop_set2))
    # stop_set2.remove("")

    # print(f"{timeis()} {green}generating json")

    # with open(rsc['epd_css_path'], 'r') as f:
    #     epd_css = f.read()
    
    # epd_data_list = []

    # for key, value in epd.items():
    #     html_string = ""
        # synonyms = key
        # synonyms = re.sub("-", " ", synonyms)
        # synonyms = re.sub("[^A-Za-zāīūṭḍḷñṅṇṃ1234567890\-'’ ]", "", synonyms)
        # synonyms = synonyms.lower()
        # synonyms_set = set(synonyms.split(" "))
        # synonyms_set = synonyms_set - stop_set1
        # synonyms_set = synonyms_set - stop_set2

        # html_string = epd_css
        # html_string += f"<body><div class ='epd'><p>{value}</p></div></body></html>"

        # epd_data_list += [[f"{key}", f"""{html_string}""", "", ""]] #synonyms_set