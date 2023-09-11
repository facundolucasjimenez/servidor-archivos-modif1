import os
import socket
import sys
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

def main():
    pass

if __name__ == '__main__':
    main()
#------------------------------------------------

#------------------------------------------------
#pedir ARCHIVO graba en cliente
#------------------------------------------------
def pedirArchivo_Ventana(titulo,conn,opcion):
       ventana01 = tk.Toplevel()
       ventana01.geometry('700x500')
       ventana01.title(titulo)
       ventana01.configure(background='blue')
       #textbox
       textbox = tk.Text(ventana01,height=20,width=75)
       #combobox
       Combo00 = listaDirectorioLinux(ventana01)
       if opcion == "Modifica":
          #Label
          label01 = tk.Label(ventana01,text="Seleccione archivo del directorio del Servidor luego Reciba Modifique y Envie",bg="blue",fg="white")
          label01.place(x=10,y=10)
          #Button
          BT_Recibir = tk.Button(ventana01,text='Recibir',command=lambda: RecibirModificar(ventana01,textbox,"1|",Combo00.get(),conn))
          BT_Enviar   = tk.Button(ventana01,text='Enviar',command=lambda: RecibirModificarEnviar(ventana01,textbox,"3|",Combo00.get(),conn))
          BT_Recibir.place(x=440,y=10)
          BT_Enviar.place(x=540,y=10)
       else:
          #Label
          label01 = tk.Label(ventana01,text="Seleccione archivo del directorio del Servidor y luego Confirme-->",bg="blue",fg="white")
          label01.place(x=10,y=10)
          #Button
          BT_Confirma = tk.Button(ventana01,text='Confirme',command=lambda: enviarRecibirGraba(ventana01,textbox,"1|",Combo00.get(),conn))
          BT_Confirma.place(x=370,y=10)


#---------- ADICIÓN ######
                
def borrarRegistros(titulo,conn):
       ventana01 = tk.Toplevel()
       ventana01.geometry('700x500')
       ventana01.title(titulo)
       ventana01.configure(background='red')
       #textbox
       textbox = tk.Text(ventana01,height=13,width=75)
       #combobox, por ahora del directorio general, por hacer despues solo de archivos compatibles
       Combo00 = listaArchivosConRegistros(ventana01)
       
       #combobox ID de registros
       Combo01 = listaID(ventana01)
       
       #Label
       label01 = tk.Label(ventana01,text="Seleccione archivo y cargue IDs, luego seleccione ID y confirme-->",bg="blue",fg="white")
       label01.place(x=10,y=10)
       # botón carga de ID
       BT_CargarID = tk.Button(ventana01,text='Cargar IDs',command=lambda: cargarID(textbox,"1|",Combo00.get(),conn))
       BT_CargarID.place(x=440,y=10)
       # botón borrar
       BT_Borrar = tk.Button(ventana01,text='Borrar',command=lambda: borrarRegistro(ventana01,"4",Combo01.get(),conn,Combo00.get()))
       BT_Borrar.place(x=540,y=10)
       
#---------- FIN ADICIÓN ######

def listaDirectorioLinux(ventana01):
       Combo00=ttk.Combobox(ventana01,width=60)
       Combo00.place(x=10,y=40)
       conn.send("1|directorio".encode())
       contenidoArchivo = conn.recv(8192)
       Combo00['values'] = contenidoArchivo
       return Combo00


#---------- ADICIÓN ######     
def listaArchivosConRegistros(ventana01):
       Combo00=ttk.Combobox(ventana01,width=60)
       Combo00.place(x=10,y=40)
       conn.send("1|directorio".encode())
       contenidoArchivo = conn.recv(8192)
       Combo00['values'] = contenidoArchivo # cambiar para filtrar y dejar solo archivos con registros
       return Combo00

def listaID(ventana01):
       global Combo01        # global para no tener que pasar como parametro en cargarID
       Combo01=ttk.Combobox(ventana01,width=60)
       Combo01.place(x=10,y=120)
       return Combo01
       
def cargarID(textbox,operacion,nombreArchivo,conn):
       textbox.place(x=0,y=100)
       textbox.delete("1.0","end") # borra todo, tipo clear
       textbox.pack(expand=True)
       conn.send((operacion+nombreArchivo).encode())
       contenidoArchivo = conn.recv(8192)
       
       lista1 = contenidoArchivo.splitlines()
       listaID = list()
       
       i=0
       for j in lista1:
            i+=1
            aux = str(i)+" "+lista1[i-1].decode('utf-8')
            textbox.insert('end',aux+"\n")
            listaID.append(str(i))
       
       Combo01['values'] = listaID
       
def borrarRegistro(ventana01,operacion,idRegistro,conn,nombreArchivo):
       conn.send((operacion+"|"+nombreArchivo+"|"+idRegistro).encode())

#---------- FIN ADICIÓN ######

def RecibirModificar(ventana01,textbox,operacion,nombreArchivo,conn):
       textbox.delete("1.0","end")
       textbox.pack(expand=True)
       #send  operacion+nombreArchivo
       conn.send((operacion+nombreArchivo).encode())
       #recive archivo
       contenidoArchivo = conn.recv(8192)
       textbox.insert('end', contenidoArchivo)

