import urllib.request
import os

sources = [
    'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts',
    'http://hosts-file.net/ad_servers.txt',
    #'https://adaway.org/hosts.txt',
    'http://winhelp2002.mvps.org/hosts.txt',
]

# windows 10 telemetry 
custom_source = [
    'statsfe2.update.microsoft.com.akadns.net',
    'fe2.update.microsoft.com.akadns.net',
    's0.2mdn.net',
    'survey.watson.microsoft.com',
    'view.atdmt.com',
    'watson.microsoft.com',
    'watson.ppe.telemetry.microsoft.com',
    'vortex.data.microsoft.com',
    'vortex-win.data.microsoft.com',
    'telecommand.telemetry.microsoft.com',
    'telecommand.telemetry.microsoft.com.nsatc.net',
    'oca.telemetry.microsoft.com',
    'sqm.telemetry.microsoft.com',
    'sqm.telemetry.microsoft.com.nsatc.net',
    'watson.telemetry.microsoft.com',
    'watson.telemetry.microsoft.com.nsatc.net',
    'redir.metaservices.microsoft.com',
    'choice.microsoft.com',
    'choice.microsoft.com.nsatc.net',
    'wes.df.telemetry.microsoft.com',
    'services.wes.df.telemetry.microsoft.com',
    'sqm.df.telemetry.microsoft.com',
    'telemetry.microsoft.com',
    'telemetry.appex.bing.net',
    'telemetry.urs.microsoft.com',
    'settings-sandbox.data.microsoft.com',
    'watson.live.com',
    'statsfe2.ws.microsoft.com',
    'corpext.msitadfs.glbdns2.microsoft.com',
    'compatexchange.cloudapp.net',
    'a-0001.a-msedge.net',
    'sls.update.microsoft.com.akadns.net',
    'diagnostics.support.microsoft.com',
    'corp.sts.microsoft.com',
    'statsfe1.ws.microsoft.com',
    'feedback.windows.com',
    'feedback.microsoft-hohm.com',
    'feedback.search.microsoft.com',
    'rad.msn.com',
    'preview.msn.com',
    'ad.doubleclick.net',
    'ads.msn.com',
    'ads1.msads.net',
    'ads1.msn.com',
    'a.ads1.msn.com',
    'a.ads2.msn.com',
    'adnexus.net',
    'adnxs.com',
    'az361816.vo.msecnd.net',
    'az512334.vo.msecnd.net',
    'ssw.live.com',
    'ca.telemetry.microsoft.com',
    'i1.services.social.microsoft.com',
    'df.telemetry.microsoft.com',
    'reports.wes.df.telemetry.microsoft.com',
    'cs1.wpc.v0cdn.net',
    'vortex-sandbox.data.microsoft.com',
    'oca.telemetry.microsoft.com.nsatc.net',
    'pre.footprintpredict.com',
    'spynet2.microsoft.com',
    'spynetalt.microsoft.com',
    'fe3.delivery.dsp.mp.microsoft.com.nsatc.net',
    'cache.datamart.windows.com',
    'db3wns2011111.wns.windows.com',
    'settings-win.data.microsoft.com',
    'v10.vortex-win.data.microsoft.com',
    'win10.ipv6.microsoft.com',
    'ca.telemetry.microsoft.com',
    'i1.services.social.microsoft.com.nsatc.net',
    'msnbot-207-46-194-33.search.msn.com',
    'settings.data.microsof.com',
    'telecommand.telemetry.microsoft.com.nsatc.net',
]

final_list = []

def get_blocked_domains(myFile):   
    myFile = [x.strip() for x in myFile]
    myFile = [z for z in myFile if z != '' and z[0] != '#']
    myFile = [h.split()[1] for h in myFile if h.split()[0] in ['0.0.0.0', '127.0.0.1']]
    myFile = [x for x in myFile if x not in ['localhost', 'localhost.localdomain', 'locals']]
    return myFile

if os.name == 'nt':
    hosts_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
elif os.name == 'posix':
    hosts_path = '/etc/hosts'

print('[+] reading original hosts file')
with open(hosts_path, 'r') as host_file:
    original_list = host_file.readlines()
    original_list = get_blocked_domains(original_list)
    print('[+] ' + str(len(original_list)) + ' blocked domains found')
    final_list += original_list

for link in sources:
    print('[+] retrieving list from: ' + link)
    f = urllib.request.urlopen(link)
    myfile = f.readlines()
    myfile = [x.decode("utf-8") for x in myfile]
    myfile = get_blocked_domains(myfile)
    print('[+] ' + str(len(myfile)) + ' blocked domains found')
    f.close()
    final_list += myfile

final_list += custom_source
print('[+] removing duplicates and sorting')
final_list = sorted(list(set(final_list)))
print('[+] total domains count ' + str(len(final_list)))

print('[+] writing to file')
with open('hosts.txt', 'w') as l:
    l.write('''# Copyleft 2016 ildoc.it
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1             localhost

127.0.0.1 localhost
127.0.0.1 localhost.localdomain
127.0.0.1 local
255.255.255.255 broadcasthost
::1 localhost
fe80::1%lo0 localhost

# Custom host records are listed here.

''')
    l.write('\n'.join('127.0.0.1 ' + url for url in final_list))