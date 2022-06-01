import pyfiglet
import subprocess

def intro():
	#subprocess
	subprocess.call(["clear"])

	#variabili
	result2 = pyfiglet.figlet_format("eternalB", font="larry3d")

	#output
	print(result2)
	print("Welcome on EternalB")

def scan1():
    #variabili
	s = "Nmap scan report for "
	ipList = list()

	#subprocess
	p = subprocess.Popen(["sudo","nmap","-sP","192.168.69.0/24"], stdout=subprocess.PIPE).stdout
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
		vulnList.append((ip, checkVuln(ip)))
	print(vulnList)


def checkVuln(ip):
	#subprocess
	p = subprocess.Popen(["sudo","nmap","-p", "445", "--script", "smb-vuln-ms17-010", ip], stdout=subprocess.PIPE).stdout
	t = p.read().splitlines()
	
	#decode from byte to string
	t = [x.decode("utf-8") for x in t]
	
	#ciclo check ip
	for i in t:
		if "VULNERABLE" in i:
			return True
	return False


if __name__ == "__main__":
	intro()
	print("fine intro")
	iplist = scan1()
	print("fine scan1")
	#print(iplist)
	scan2(iplist)
	#print(checkVuln("192.168.69.1"))
	
