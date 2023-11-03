import argparse
import shlex 

def parse_args(command_line=None):
    parser = argparse.ArgumentParser(description='Parseo de comandos en la terminal de un sistema de archivos')
    subparsers = parser.add_subparsers(title='Comandos disponibles', dest='command')

    
    # ***************************************** ADMINISTRACIÓN DE DISCOS *********************************************
    
    #MKDISK
    make_disk = subparsers.add_parser('mkdisk', )
    make_disk.add_argument('-size', required=True, type=int)
    make_disk.add_argument('-path', required=True)
    make_disk.add_argument('-fit', required=False, choices=["bf", "ff", "wf"], default="ff")
    make_disk.add_argument('-unit', required=False, choices=["k", "m"], default="M")

    #RMDISK
    remove_disk = subparsers.add_parser('rmdisk')
    remove_disk.add_argument('-path', required=True)
    
    #FDISK 
    fdisk = subparsers.add_parser('fdisk')
    fdisk.add_argument('-size', required=True)
    fdisk.add_argument('-unit',choices=["b","k", "m"] , default="K")
    fdisk.add_argument('-path', required=True)
    fdisk.add_argument('-name', required=True)
    fdisk.add_argument('-type', required=False, choices=["p", "e", "l"])
    fdisk.add_argument('-fit', required=False, choices=["bf", "ff", "wf"], default="WF")
    
    #MOUNT
    fdisk = subparsers.add_parser('mount')
    fdisk.add_argument('-path', required=True)
    fdisk.add_argument('-name', required=True)


    # ***************************************** ADMINISTRACIÓN DEL SISTEMA DE ARCHIVOS ********************************

    #MKFS
    fdisk = subparsers.add_parser('mkfs')
    fdisk.add_argument('-id', required=True)
    fdisk.add_argument('-type', required=True, choices=["full"])

    # ***************************************** ADMINISTRACIÓN DE USUARIOS *******************************************

    #LOGIN
    fdisk = subparsers.add_parser('login')
    fdisk.add_argument('-user', required=True)
    fdisk.add_argument('-pass', required=True)
    fdisk.add_argument('-id', required=True)

    #LOGOUT
    fdisk = subparsers.add_parser('logout')

    #MKGRP
    fdisk = subparsers.add_parser('mkgrp')
    fdisk.add_argument('-name', required=True)

    #RMGRP
    fdisk = subparsers.add_parser('rmgrp')
    fdisk.add_argument('-name', required=True)

    #MKUSR
    fdisk = subparsers.add_parser('mkusr')
    fdisk.add_argument('-user', required=True)
    fdisk.add_argument('-pass', required=True)
    fdisk.add_argument('-grp', required=True)

    #RMUSR
    fdisk = subparsers.add_parser('rmusr')
    fdisk.add_argument('-user', required=True)

    # ***************************************** ADMINISTRACIÓN DE CARPETAS Y ARCHIVOS *******************************************

    #MKFILE
    fdisk = subparsers.add_parser('mkfile')
    fdisk.add_argument('-path', required=True)
    fdisk.add_argument('-size', required=True)
    fdisk.add_argument('-cont', required=True)
    fdisk.add_argument('-r', required=False)

    #MKDIR
    fdisk = subparsers.add_parser('mkdir')
    fdisk.add_argument('-path', required=True)
    fdisk.add_argument('-r', required=False)

    #REP
    fdisk = subparsers.add_parser('rep')
    fdisk.add_argument('-name', required=True, choices=["mbr", "disk"])
    fdisk.add_argument('-path', required=True)
    fdisk.add_argument('-id', required=True)
    fdisk.add_argument('-ruta', required=False)

    
    if command_line is not None:
        return parser.parse_args(shlex.split(command_line))
    else:
        return parser.parse_args()
    

if __name__ == '__main__':
    command_line = input('Ingrese comando: ')
    try:
        args = parse_args(command_line)
    except:
        print('Sintaxis o tokens invalidos')
