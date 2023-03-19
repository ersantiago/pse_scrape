#!/home/xinyx/anaconda3/bin/python
from bs4 import BeautifulSoup
import re
import requests
import pygsheets

def write(input,output_file):
    encode_input = input.encode('ascii', 'ignore')
    with open(output_file, 'wb') as f:
        f.write(encode_input)
        f.close()

# Load pygsheets
path_cred = '/mnt/share/scripts/admin_scripts/api/IT-DA-9a643fc39003.json'
stxd_sheet = 'https://docs.google.com/spreadsheets/d/1au3cvGiRtNvi8SR28yc9p9YK7m15Ad5lZj3-oGtDEVQ/edit#gid=1270897057'

gc = pygsheets.authorize(service_file=path_cred)
wks = gc.open_by_url(stxd_sheet).worksheet_by_title('Raw_Data')

stklist_p = '/mnt/share/scripts/admin_scripts/misc/all_cmpy'
stklist = open(stklist_p, 'r').read().splitlines()
pse_tablefile = open('/mnt/share/scripts/admin_scripts/misc/pse_gg.txt', 'w')

#===================== Data from pse ==========================#
header = ["symb", "dtFY", "dtQ", "utFY", "utQ", "eFYp", "eFYc", "cy3", "py3", "cytd", "pytd"]
print("".join(word.ljust(11) for word in header))
header_print = "\t".join(header)
pse_tablefile.write(header_print + '\n')

full_list = []

for cmpy in stklist:
    symb, id1, id2 = cmpy.split()
    stxlnk = 'http://edge.pse.com.ph/companyPage/financial_reports_view.do?cmpy_id=' + id1

    try:
        # get requests
        gg = requests.get(stxlnk)
        ggtext = gg.text

        # regexes
        rgxdtFY = re.compile(r'For the fiscal year ended : (.*)<br>')
        rgxdtQ = re.compile(r'For the period ended : (.*)<br>')
        rgxunits = re.compile(r'Currency\(and units, if applicable\) : (.*)</p>')
        #rgxFYprev =
        #rgxFYcurrent =
        #rgxQytd =
        rgxEps = re.compile(r'<th>Earnings/\(Loss\) Per Share \(Diluted\)</th>(.*?)</tr>', re.DOTALL)
        #rgxeFYc =
        #rgxeQytd =
        rgxtrim = re.compile(r'alignR">(.*?)</td>')

        # Parse Data
        dtFY = rgxdtFY.findall(ggtext)[0]
        dtQ = rgxdtQ.findall(ggtext)[0]
        utFY, utQ = rgxunits.findall(ggtext)
        rweFY = rgxEps.findall(ggtext)[0].strip()
        rweQtd = rgxEps.findall(ggtext)[1].strip()
        eFYc, eFYp = rgxtrim.findall(rweFY)
        cy3, py3, cytd, pytd = rgxtrim.findall(rweQtd)
        results = [symb, dtFY, dtQ, utFY, utQ, eFYp, eFYc, cy3, py3, cytd, pytd]
        print("".join(word.ljust(11) for word in results))
        out_inv = "\t".join(results)
    except:
        out_inv = 'Unable to parse data for ' + symb
        dtFY, dtQ, utFY, utQ, eFYp, eFYc, cy3, py3, cytd, pytd = 0,0,0,0,0,0,0,0,0,0
        results = [symb, 'nodata', dtQ, utFY, utQ, eFYp, eFYc, cy3, py3, cytd, pytd]
    pse_tablefile.write(out_inv + '\n')
    full_list.append(results)
wks.update_values('L2',full_list)
pse_tablefile.close()