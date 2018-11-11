import pandas as pd
import os
import fnmatch
from datetime import datetime, timedelta
import datetime

path = os.chdir('/users/victorolade/Box/Lead Gen - AARP')
filenames = os.listdir('.')
for file in filenames:
    if fnmatch.fnmatch(file,'*.xls') and fnmatch.fnmatch(file,'Lead_Gen_Summary_Report*'):
	    filedate = datetime.datetime.fromtimestamp(os.path.getctime(file))
	    fd_clean = filedate.strftime('%m-%d-%y')
	    no_ext = file[:-4]
	    new_name = no_ext + '_' + fd_clean + '.csv'
	    os.rename(file, new_name)
	    
        
        
