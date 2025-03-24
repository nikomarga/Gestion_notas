import sys
users = []  # Lista de usuarios
courses = []  # Lista de cursos
logged_user = None  # Usuario en sesión
2
# 🔹 Registrar un usuario con rol (admin, profesor, estudiante)
def user_register():
    id = int(input("Ingrese su ID: "))
    name = input("Ingrese su nombre: ")
    last_name = input("Ingrese su apellido: ")
    password = input("Cree su contraseña: ")
    
    print("Seleccione el rol:")
    print("1. Administrador")
    print("2. Profesor")
    print("3. Estudiante")
    
    role_option = input("Seleccione una opción: ")
    roles = {"1": "admin", "2": "profesor", "3": "estudiante"}
    
    if role_option not in roles:
        print("Opción inválida. Registro cancelado.")
        return
    
    role = roles[role_option]

    users.append({
        "id": id,
        "name": name,
        "last_name": last_name,
        "password": password,
        "role": role,
        "courses": {}  # Diccionario de cursos y notas
    })
    print(f"Usuario {name} registrado exitosamente como {role}.")

# 🔹 Iniciar sesión
def user_login():
    global logged_user
    id = int(input("Ingrese su ID: "))
    password = input("Ingrese su contraseña: ")
    
    for user in users:
        if user["id"] == id and user["password"] == password:
            logged_user = user
            print(f"Bienvenido, {user['name']} ({user['role']})!")
            dashboard()
            return
    print("ID o contraseña incorrectos.")

# 🔹 Panel según el rol del usuario
def dashboard():
    while True:
        print("\nOpciones:")
        if logged_user["role"] == "admin":
            print("1. Crear curso")
            print("2. Asignar profesor a curso")
            print("3. Asignar estudiante a curso")
        elif logged_user["role"] == "profesor":
            print("4. Agregar notas a un curso")
        print("5. Ver notas")
        print("6. Cerrar sesión")
        
        option = input("Seleccione una opción: ")

        if option == "1" and logged_user["role"] == "admin":
            create_course()
        elif option == "2" and logged_user["role"] == "admin":
            assign_professor()
        elif option == "3" and logged_user["role"] == "admin":
            assign_student_to_course()
        elif option == "4" and logged_user["role"] == "profesor":
            add_note()
        elif option == "5":
            view_notes()
        elif option == "6":
            logout()
            break
        else:
            print("Opción inválida.")

# 🔹 Crear un curso (Administrador)
def create_course():
    course_name = input("Ingrese el nombre del curso: ")
    courses.append({"name": course_name, "professor": None, "students": {}, "notes": {}})
    print(f"Curso '{course_name}' creado exitosamente.")

# 🔹 Asignar profesor a un curso
def assign_professor():
    print("\nCursos disponibles:")
    for i, course in enumerate(courses):
        print(f"{i + 1}. {course['name']} - Profesor: {course['professor']}")

    choice = int(input("Seleccione el curso: ")) - 1
    professor_id = int(input("Ingrese el ID del profesor: "))

    for user in users:
        if user["id"] == professor_id and user["role"] == "profesor":
            courses[choice]["professor"] = user["name"]
            print(f"Profesor {user['name']} asignado a {courses[choice]['name']}.")
            return
    print("Profesor no encontrado.")

# 🔹 Asignar estudiante a un curso (Administrador)
def assign_student_to_course():
    print("\nCursos disponibles:")
    for i, course in enumerate(courses):
        print(f"{i + 1}. {course['name']} - Profesor: {course['professor']}")

    choice = int(input("Seleccione el curso: ")) - 1
    student_id = int(input("Ingrese el ID del estudiante: "))

    for user in users:
        if user["id"] == student_id and user["role"] == "estudiante":
            courses[choice]["students"][user["id"]] = user["name"]
            courses[choice]["notes"][user["id"]] = []
            print(f"Estudiante {user['name']} asignado a {courses[choice]['name']}.")
            return
    print("Estudiante no encontrado.")

# 🔹 Agregar notas a un curso (Profesor)
def add_note():
    print("\nCursos asignados:")
    assigned_courses = [course for course in courses if course["professor"] == logged_user["name"]]

    if not assigned_courses:
        print("No tienes cursos asignados.")
        return

    for i, course in enumerate(assigned_courses):
        print(f"{i + 1}. {course['name']}")

    choice = int(input("Seleccione el curso: ")) - 1
    course = assigned_courses[choice]

    if not course["students"]:
        print("No hay estudiantes inscritos en este curso.")
        return

    print("\nEstudiantes en el curso:")
    for student_id, student_name in course["students"].items():
        print(f"{student_id}: {student_name}")

    student_id = int(input("Ingrese el ID del estudiante para agregar una nota: "))

    if student_id not in course["students"]:
        print("Estudiante no encontrado en este curso.")
        return

    note = input(f"Ingrese la nota para {course['students'][student_id]}: ")
    course["notes"][student_id].append(note)

    print("Nota agregada exitosamente.")

# 🔹 Ver notas (Profesor o Estudiante)
def view_notes():
    print("\nNotas registradas:")
    if logged_user["role"] == "estudiante":
        for course in courses:
            if logged_user["id"] in course["students"]:
                print(f"Curso: {course['name']} - Notas: {course['notes'][logged_user['id']]}")
    elif logged_user["role"] == "profesor":
        for course in courses:
            if course["professor"] == logged_user["name"]:
                print(f"\nCurso: {course['name']}")
                for student_id, notes in course["notes"].items():
                    print(f"Estudiante {course['students'][student_id]}: {notes}")

 #Cerrar sesión
def logout():
    global logged_user
    print(f"Sesión cerrada para {logged_user['name']}.")
    logged_user = None

 #Menú principal
def main():
    while True:
        print("\n1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        
        option = input("Seleccione una opción: ")
        
        if option == "1":
            user_register()
        elif option == "2":
            user_login()
        elif option == "3":
            sys.exit() 
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()