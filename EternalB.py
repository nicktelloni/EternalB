import pyfiglet
import subprocess

def intro():
	#subprocess
	subprocess.call(["clear"])

	#variabili
	result2 = pyfiglet.figlet_format('eternalB', font='larry3d')

	#output
	print(result2)
	print("Welcome on EternalB")

def scan1():
    #variabili
	s = 'Nmap scan report for '
	ipL = list()

	#subprocess
	p = subprocess.Popen(["sudo","nmap","-sP","192.168.69.0/24"], stdout=subprocess.PIPE).stdout
	l = p.read().splitlines()

	#decode from byte to string
	l=[x.decode('utf-8') for x in l]

	#rimuovi primo e ultimo elemento
	del l[0]
	del l[-1]

	#ciclo stampa ip
	for i, x in enumerate(l):
		if s in x:
			l[i] = x.replace(s,'')
			#print(l[i])
			ipL.append(l[i])
	return ipL


if __name__ == '__main__':
	intro()
	#scan1()
	iplist = scan1()
	print("main")
	print(iplist)
