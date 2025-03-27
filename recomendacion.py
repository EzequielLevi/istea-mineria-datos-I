import csv

def pausa():
    input("\tPresione enter para continuar")

class Libro:
    """
    Esta clase representa un libro con su título, autor, género y puntuación.
    """
    def __init__(self, titulo, autor, genero, puntuacion):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.puntuacion = puntuacion
#----------------------------------------------------------------------------------------
def cargar_libros_desde_csv(archivo='libros.csv'):
    """
    Esta función sirve para cargar los libros que se encuentran en el archivo libros.csv
    Se llena la lista_libros y de esta forma es como se realizan las consultas de 
    buscar libros por su genero y la recomendación del libro mejor puntuado
    """
    lista_libros = []
    try:
        with open(archivo, mode='r', encoding='utf-8') as file:
            lector = csv.reader(file)
            next(lector, None)  # Saltea cabecera sin error si archivo vacío
            
            for fila in lector:
                try:
                    if len(fila) >= 4:  # Verificar que la fila tenga todos los campos
                        titulo = fila[0].strip('"').strip().capitalize()
                        autor = fila[1].strip('"').strip().capitalize()
                        genero = fila[2].strip('"').strip().capitalize()
                        puntuacion = float(fila[3])
                        lista_libros.append(Libro(titulo, autor, genero, puntuacion))
                except (ValueError, IndexError) as e:
                    print(f"Error procesando fila {fila}: {str(e)}")
                    continue
                    
        print(f"Se cargaron {len(lista_libros)} libros desde {archivo}")
        
    except FileNotFoundError:
        print(f"Archivo {archivo} no encontrado. Se creará uno nuevo.")
    except csv.Error as e:
        print(f"Error en formato CSV: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
    
    return lista_libros
#----------------------------------------------------------------------------------------
def guardar_libros(lista_libros, archivo='libros.csv', modo='w'): 
    """
    Esta función sirve para guardar los libros que se agregan desde la función agregar_libro()
    en el archivo libros.csv
    """
    try:
        with open(archivo, mode=modo, newline='', encoding='utf-8') as file:
            writer = csv.writer(file, lineterminator='\n')  # Usar lineterminator para evitar líneas en blanco
            if modo == 'w':
                writer.writerow(['Título', 'Autor', 'Género', 'Puntuación'])
            for libro in lista_libros:
                writer.writerow([libro.titulo, libro.autor, libro.genero, libro.puntuacion])
        print(f"Libros guardados correctamente en {archivo}")
    except Exception as e:
        print(f"Error inesperado al guardar los libros: {e}")
#----------------------------------------------------------------------------------------
def agregar_libro(lista_libros): 
    """
    Esta función sirve para agregar un libro nuevo que se guarda en el archivo libros.csv
    """
    print("\n" + "#"*50)
    print("AGREGAR NUEVO LIBRO".center(50))
    print("#"*50)
    while True:

        titulo = input("Ingrese el título del libro: ").strip()
        while titulo == "":
            print("ERROR: El título solo debe contener letras y espacios.")
            titulo = input("Por favor, ingrese el título del libro: ").strip().capitalize()

        autor = input("Ingrese el autor del libro: ").strip().capitalize() 
        while autor == "" or not autor.replace(" ", "").isalpha():
            print("ERROR al ingresar el autor")
            autor = input("Por favor, ingrese el autor del libro: ").strip().capitalize()

        genero = input("Ingrese el género del libro: ").strip().capitalize()
        while genero == "" or not genero.replace(" ", "").isalpha():
            print("ERROR al ingresar el género")
            genero = input("Por favor, ingrese el género del libro: ").strip().capitalize()

        while True:
            try:
                puntuacion = float(input("Ingrese la puntuación (0-5): "))
                if 0 <= puntuacion <= 5:
                    break
                print("La puntuación debe estar entre 0 y 5")
            except ValueError:
                print("¡Debe ingresar un número válido!")
        
        nuevo_libro = Libro(titulo, autor, genero, puntuacion)
        lista_libros.append(nuevo_libro)
        
        try:
            guardar_libros([nuevo_libro], modo='a')
            print("\n¡Libro agregado y guardado exitosamente!")
            print("-"*50)
            print(f"Título: {nuevo_libro.titulo}")
            print(f"Autor: {nuevo_libro.autor}")
            print(f"Género: {nuevo_libro.genero}")
            print(f"Puntuación: {nuevo_libro.puntuacion}")
        except Exception as e:
            print(f"\nError al guardar el libro: {e}")
            print("El libro se agregó a la lista actual pero no se pudo guardar en el archivo.")
        
        pausa()
        return lista_libros
#----------------------------------------------------------------------------------------
def buscar_genero(lista_libros):
    """
    Esta función recorre fila por fila del archivo csv buscando coincidencia en el genero propio de los libros
    con el ingreso de los datos por el usuario en la busqueda. Devuelve las filas que coinciden con el ingreso
    de datos del usuario.
    """
    print("\n" + "#"*50)
    print("BUSCAR POR GÉNERO".center(50))
    print("#"*50)
    
    genero = input("Ingrese el género que está buscando: ")
    while genero == "" or genero.isspace():
            genero = input("Ingrese el nombre del genero: ").strip().capitalize()
    libros_encontrados = [libro for libro in lista_libros if libro.genero.capitalize() == genero.capitalize()]

    if libros_encontrados:
        print(f"\nLibros encontrados del género {genero}:")
        print("-"*50)
        for libro in libros_encontrados:
            print(f"Título: {libro.titulo}")
            print(f"Autor: {libro.autor}")
            print(f"Puntuación: {libro.puntuacion}")
            print("-"*50)
    else:
        print(f"No se encontraron libros del género {genero}")
    
#----------------------------------------------------------------------------------------
def recomendar_libro(lista_libros):
    """
    Esta función recorre fila por fila del archivo csv buscando coincidencia en el genero propio de los libros
    con el ingreso de los datos por el usuario en la busqueda. Devuelve el libro con mejor puntuacion
    """
    genero = input("Ingrese el género que está buscando: ")
    libros_del_genero = [libro for libro in lista_libros if libro.genero.capitalize() == genero.capitalize()]
    
    if libros_del_genero:
        libro_recomendado = max(libros_del_genero, key=lambda x: x.puntuacion)
        print("\nLibro recomendado:")
        print("-"*50)
        print(f"Título: {libro_recomendado.titulo}")
        print(f"Autor: {libro_recomendado.autor}")
        print(f"Puntuación: {libro_recomendado.puntuacion}")
        print("-"*50)
    else:
        print(f"No se encontraron libros del género {genero}")
    
#----------------------------------------------------------------------------------------
def menu():
    print("1. Agregar un libro ")
    print("2. Buscar libro por genero ")
    print("3. Recomendar libro con mejor puntuacion")
    print("4. Salir")

def main():
    
    lista_libros = cargar_libros_desde_csv(archivo='libros.csv')

    while True:
        menu()
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            agregar_libro(lista_libros)
        elif opcion == "2":
            buscar_genero(lista_libros)
        elif opcion == "3":
            recomendar_libro(lista_libros)
        elif opcion == "4":            
            print("""Saliendo del programa... \nHasta luego""")
            break
        else:
            print("Opción equivocada. Intentelo nuevamente.")

if __name__ == "__main__":
    
    main()