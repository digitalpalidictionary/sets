#!/usr/bin/env python3
# coding: utf-8

import os
import re
import pandas as pd
import warnings
from datetime import date
from timeis import timeis, yellow, red, green, line, tic, toc
from sorter import sort_key

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

	exceptions = ["dps", "ncped", "pass1", "sandhi"]

	set_names_list = list(set(set_names_string.split("; ")))
	set_names_list.remove('')
	for exception in exceptions:
		set_names_list.remove(exception)
	set_names_list.sort()

	with open("output/set_names_list.txt", "w") as f:
		for item in set_names_list:
			f.write(f"{item}\n")

def generate_set_html():
	global exceptions
	print(f"{timeis()} {green}generating sets html")

	dpd_df.loc[dpd_df["Meaning IN CONTEXT"] == "", "Meaning IN CONTEXT"] = dpd_df["Buddhadatta"] + "*"
	dpd_df.loc[dpd_df["Literal Meaning"] != "", "Meaning IN CONTEXT"] += "; lit. " + dpd_df["Literal Meaning"]
	
	set_name_length = len(set_names_list)
	counter = 0

	with open("../exporter/assets/dpd-words.css", "r") as c:
		css = c.read()

	for set_name in set_names_list:

		if counter % 25 == 0:
			print(f"{timeis()} {counter}/{set_name_length}\t{set_name}")

		exception_flag = False

		if exception_flag == False:
			test1 = dpd_df["Category"].str.contains(f"(^|; ){set_name}($|; )")
			test2 =  dpd_df["Meaning IN CONTEXT"] != ""
			filter = test1 & test2
			set_df = dpd_df.loc[filter, ["Pāli1", "POS", "Meaning IN CONTEXT"]]
			set_df = set_df.sort_values(by=["Pāli1", "Meaning IN CONTEXT"])
			set_df.sort_values(by=["Pāli1"], inplace=True, ignore_index=True, key=lambda x: x.map(sort_key))

			# set_df = set_df.set_index("Pāli1")
			# set_df.index.name = None
			# set_html = set_df.to_html(escape=False, header = None, index = True)
			# set_html = re.sub ('table border="1" class="dataframe"', 'table class="table1"', set_html)

			# print(set_df)

			if set_df.shape[0] > 0:
				set_html = f"""<style>{css}</style><table class = "table1">"""
				set_html = f"""<table class = "table1">"""
				length = set_df.shape[0]

				for row in range(length):
					pali = set_df.iloc[row, 0]
					pos = set_df.iloc[row, 1]
					meaning = set_df.iloc[row, 2]

					set_html += f"""<tr><th class="cfpali">{pali}</th><td class="cfpos">{pos}</td><td class="cfeng">{meaning}</td></tr>"""
					
				set_html += """</table>"""

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

tic()
setup_dpd_df()
extract_list_of_set_name()
generate_set_html()
delete_unused_files()
toc()
