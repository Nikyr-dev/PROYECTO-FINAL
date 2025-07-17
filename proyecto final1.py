import sqlite3
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

DATABASE_NAME = 'inventario.db'

def connect_db():
    """Establece conexión con la base de datos."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table():
    """Crea la tabla 'productos' si no existe."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_product():
    """Registra un nuevo producto en la base de datos."""
    print(Fore.CYAN + "\n--- Registrar Nuevo Producto ---")
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción del producto: ")
    while True:
        try:
            cantidad = int(input("Cantidad disponible: "))
            break
        except ValueError:
            print(Fore.RED + "Error: La cantidad debe ser un número entero.")
    while True:
        try:
            precio = float(input("Precio del producto: "))
            break
        except ValueError:
            print(Fore.RED + "Error: El precio debe ser un número.")
    categoria = input("Categoría del producto: ")

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria))
        conn.commit()
        print(Fore.GREEN + "Producto registrado exitosamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al registrar el producto: {e}")
    finally:
        conn.close()

def view_products():
    """Muestra todos los productos registrados en la base de datos."""
    print(Fore.CYAN + "\n--- Productos Registrados ---")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()

    if not productos:
        print(Fore.YELLOW + "No hay productos registrados.")
        return

    # Imprimir encabezados de tabla
    print(Fore.BLUE + f"{'ID':<5} {'Nombre':<20} {'Descripción':<30} {'Cantidad':<10} {'Precio':<10} {'Categoría':<15}")
    print(Fore.BLUE + "-" * 95)
    for prod in productos:
        print(f"{prod[0]:<5} {prod[1]:<20} {prod[2]:<30} {prod[3]:<10} {prod[4]:<10.2f} {prod[5]:<15}")
    conn.close()

def update_product():
    """Actualiza los datos de un producto existente por su ID."""
    print(Fore.CYAN + "\n--- Actualizar Producto ---")
    product_id = input("Ingrese el ID del producto a actualizar: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    if not product:
        print(Fore.RED + "Producto no encontrado.")
        conn.close()
        return

    print(Fore.YELLOW + "Producto encontrado. Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")
    nombre = input(f"Nombre ({product[1]}): ") or product[1]
    descripcion = input(f"Descripción ({product[2]}): ") or product[2]
    
    while True:
        cantidad_input = input(f"Cantidad ({product[3]}): ")
        if cantidad_input == "":
            cantidad = product[3]
            break
        try:
            cantidad = int(cantidad_input)
            break
        except ValueError:
            print(Fore.RED + "Error: La cantidad debe ser un número entero.")

    while True:
        precio_input = input(f"Precio ({product[4]}): ")
        if precio_input == "":
            precio = product[4]
            break
        try:
            precio = float(precio_input)
            break
        except ValueError:
            print(Fore.RED + "Error: El precio debe ser un número.")
            
    categoria = input(f"Categoría ({product[5]}): ") or product[5]

    try:
        cursor.execute('''
            UPDATE productos
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
            WHERE id = ?
        ''', (nombre, descripcion, cantidad, precio, categoria, product_id))
        conn.commit()
        print(Fore.GREEN + "Producto actualizado exitosamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al actualizar el producto: {e}")
    finally:
        conn.close()

def delete_product():
    """Elimina un producto de la base de datos por su ID."""
    print(Fore.CYAN + "\n--- Eliminar Producto ---")
    product_id = input("Ingrese el ID del producto a eliminar: ")

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM productos WHERE id = ?', (product_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print(Fore.GREEN + "Producto eliminado exitosamente.")
        else:
            print(Fore.RED + "Producto no encontrado.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al eliminar el producto: {e}")
    finally:
        conn.close()

def search_product():
    """Busca productos por ID, nombre o categoría."""
    print(Fore.CYAN + "\n--- Buscar Producto ---")
    print("Opciones de búsqueda:")
    print("1. Buscar por ID")
    print("2. Buscar por Nombre")
    print("3. Buscar por Categoría")
    
    choice = input("Ingrese su opción (1-3): ")
    conn = connect_db()
    cursor = conn.cursor()
    productos = []

    if choice == '1':
        product_id = input("Ingrese el ID del producto: ")
        cursor.execute('SELECT * FROM productos WHERE id = ?', (product_id,))
        productos = cursor.fetchall()
    elif choice == '2':
        product_name = input("Ingrese el nombre del producto: ")
        cursor.execute('SELECT * FROM productos WHERE nombre LIKE ?', ('%' + product_name + '%',))
        productos = cursor.fetchall()
    elif choice == '3':
        product_category = input("Ingrese la categoría del producto: ")
        cursor.execute('SELECT * FROM productos WHERE categoria LIKE ?', ('%' + product_category + '%',))
        productos = cursor.fetchall()
    else:
        print(Fore.RED + "Opción inválida.")
        conn.close()
        return

    if not productos:
        print(Fore.YELLOW + "No se encontraron productos con los criterios de búsqueda.")
        return

    print(Fore.BLUE + f"{'ID':<5} {'Nombre':<20} {'Descripción':<30} {'Cantidad':<10} {'Precio':<10} {'Categoría':<15}")
    print(Fore.BLUE + "-" * 95)
    for prod in productos:
        print(f"{prod[0]:<5} {prod[1]:<20} {prod[2]:<30} {prod[3]:<10} {prod[4]:<10.2f} {prod[5]:<15}")
    conn.close()

def low_stock_report():
    """Genera un reporte de productos con cantidad igual o inferior a un límite."""
    print(Fore.CYAN + "\n--- Reporte de Productos con Bajo Stock ---")
    while True:
        try:
            limit = int(input("Ingrese el límite de cantidad (mostrar productos con cantidad <= este límite): "))
            break
        except ValueError:
            print(Fore.RED + "Error: El límite debe ser un número entero.")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE cantidad <= ?', (limit,))
    productos = cursor.fetchall()

    if not productos:
        print(Fore.YELLOW + "No hay productos con cantidad igual o inferior al límite especificado.")
        return

    print(Fore.BLUE + f"{'ID':<5} {'Nombre':<20} {'Descripción':<30} {'Cantidad':<10} {'Precio':<10} {'Categoría':<15}")
    print(Fore.BLUE + "-" * 95)
    for prod in productos:
        print(f"{prod[0]:<5} {prod[1]:<20} {prod[2]:<30} {prod[3]:<10} {prod[4]:<10.2f} {prod[5]:<15}")
    conn.close()

def main_menu():
    """Muestra el menú principal de la aplicación."""
    create_table() # Asegura que la tabla exista al iniciar la aplicación

    while True:
        print(Fore.YELLOW + Style.BRIGHT + "\n--- MENÚ PRINCIPAL DE INVENTARIO ---")
        print(Fore.GREEN + "1. Registrar nuevo producto")
        print(Fore.GREEN + "2. Visualizar productos")
        print(Fore.GREEN + "3. Actualizar producto")
        print(Fore.GREEN + "4. Eliminar producto")
        print(Fore.GREEN + "5. Buscar producto")
        print(Fore.GREEN + "6. Reporte de bajo stock")
        print(Fore.RED + "7. Salir")

        choice = input(Fore.YELLOW + "Seleccione una opción: ")

        if choice == '1':
            register_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            update_product()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            search_product()
        elif choice == '6':
            low_stock_report()
        elif choice == '7':
            print(Fore.MAGENTA + "¡Gracias por usar la aplicación de inventario! Hasta luego.")
            break
        else:
            print(Fore.RED + "Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main_menu()