def RecibirModificarEnviar(ventana01,textbox,operacion,nombreArchivo,conn):
       conn.send((operacion+nombreArchivo+"|"+textbox.get("1.0","end")).encode()) # OPERACION YA TIENE EL | ATRÁS, POR ESO NO LO PONE ACÁ

def enviarRecibirGraba(ventana01,textbox,operacion,nombreArchivo,conn):
       textbox.delete("1.0","end") # borra todo, tipo clear
       textbox.pack(expand=True)
       #send  operacion+nombreArchivo
       conn.send((operacion+nombreArchivo).encode()) # envia a socket un string como "1|aaa.txt". operacion es el "1|"
       #receive archivo
       contenidoArchivo = conn.recv(8192)
       textbox.insert('end', contenidoArchivo)
       mi_lista = []
       mi_lista = nombreArchivo.split("|")
       f = open(mi_lista[0], "w")
       f.write(contenidoArchivo.decode())
       f.close()


#---------------------------------------------------------
#ENVIAR ARCHIVO de windows a linux
#---------------------------------------------------------
def enviarArchivo_Ventana(titulo,conn):
       ventana01 = tk.Toplevel()
       ventana01.geometry('700x500')
       ventana01.title(titulo)
       ventana01.configure(background='blue')
       #Label
       label01 = tk.Label(ventana01,text="Enviar archivo: ",bg="blue",fg="white")
       label01.place(x=10,y=10)
       #combobox
       Combo00 = listaDirectorioWindows(ventana01)
       #textbox
       textbox = tk.Text(ventana01,height=20,width=75)
       #Button
       BT_Confirma = tk.Button(ventana01,text='Confirma',command=lambda: enviarArchivo(ventana01,textbox,"2|",Combo00.get(),conn))
       BT_Confirma.place(x=250,y=10)

def listaDirectorioWindows(ventana01):
       Combo00=ttk.Combobox(ventana01,width=60)
       Combo00.place(x=10,y=40)
       nombre_carpeta = "C:\\Users\\fl\\Downloads\\clienteArchivos"
       contenido = os.listdir(nombre_carpeta)
       mi_lista = []
       for elemento in contenido:
               ruta_completa = os.path.join(nombre_carpeta, elemento)
               print(elemento, ruta_completa, sep=', ')  # mostramos el nombre del elemento y la ruta completa
               #mi_lista.append(ruta_completa)
               mi_lista.append(elemento)
       Combo00['values'] = mi_lista
       return Combo00

def enviarArchivo(ventana01,textbox,operacion,nombreArchivo,conn):
       textbox.delete("1.0","end")
       textbox.pack(expand=True)
       archivo = open(nombreArchivo)
       contenidoArchivo = archivo.read()
       archivo.close()
       textbox.insert('end', contenidoArchivo)
       conn.send((operacion+nombreArchivo+"|"+contenidoArchivo).encode())

#---------------------------------------------------------
#TERMINAR
#---------------------------------------------------------
def Terminar(ventana,conn):
       mensaje = "0|Terminar"
       conn.send(mensaje.encode())
       conn.close()
       ventana.destroy()
       sys.exit(0)
#---------------------------------------------------------


#---------------------------------------------------------
# main
#---------------------------------------------------------
ventana = tk.Tk()
ventana.title("Menu")
ventana.geometry('400x400')
ventana.configure(background='blue')
#--conexion al servidor
conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
#--Poner el IP correspondiente a su equipo
servidor = "192.168.56.102"
puerto = 8888
try:
    conn.connect((servidor, puerto))
except socket.error as message:
            label01 = tk.Label(ventana,text="Falló la conexión con el servidor {} por el puerto {}".format(servidor, puerto),bg="blue",fg="white")
            #print("Falló la conexión con el servidor {} por el puerto {}".format(servidor, puerto))
            print(message)
            sys.exit()
label01 = tk.Label(ventana,text="Conexión con el servidor {} por el puerto {}".format(servidor, puerto),bg="blue",fg="white")
#print("Conexión con el servidor {} por el puerto {}".format(servidor, puerto))
label01.pack(fill=tk.X)
#-------------------------------------------------
bot01=tk.Button(ventana,text='Pedir Archivo al Servidor',fg='blue',command=lambda: pedirArchivo_Ventana('Pedir Archivo al Servidor',conn,"NoModifica"))
bot01.place(x=10,y=20)
bot01=tk.Button(ventana,text='Enviar Archivo al Servidor',fg='blue',command=lambda: enviarArchivo_Ventana('Enviar Archivo al Servidor',conn))
bot01.place(x=10,y=50)
bot01=tk.Button(ventana,text='Modificar Archivo del Servidor en Carga y Descarga',fg='blue',command=lambda: pedirArchivo_Ventana('Modificar Archivo Carga y Descarga en Servidor',conn,"Modifica"))
bot01.place(x=10,y=80)
bot00=tk.Button(ventana,text='Terminar',fg='blue',command=lambda: Terminar(ventana,conn))
bot00.place(x=10,y=160)

#---------- ADICIÓN ######
bot01=tk.Button(ventana,text='Borrar un registro en un archivo',fg='blue',command=lambda: borrarRegistros('Borrar registro de un archivo en servidor',conn))
bot01.place(x=10,y=110)
#---------- FIN ADICIÓN ######

ventana.mainloop()
#---------------------------------
