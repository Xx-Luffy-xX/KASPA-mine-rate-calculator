import subprocess, locale, datetime
import os
from sys import exit
import sys

hour_to_sec = 3600;
day_to_sec = hour_to_sec * 24;
locale.setlocale(locale.LC_ALL, 'en_US')

KASPACTL = str(os.path.join(os.getcwd(),"kaspactl"))
win_flag = 0
if not os.path.isfile(KASPACTL):
    KASPACTL = str(os.path.join(os.getcwd(),"kaspactl.exe"))
    win_flag = 1
    if not os.path.isfile(KASPACTL):
        print("kaspactl was not found, make sure you run the program from the same directory as kaspactl.")
        exit()

if len(sys.argv)>1 and str(sys.argv[1])=="-s":
    node_ip = str(sys.argv[2])
    KASPACTL = KASPACTL + " -s " + node_ip
else:
    try:
        if win_flag==1:
            subprocess.check_call(KASPACTL + " GetSelectedTipHash > $null", shell=True)
        else:
            subprocess.check_call(KASPACTL + " GetSelectedTipHash>/dev/null 2>&1", shell=True)
    except subprocess.CalledProcessError:
      print("\nNODE NOT FOUND!\nIf kaspad is running on other machine in the network please enter the machine's local IP:")
      node_ip = input()
      KASPACTL = KASPACTL + " -s " + node_ip
  
output = subprocess.Popen(KASPACTL + " GetSelectedTipHash", stdout=subprocess.PIPE, shell=True).communicate()

try:
    hash = str(output).split("selectedTipHash")[1].split('"')[2]
except:
    print("Couldn't connect to network...")
    exit()
    
output = subprocess.Popen(KASPACTL + " EstimateNetworkHashesPerSecond 3000 " + hash, stdout=subprocess.PIPE, shell=True).communicate()
global_hashrate = int(str(output).split('"')[5])
print("\nNode found!\nGlobal hash rate is found to be:\t", locale.format_string("%.2f", global_hashrate/10**9, grouping=True), "GH/s")

print("\nWhat is the local hash rate estimation in Khash/s?\n(you can enter the collective sum of several mining machines. For example: 24000 + 6000 + 256)")
local_hashrate = ""
while type(local_hashrate) == str:
    hrate_str = input()
    try:
        hrate_str = hrate_str.split("+")
        hrate_str = [int(i) for i in hrate_str]
        local_hashrate = sum(hrate_str)
    except:
        print("\nThe local hash rate must be an integer! What is it then?")
local_hashrate = int(local_hashrate * 1e3)

print("\nDefault settings use 1 block/sec and 500KAS block reward.\nDo you want to use the default settings? [y/n]\n(if not you can reset them manually)")
def_set = input()
while def_set not in ["y","n"]:
    print("\nOnly 'y' or 'n' are acceptable... y/n?")
    def_set = input()

global_blockrate = 1
block_reward = 500
if def_set == "n":
    print("\nWhat is the global block rate [1/s]? (unless devs changed it, use '1')")
    global_blockrate = ""
    while type(global_blockrate) == str:
        brate_str = input()
        try:
            global_blockrate = float(brate_str)
        except:
            print("\nThe global block rate must be a number! What is it then?")

    print("\nWhat is the block reward [KAS]? (unless devs changed it, use '500')")
    block_reward = ""
    while type(block_reward) == str:
        breward_str = input()
        try:
            block_reward = float(breward_str)
        except:
            print("\nThe block reward must be a number! What is it then?")

local_blockrate = local_hashrate / global_hashrate * global_blockrate
local_kasrate = local_blockrate * block_reward

sec_for_block = int(1 / local_blockrate)
minutes, seconds = divmod(sec_for_block, 60)
hr, minutes = divmod(minutes, 60)
if hr != 0 and minutes != 1:
    time_for_block = "%d:%02d [h:m]" % (hr, minutes)
else:
    time_for_block = "%d:%02d:%02d [h:m:s]" % (hr, minutes, seconds)

print(
"\n\n ***********************\n",
"* Mining Estimations: *\n",
"***********************\n",
"\n",
"On average, you should find a block every ", time_for_block, " hours.\n",
"This translates to:\n\n",
"%.2f" %(local_blockrate * hour_to_sec), " Blocks/hour\t==>\t",
"%.2f" %(local_blockrate * day_to_sec), " Blocks/day\n",
"%.2f" %(local_kasrate * hour_to_sec), " KAS/hour\t==>\t",
"%.2f" %(local_kasrate * day_to_sec), " KAS/day\n",
"\n"
)
      
input("Press enter to proceed...")
