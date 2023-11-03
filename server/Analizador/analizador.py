import re
from Analizador.parser import parse_args
from Methods.admin_discos import mkdisk, rmdisk, fdisk, mount
from Methods.reportes import reportes


consola = ''
def analizador(data):
   global consola
   consola += '------ Analizando comandos ------\n'
   clonData = data

   for command in clonData:
      command = re.sub(r"[#][^\n]*", "", command)
      command = command.lower()
      if command == "": continue
      try:
         command = parse_args(command)
         consola += metodos(command) + "\n"
      except SystemExit as e: consola += 'Error al analizar comando\n'; print(e)
      except Exception as e: consola += str(e) + "\n"
   consola += '------ Fin de analisis de comandos ------\n'
   return consola
   

def metodos(comando):
   if comando.command == 'mkdisk':
      return mkdisk(comando)
   elif comando.command == 'rmdisk':
      return rmdisk(comando)
   elif comando.command == 'fdisk':
      return fdisk(comando)
   elif comando.command == 'mount':
      return mount(comando)
   elif comando.command == 'rep':
      return reportes(comando)




  

      
      
