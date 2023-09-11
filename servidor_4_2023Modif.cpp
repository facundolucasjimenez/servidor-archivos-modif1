// compilar con c++ servidor_4_2023 

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>
#include <dirent.h>
#include <iostream>
#include <string.h>
#include <unistd.h> 
#include <fcntl.h> 
#include <sys/stat.h> 

#include <fstream>
#include <vector>

#define PUERTO 8888

using namespace std;

int generarArchivoDirectorio(void);
int mostrarArchivoDirectorio(void);

void crearSocket(char *);
void atenderCliente(int);

void enviarArchivo(int idsockCli ,char * nombreArchivo);

int menu(void) ;

vector<string> split(string s, string delimiter);

int main(int argc, char * argv[])
{
    int opcion ;
    while((opcion = menu()) != 0)
    {
	    switch(opcion)
	    {
		case 1:
                   if (generarArchivoDirectorio() == -1)
                     cout << "Error generar Archivo Directorio \n" ; 
		   break;
		case 2:
                   if (mostrarArchivoDirectorio() == -1)
                     cout << "Error mostrar Archivo Directorio \n" ; 
		   break;
		case 3:
		    crearSocket(argv[1]);
		    break;
                case 7:
		    system("clear");
		    break;
		
	    }
    }
    exit(0);
}


int generarArchivoDirectorio(void)
{
    int fdd = open("directorio",O_CREAT|O_WRONLY|O_TRUNC,0666);
    if ( fdd == -1 )
         return -1;
    else
    {
      struct dirent * ent;        
      DIR * DIRdirec = opendir(".");
      if (DIRdirec == NULL)
         return -1;
      else       
      {
           struct stat sta ;
    	   while ((ent = readdir(DIRdirec)) != NULL)
	   {
                  if (stat(ent->d_name,&sta) == -1)
                       return -1;
                  else  
                   {
                     char registro[1024];
                     strcpy(registro,ent->d_name);
                     strcat(registro,"|");
                     char sizestr[16] ;
                     sprintf(sizestr,"%d",sta.st_size);
                     strcat(registro,sizestr);
                     strcat(registro,"\n\0");
                     write(fdd,registro,strlen(registro)) ;
                   }             
           }
         closedir(DIRdirec);
         close(fdd);
         return 0 ;
        }
    }
    return 0 ;
}

int mostrarArchivoDirectorio(void)
{
    int fdd = open("directorio",O_RDONLY);
    if ( fdd == -1 )
         return -1;
    else
    {
         char registro[1024];
         int nb ;            
         while ((nb=read(fdd,registro,1024)) > 0)
	   {
               registro[nb]='\0';
               cout << registro << endl ;
           }
         close(fdd);
    }
    return 0 ;
}


//------------------------------------------------------------------
void crearSocket(char * ip)
{
    struct sockaddr_in sockSer,sockCli;
    int idsockSer,idsockCli;
    
    idsockSer = socket(AF_INET,SOCK_STREAM,0);
    cout << "Identificador socket servidor: " << idsockSer <<endl;

    sockSer.sin_family = AF_INET;
    sockSer.sin_port = htons(PUERTO);
    sockSer.sin_addr.s_addr = inet_addr(ip);
    memset(sockSer.sin_zero,0,8);

    socklen_t lensock = sizeof(struct sockaddr_in);
    if (bind(idsockSer,(struct sockaddr*)&sockSer,lensock) == -1)
	{
           cout << "Error al ejecutar la funcion bind()" << endl ;
           exit(-1) ;
	}

    if (listen(idsockSer,5) == -1)
       {
           cout << "Error al ejecutar la funcion listen()" << endl ;
           exit(-1) ;
	}

    system("clear");
    cout << "Escuchando solicitudes..." << endl;
    while(1)
    {
        idsockCli = accept(idsockSer,(struct sockaddr *)&sockCli , &lensock);
        cout << "La IP del cliente es: " << inet_ntoa(sockCli.sin_addr) << endl;
        if ( idsockCli == -1 )
            cout << "Error al ejecutar la funcion accept()" << endl ;
        else
        {
            pid_t pid = fork() ;
            if ( pid == 0 )
             {
               atenderCliente(idsockCli) ;
               exit(0) ;
             }
        }
    }
}

vector<string> split(string s, string delimiter){
	size_t pos_start = 0, pos_end, delim_len = delimiter.length();
	string token;
	vector<string> res;
	
	while((pos_end=s.find(delimiter,pos_start)) != std::string::npos){
		token = s.substr (pos_start, pos_end - pos_start);
		pos_start = pos_end + delim_len;
		res.push_back(token);
	}
	
	res.push_back (s.substr (pos_start));
	return res;
}

