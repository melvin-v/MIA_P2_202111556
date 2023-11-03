from Global.Global import mounted_partitions, counter
from Structures.EBR import EBR
from Tools.utilities import coding_str, get_sizeB
from Tools.load import Fread_displacement
import graphviz
import os

output_path = '/home/melvin/archivos/reports/'
def reportes(args):
    global counter
    if args.name == 'mbr':
        dot_code = """
                    digraph D {
                    subgraph cluster_0 {
                    bgcolor="#68d9e2"
                    node [style="rounded" style=filled];
                    node_A [shape=record label="MBR
                    """
        for element in mounted_partitions:
            if element[0] == args.id:
                total = len(element[3].doSerialize())
                for partition in element[3].partitions:
                    if partition.size != -1 and partition.type.decode() == 'p':
                        dot_code += f"|{partition.name.decode()}"
                        total += partition.size
                    elif partition.size != -1 and partition.type.decode() == 'e':
                        dot_code += "|{Extendida|{"
                              #Cargamos EBR inicial
                        ebr = EBR()
                        archivo = open(element[2], 'rb+')
                        Fread_displacement(archivo, partition.start, ebr)
                        archivo.close()
                        total += partition.size
                        while True:
                            dot_code +=  f"EBR|{ebr.part_name.decode()}"
                            if ebr.next == -1:
                                break
                            archivo = open(element[2], 'rb+')
                            Fread_displacement(archivo, ebr.next, ebr)
                            archivo.close()
                        dot_code += "}}"
                    else:
                        break
                break
        else:
            return "Error: No se reconoce el nombre del reporte"
        if (element[3].size - total) > 0:
            dot_code += f"|Libre"
        dot_code += """
                    "];
                    }
                    }
                    """
        graph = graphviz.Source(dot_code, format='jpg')
        graph.render(args.path.split('.')[0])
        counter += 1
        eliminar_archivos_no_jpg(output_path)
        return "Reporte generado exitosamente"

    if args.name == 'disk':
        dot_code = """
                    digraph G {
                    
                    a0 [shape=none label=<
                    <TABLE cellspacing="10" cellpadding="10" style="rounded" bgcolor="red">
                    
                    <TR>
                    <TD bgcolor="yellow">REPORTE MBR</TD>
                    </TR>
  
                    """
        for element in mounted_partitions:
            if element[0] == args.id:
                mbr = element[3]
                dot_code += f"""
                                <TR>
                                <TD bgcolor="yellow">MBR tamano</TD>
                                <TD bgcolor="yellow">{mbr.size}</TD>
                                </TR>
                            """
                dot_code += f"""
                                <TR>
                                <TD bgcolor="yellow">MBR tamano</TD>
                                <TD bgcolor="yellow">{mbr.date_creation.decode()}</TD>
                                </TR>
                            """
                
                dot_code += f"""
                                <TR>
                                <TD bgcolor="yellow">DISK signature</TD>
                                <TD bgcolor="yellow">{mbr.asignature}</TD>
                                </TR>
                            """
                index = 1
                for element in mbr.partitions:
                    if element.size != -1:
                        dot_code += f"""
                             <TR>
                            <TD bgcolor="purple">Particion {index}</TD>
                            </TR>
  
                                    """
                    index += 1
        dot_code += """

                        </TABLE>>];

                        }
                    """
        graph = graphviz.Source(dot_code, format='jpg')
        graph.render(args.path.split('.')[0])
        counter += 1
        eliminar_archivos_no_jpg(output_path)
        return "Reporte generado exitosamente"

def eliminar_archivos_no_jpg(carpeta):
    try:
        for archivo in os.listdir(carpeta):
            ruta_completa = os.path.join(carpeta, archivo)
            if not archivo.lower().endswith('.jpg'):
                if os.path.isfile(ruta_completa):
                    os.remove(ruta_completa)
                    print(f"Eliminado: {archivo}")
                else:
                    print(f"No es un archivo: {archivo}")
    except Exception as e:
        print(f"Error: {e}")

# Llama a la función con la ruta de la carpeta
carpeta = "/ruta/a/tu/carpeta"
eliminar_archivos_no_jpg(carpeta)

        