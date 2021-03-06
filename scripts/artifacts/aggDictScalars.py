import glob
import os
import pathlib
import plistlib
import sqlite3
import json

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, is_platform_windows 


def get_aggDictScalars(files_found, report_folder, seeker):
	file_found = str(files_found[0])
	db = sqlite3.connect(file_found)
	cursor = db.cursor()

	cursor.execute(
	"""
	SELECT
	   DATE(DAYSSINCE1970*86400, 'unixepoch') AS DAY,
	   KEY AS "KEY",
	   VALUE AS "VALUE"
	FROM
	   SCALARS
	"""
	)

	all_rows = cursor.fetchall()
	usageentries = len(all_rows)
	data_list = []    
	for row in all_rows:
		data_list.append((row[0], row[1], row[2] ))

	description = ''
	report = ArtifactHtmlReport('Aggregate Dictionary Scalars')
	report.start_artifact_report(report_folder, 'Scalars', description)
	report.add_script()
	data_headers = ('Day','Key','Value' )     
	report.write_artifact_data_table(data_headers, data_list, file_found)
	report.end_artifact_report()
	
	tsvname = 'Agg Dict Scalars'
	tsv(report_folder, data_headers, data_list, tsvname)
	