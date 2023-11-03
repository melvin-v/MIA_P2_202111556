from Tools.load import Fcreate_file, Fwrite_displacement, Winit_size, Fread_displacement
from Tools.utilities import get_sizeB
from Structures.MBR import MBR
from Structures.Partition import Partition
from Structures.EBR import EBR
import os
from Global.Global import mounted_partitions

def mkdisk(args):
   size_bytes = get_sizeB(int(args.size),args.unit)
   directorio = os.path.dirname(args.path)
   try:
        os.makedirs(directorio)
   except:
        pass
   if (Fcreate_file(args.path)): return
   Crrfile = open(args.path, "rb+")
   Winit_size(Crrfile,size_bytes)
   NewMBR = MBR()
   NewMBR.set_infomation(size_bytes,args.fit)
   Fwrite_displacement(Crrfile,0,NewMBR)
   Crrfile.close()
   return "Disco creado exitosamente en: " + args.path

def rmdisk(args):
   try:
      os.remove(args.path)
      return "Disco eliminado exitosamente en: " + args.path
   except:
      return "No se pudo eliminar el disco con ruta: " + args.path

def fdisk(comando):
   tipo = comando.type
   ruta = comando.path
   size = int(comando.size)
   if size < 1:
     return 'El tamaño de la partición debe ser mayor a 0 para el disco: ' + ruta
   if not os.path.exists(ruta):
     return 'El disco no existe en: ' + ruta
   mbr = MBR()
   archivo = open(ruta, 'rb+')
   Fread_displacement(archivo, 0, mbr)
   archivo.close()
   
    

   for element in mbr.partitions:
      if element.name.decode() == comando.name:
         return 'Ya existe una partición con ese nombre en: ' + ruta
   flag = True
   for element in mbr.partitions:
      if element.size == -1:
         flag = False
         break
   if flag and tipo != 'l':
      return 'No se pueden crear mas particiones en el disco: ' + ruta

   size_bytes = get_sizeB(int(comando.size),comando.unit)
   if tipo == 'p':
      tamanio = len(MBR().doSerialize())
      for element in mbr.partitions:
         if element.size == -1:
            if (size_bytes + tamanio) > mbr.size:
               return 'No hay espacio suficiente para crear la partición en: ' + ruta
            element.set_infomation('1', tipo, comando.fit, tamanio, size_bytes, comando.name)
            archivo = open(ruta, 'rb+')
            Fwrite_displacement(archivo, 0, mbr)
            archivo.close()
            return 'Partición primaria creada exitosamente en: ' + ruta
            
         tamanio += element.size

   elif tipo == 'e':
      tamanio = len(MBR().doSerialize())
      for element in mbr.partitions:
         if element.size == -1:
            if element.type.decode() == 'e':
               return 'Ya existe una partición extendida en: ' + ruta
            if (size_bytes + tamanio) > mbr.size:
               return 'No hay espacio suficiente para crear la partición en: ' + ruta
            element.set_infomation('1', tipo, comando.fit, tamanio, size_bytes, comando.name)
            archivo = open(ruta, 'rb+')
            Fwrite_displacement(archivo, 0, mbr)
            archivo.close()
            ebr = EBR()
            ebr.start = tamanio
            archivo = open(ruta, 'rb+')
            Fwrite_displacement(archivo, tamanio, ebr)
            archivo.close()
            return 'Partición extendida creada exitosamente en: ' + ruta
            
         tamanio += element.size
   
   elif tipo == 'l':
      flag = True
      for element in mbr.partitions:
         if element.type.decode() == 'e':
            flag = False
            break
      if flag:
         return 'No existe una partición extendida en: ' + ruta
      #Cargamos EBR inicial
      ebr = EBR()
      tamanioExentdida = 0
      for element in mbr.partitions:
         if element.type.decode() == 'e':
            tamanioExentdida = size_bytes
            archivo = open(ruta, 'rb+')
            Fread_displacement(archivo, element.start, ebr)
            archivo.close()
            break
      #Buscamos el ultimo EBR y sumamos espacios
      tamanio = ebr.start
      while ebr.next != -1:
         tamanio += ebr.s
         if ebr.name.decode() == comando.name:
            return 'Ya existe una partición con ese nombre en: ' + ruta
         Fread_displacement(archivo, tamanio, ebr)
      #Verificamos que haya espacio suficiente
      if (size_bytes + tamanio) < (tamanioExentdida):
         return 'No hay espacio suficiente para crear la partición en: ' + ruta
      #Creamos la particion
      ebr.set_infomation('1', comando.fit, tamanio, size_bytes, -1, comando.name)
      archivo = open(ruta, 'rb+')
      Fwrite_displacement(archivo, tamanio, ebr)
      archivo.close()
      return 'Partición lógica creada exitosamente en: ' + ruta
         
def mount(args):
   crr_mbr = MBR()
   Crrfile = open(args.path, "rb+")
   Fread_displacement(Crrfile,0,crr_mbr)
   
   crr_partition = Partition()
   for partition in crr_mbr.partitions:
      if partition.size != -1:
         if partition.name.decode() == args.name:
            crr_partition = partition

   if crr_partition.size != -1:
      # F = XX +  NUM PARTITION + NOMBRE DISCO donde XX es el numero de carnet
      nombre_archivo = os.path.splitext(os.path.basename(args.path))[0]
      index = 1
      id = "56" + str(index) + nombre_archivo
      #for data in mounted_partitions:
      #   if data[0] == id:
      #     index += 1
      #      id = "56" + str(index) + nombre_archivo 
      for data in mounted_partitions:
         if data[2] == args.path and data[1].name == crr_partition.name:
            return "La particion ya esta montada"

      flag = True
      while flag:
         flag = False
         for data in mounted_partitions:
            if data[0] == id:
               index += 1
               id = "56" + str(index) + nombre_archivo 
               flag = True
               break

      temp = [id,crr_partition ,args.path, crr_mbr]
      mounted_partitions.append(temp)
   else:
      return "La particion no existe"
   Crrfile.close()
   return "Particion montada exitosamente" + " id: " + str(id)