void atenderCliente(int idsockCli)
{
  int salir = 1 ;
  do
   {
     char mensajeRecibido[1024];
     memset(mensajeRecibido,'\0',1024);
     ssize_t nb = recv(idsockCli,mensajeRecibido,1024,0);
     mensajeRecibido[nb] = '\0';
     cout << "Mensaje recibido del cliente " << mensajeRecibido << endl ;   
     switch(mensajeRecibido[0])
	   {
	      case '1' : 
		   {
		      char * nombreArchivo = strtok(mensajeRecibido,"|");
		      if (nombreArchivo != NULL )
		           nombreArchivo = strtok(NULL,"|");
		      enviarArchivo(idsockCli,nombreArchivo) ;
		      break;
		   }
              case '2' : 
		   {
		      char * operacion = strtok(mensajeRecibido,"|");
		      char * nombreArchivo = strtok(NULL,"|");
                      char * contenidoArchivo = strtok(NULL,"|");
                      //printf("Operacion %s\n",operacion);
                      //printf("Nombre archivo %s\n",nombreArchivo);
                      //printf("Contenido archivo %s\n",contenidoArchivo);
                      int fd = open(nombreArchivo,O_CREAT|O_WRONLY|O_TRUNC,0666);
                      write(fd,contenidoArchivo,strlen(contenidoArchivo));
                      close(fd);
		      break;
		   }
               case '3' : 
		   {
		      char * operacion = strtok(mensajeRecibido,"|");
		      char * nombreArchivo = strtok(NULL,"|");
                      char * tamanioArchivo=strtok(NULL,"|");
                      char * contenidoArchivo = strtok(NULL,"|");
                      printf("Operacion %s\n",operacion);
                      printf("Nombre archivo %s\n",nombreArchivo);
                      printf("Tamanio archivo %s\n",tamanioArchivo);
                      printf("Contenido archivo %s\n",contenidoArchivo);
                      int fd = open(nombreArchivo,O_CREAT|O_WRONLY|O_TRUNC,0666);
                      write(fd,contenidoArchivo,strlen(contenidoArchivo));
                      close(fd);
		      break;
		   }
	      case '4' :
	      	   {
	      	  	char * operacion = strtok(mensajeRecibido,"|");
		      char * nombreArchivo = strtok(NULL,"|");
                      char * tamanioArchivo=strtok(NULL,"|");
                      char * idABorrar = strtok(NULL,"|");
                      printf("Operacion %s\n",operacion);
                      printf("Nombre archivo %s\n",nombreArchivo);
                      printf("Tamanio archivo %s\n",tamanioArchivo);
                      printf("Id de registro a borrar %s\n\n\n",idABorrar);
                      
                      char todoElTexto[8192];
			memset(todoElTexto,'\0',8192);
			  int fd = open(nombreArchivo,O_RDONLY);
			  if (fd != -1)
			    {
			       int nb = read(fd,todoElTexto,8192);
			       todoElTexto[nb] = '\0';
			       cout << todoElTexto << endl ;
			    }
			    close(fd);
			    
			string todoElTextoString = todoElTexto;
			string delimiter = "\n";
			vector<string> vector1 = split(todoElTextoString, delimiter);
			vector<string> corregido;
			
			cout<<"\n"<<idABorrar<<"\n"<<*idABorrar<<"\n"<<endl;
			cout<<"\n"<<vector1.size()<<"\n"<<&idABorrar<<"\n"<<endl;
			
			for (int i=0; i<vector1.size(); i++){
				if ((i+1)!= atoi(idABorrar)){
					//cout<<i+1<<" es el i+1 y "<<*idABorrar<<" es el id a borrar"<<endl;
					corregido.push_back(vector1[i]);
				}
			}
			
			for (auto i:corregido) cout<<i<<endl;
			
			
			FILE * fp;
			fp = fopen (nombreArchivo,"w+");
			
			/*for (int i = 0; i<corregido.size(); i++){
				string stringAux = corregido[i];
				fprintf(fp,"%s",""+stringAux);
			}
			mal, "The format specifier "%s" expects a C-style null terminated
			string, not a std::string. --> usar solo tipo char* */ 
			
			for (int i = 0; i<corregido.size(); i++){
				if (i+1==corregido.size())
					fprintf(fp,"%s",corregido[i].c_str());
				else
					fprintf(fp,"%s\n",corregido[i].c_str());
			}
			
			fclose(fp);
			
	      	      break;
	      	   }
              case '0' : 
		   {
		     salir = 0 ; 
                     break;
		   }
	   }
    }while(salir);         
}

void enviarArchivo(int idsockCli , char * nombreArchivo)
{
  cout << " Enviando archivo " << nombreArchivo << " al cliente " << idsockCli << endl;
  char contenido[8192];
  memset(contenido,'\0',8192);
  int fd = open(nombreArchivo,O_RDONLY);
  if (fd != -1)
    {
       int nb = read(fd,contenido,8192);
       contenido[nb] = '\0';
       cout << contenido << endl ;
    }  
  else
    {
       strcpy(contenido,"Error: archivo no existe o problema en la conexion\0");  
    }
  send(idsockCli,contenido,strlen(contenido),0);
}

int menu(void)
{
    int opcion ;
    cout << " Menu Servidor de archivos 4-2023 " << endl;
    cout << " 1) crear archivo directorio      " << endl;
    cout << " 2) mostrar archivo directorio    " << endl;
    cout << " 3) crear iniciar socket          " << endl;   
    cout << " 4) ----------------------------- " << endl;   
    cout << " 7) limpiar pantalla              " <<endl;
    cout << " 0) apagar servidor               " <<endl;
    cout << "Ingresar opcion: " ;
    cin >> opcion;
    return opcion;
}
