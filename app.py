from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
# =====================================
# CONEXION DEL PGADMIN
conexion = psycopg2.connect(
    host="dpg-d8tksn9kh4rs73fembrg-a",
    database="colegio_yunguyo",
    user="colegio_yunguyo_user",
    password="Hu6pct5HvIMVCfZO29flKW9aIgPrLkxU",
    port="5432"
)
# =====================================
# PAGINA PRINCIPAL
#======================================
@app.route('/')
def inicio():
    return render_template('inicio.html')
# =====================================
# LOGIN ESTUDIANTE
#=====================================
@app.route('/login_estudiante')
def login_estudiante():
    return render_template('login_estudiante.html')

@app.route('/validar_estudiante', methods=['POST'])
def validar_estudiante():
    ci = request.form['ci']
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT *
        FROM estudiante
        WHERE ci = %s
    """, (ci,))
    estudiante = cursor.fetchone()
    cursor.close()
    if estudiante:
        return redirect(
            '/panel_estudiante/' +
            str(estudiante[0])
        )
    return "CI no encontrado"
# =====================================
# PANEL ESTUDIANTE
#======================================
@app.route('/panel_estudiante/<int:id_estudiante>')
def panel_estudiante(id_estudiante):
    cursor = conexion.cursor()

    # =========================
    # DATOS ESTUDIANTE
    # =========================
    cursor.execute("""
        SELECT
            e.nombre,
            e.apellido,
            e.ci,
            c.grado,
            c.paralelo,
            e.fecha_ingreso
        FROM estudiante e
        JOIN curso c ON e.id_curso = c.id_curso
        WHERE e.id_estudiante = %s
    """, (id_estudiante,))
    estudiante = cursor.fetchone()

    # =========================
    # MATERIAS + PROFESOR
    # =========================
    cursor.execute("""
        SELECT
            m.nombre,
            p.nombre,
            p.apellido
        FROM estudiante e
        JOIN curso c ON e.id_curso = c.id_curso
        JOIN profesor_materia pm ON c.id_curso = pm.id_curso
        JOIN materia m ON pm.id_materia = m.id_materia
        JOIN profesor p ON pm.id_profesor = p.id_profesor
        WHERE e.id_estudiante = %s
        ORDER BY m.nombre
    """, (id_estudiante,))
    materias = cursor.fetchall()

    # =========================
    # NOTAS EXAMEN
    # =========================
    cursor.execute("""
        SELECT
            m.nombre,
            nt.nota,
            nt.trimestre
        FROM nota_trimestre nt
        JOIN materia m ON nt.id_materia = m.id_materia
        WHERE nt.id_estudiante = %s
    """, (id_estudiante,))
    notas = cursor.fetchall()

    notas_1 = [n for n in notas if n[2] == 1]
    notas_2 = [n for n in notas if n[2] == 2]
    notas_3 = [n for n in notas if n[2] == 3]

    # =========================
    # PRÁCTICAS
    # =========================
    cursor.execute("""
        SELECT
            m.nombre,
            p.titulo,
            np.nota,
            p.trimestre
        FROM nota_practica np
        JOIN practica p ON np.id_practica = p.id_practica
        JOIN materia m ON p.id_materia = m.id_materia
        WHERE np.id_estudiante = %s
    """, (id_estudiante,))
    practicas = cursor.fetchall()

    practicas_1 = [p for p in practicas if p[3] == 1]
    practicas_2 = [p for p in practicas if p[3] == 2]
    practicas_3 = [p for p in practicas if p[3] == 3]

    # =========================
    # 🔥 1RA EVALUACIÓN (EXAMEN + PRÁCTICA)
    # =========================
    notas_dict_1 = {}

    for n in notas_1:
        materia = n[0]
        notas_dict_1[materia] = {"examen": n[1], "practica": 0}

    for p in practicas_1:
        materia = p[0]
        if materia in notas_dict_1:
            notas_dict_1[materia]["practica"] = p[2]
        else:
            notas_dict_1[materia] = {"examen": 0, "practica": p[2]}

    final_1 = [
        (m, d["examen"], d["practica"], d["examen"] + d["practica"])
        for m, d in notas_dict_1.items()
    ]

    # =========================
    # 🔥 2DA EVALUACIÓN
    # =========================
    notas_dict_2 = {}

    for n in notas_2:
        materia = n[0]
        notas_dict_2[materia] = {"examen": n[1], "practica": 0}

    for p in practicas_2:
        materia = p[0]
        if materia in notas_dict_2:
            notas_dict_2[materia]["practica"] = p[2]
        else:
            notas_dict_2[materia] = {"examen": 0, "practica": p[2]}

    final_2 = [
        (m, d["examen"], d["practica"], d["examen"] + d["practica"])
        for m, d in notas_dict_2.items()
    ]

    # =========================
    # 🔥 3RA EVALUACIÓN
    # =========================
    notas_dict_3 = {}

    for n in notas_3:
        materia = n[0]
        notas_dict_3[materia] = {"examen": n[1], "practica": 0}

    for p in practicas_3:
        materia = p[0]
        if materia in notas_dict_3:
            notas_dict_3[materia]["practica"] = p[2]
        else:
            notas_dict_3[materia] = {"examen": 0, "practica": p[2]}

    final_3 = [
        (m, d["examen"], d["practica"], d["examen"] + d["practica"])
        for m, d in notas_dict_3.items()
    ]
    # =========================
    # PROMEDIO GENERAL
    # =========================
    cursor.execute("""
        SELECT AVG(nota)
        FROM nota_trimestre
        WHERE id_estudiante = %s
    """, (id_estudiante,))
    promedio = cursor.fetchone()[0]

    if promedio is not None:
        promedio = round(float(promedio), 2)

    estado = "SIN NOTAS"
    if promedio is not None:
        estado = "APROBADO" if promedio >= 51 else "REPROBADO"

    cursor.close()

    return render_template(
        'panel_estudiante.html',
        estudiante=estudiante,
        materias=materias,
        notas_2=notas_2,
        notas_3=notas_3,
        promedio=promedio,
        estado=estado,
        final_1=final_1
    )
# =====================================
# LOGIN PROFESOR
#======================================
@app.route('/login_profesor')
def login_profesor():
    return render_template('login_profesor.html')
@app.route('/validar_profesor', methods=['POST'])
def validar_profesor():
    ci = request.form['ci']
    password = request.form['password']
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT *
        FROM profesor
        WHERE ci=%s
        AND password=%s
    """, (ci, password))
    profesor = cursor.fetchone()
    cursor.close()
    if profesor:
        return redirect(
            '/panel_profesor/' +
            str(profesor[0])
        )
    return "Credenciales incorrectas"
# =====================================
# PANEL PROFESOR
#======================================

@app.route('/panel_profesor/<int:id_profesor>')
def panel_profesor(id_profesor):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            nombre,
            apellido
        FROM profesor
        WHERE id_profesor=%s
    """, (id_profesor,))
    profesor = cursor.fetchone()
    cursor.close()
    return render_template(
    'panel_profesor.html',
    profesor=profesor,
    id_profesor=id_profesor)
#======================================
# Registrar Nota
#======================================
@app.route('/registrar_notas/<int:id_profesor>')
def registrar_notas(id_profesor):

    cursor = conexion.cursor()

    # Verificar permiso del director
    cursor.execute("""
        SELECT habilitado
        FROM permiso_notas
        WHERE id_profesor = %s
    """, (id_profesor,))

    permiso = cursor.fetchone()

    if not permiso or permiso[0] == False:

        cursor.close()

        return f"""
        <h1>No tiene autorización del Director
        para modificar notas.</h1>

        <a href="/panel_profesor/{id_profesor}">
            Volver
        </a>
        """

    # CURSOS DEL PROFESOR
    cursor.execute("""
        SELECT DISTINCT
            c.id_curso,
            c.grado,
            c.paralelo
        FROM curso c
        JOIN profesor_materia pm
            ON c.id_curso = pm.id_curso
        WHERE pm.id_profesor = %s
        ORDER BY
            c.grado,
            c.paralelo
    """, (id_profesor,))

    cursos = cursor.fetchall()

    # ESTUDIANTES DEL PROFESOR
    cursor.execute("""
        SELECT
            e.id_estudiante,
            e.nombre,
            e.apellido,
            c.id_curso,
            c.grado,
            c.paralelo
        FROM estudiante e
        JOIN curso c
            ON e.id_curso = c.id_curso
        JOIN profesor_materia pm
            ON c.id_curso = pm.id_curso
        WHERE pm.id_profesor = %s
        ORDER BY
            c.grado,
            c.paralelo,
            e.apellido,
            e.nombre
    """, (id_profesor,))

    estudiantes = cursor.fetchall()

    # MATERIAS DEL PROFESOR
    cursor.execute("""
        SELECT DISTINCT
            m.id_materia,
            m.nombre
        FROM materia m
        JOIN profesor_materia pm
            ON m.id_materia = pm.id_materia
        WHERE pm.id_profesor = %s
        ORDER BY m.nombre
    """, (id_profesor,))

    materias = cursor.fetchall()

    cursor.close()

    return render_template(
        'registrar_notas.html',
        cursos=cursos,
        estudiantes=estudiantes,
        materias=materias,
        id_profesor=id_profesor
    )
#======================================
# Guardar Nota
#======================================
@app.route('/guardar_nota', methods=['POST'])
def guardar_nota():

    id_estudiante = request.form['id_estudiante']
    id_materia = request.form['id_materia']
    trimestre = request.form['evaluacion']
    nota = request.form['nota']
    tipo_nota = request.form['tipo_nota']

    cursor = conexion.cursor()

    if tipo_nota == "examen":

        cursor.execute("""
            INSERT INTO nota_trimestre
            (
                id_estudiante,
                id_materia,
                trimestre,
                nota
            )
            VALUES
            (%s,%s,%s,%s)
        """,
        (
            id_estudiante,
            id_materia,
            trimestre,
            nota
        ))

    else:

        cursor.execute("""
            SELECT id_practica
            FROM practica
            WHERE id_materia = %s
            AND trimestre = %s
        """,
        (
            id_materia,
            trimestre
        ))

        practica = cursor.fetchone()

        if practica:

            cursor.execute("""
                INSERT INTO nota_practica
                (
                    id_practica,
                    id_estudiante,
                    nota
                )
                VALUES
                (%s,%s,%s)
            """,
            (
                practica[0],
                id_estudiante,
                nota
            ))

        else:

            cursor.close()

            return """
            <h1>No existe una práctica creada para esa materia y evaluación.</h1>

            <a href="javascript:history.back()">
                Volver
            </a>
            """

    conexion.commit()

    cursor.close()

    return """
    <h1>Nota registrada correctamente</h1>

    <a href="javascript:history.back()">
        Volver
    </a>
    """
# ==========================================
# MATERIAS DEL PROFESOR 
# ==========================================
@app.route('/ver_materias/<int:id_profesor>')
def ver_materias(id_profesor):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            m.nombre,
            c.grado,
            c.paralelo
        FROM profesor_materia pm
        JOIN materia m
        ON pm.id_materia = m.id_materia
        JOIN curso c
        ON pm.id_curso = c.id_curso
        WHERE pm.id_profesor = %s
    """, (id_profesor,))
    materias = cursor.fetchall()
    cursor.close()
    return render_template(
        'ver_materias.html',
        materias=materias
    )
# ==========================================
# ESTUDIANTES DEL PROFESOR
#===========================================
@app.route('/ver_estudiantes_profesor/<int:id_profesor>')
def ver_estudiantes_profesor(id_profesor):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT DISTINCT
            e.nombre,
            e.apellido,
            c.grado,
            c.paralelo
        FROM estudiante e
        JOIN curso c
            ON e.id_curso = c.id_curso
        JOIN profesor_materia pm
            ON c.id_curso = pm.id_curso
        WHERE pm.id_profesor = %s
        ORDER BY
            c.grado,
            c.paralelo,
            e.apellido,
            e.nombre
    """, (id_profesor,))
    datos = cursor.fetchall()
    cursor.close()
    cursos = {}
    for nombre, apellido, grado, paralelo in datos:
        curso = f"{grado} {paralelo}"
        if curso not in cursos:
            cursos[curso] = []
        cursos[curso].append((apellido, nombre))
    return render_template(
        'ver_estudiantes_profesor.html',
        cursos=cursos
    )
# ==========================================
# DELEGADOS Y CODELEGADOS
#===========================================
@app.route('/ver_representantes/<int:id_profesor>')
def ver_representantes(id_profesor):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            c.grado,
            c.paralelo,
            e.nombre,
            e.apellido,
            r.cargo
        FROM representante r
        JOIN estudiante e
        ON r.id_estudiante = e.id_estudiante
        JOIN curso c
        ON e.id_curso = c.id_curso
        JOIN profesor_materia pm
        ON c.id_curso = pm.id_curso
        WHERE pm.id_profesor = %s
        ORDER BY c.paralelo
    """, (id_profesor,))
    representantes = cursor.fetchall()
    cursor.close()
    return render_template(
        'representantes.html',
        representantes=representantes
    )

# =====================================
# LOGIN DIRECTOR
#=====================================
@app.route('/login_director')
def login_director():
    return render_template('login_director.html')

@app.route('/validar_director', methods=['POST'])
def validar_director():
    ci = request.form['ci']
    password = request.form['password']
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT *
        FROM director
        WHERE ci=%s
        AND password=%s
    """, (ci, password))
    director = cursor.fetchone()
    cursor.close()
    if director:
        return redirect(
            '/panel_director/' +
            str(director[0])
        )
    return "Credenciales incorrectas"
#==============================
# PANEL DiRECTOR
#==============================
@app.route('/panel_director/<int:id_director>')
def panel_director(id_director):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            nombre,
            apellido
        FROM director
        WHERE id_director=%s
    """, (id_director,))
    director = cursor.fetchone()
    # Total estudiantes
    cursor.execute("""
        SELECT COUNT(*)
        FROM estudiante
    """)
    total_estudiantes = cursor.fetchone()[0]
    # Total profesores
    cursor.execute("""
        SELECT COUNT(*)
        FROM profesor
    """)
    total_profesores = cursor.fetchone()[0]
    cursor.close()
    return render_template(
        'panel_director.html',
        director=director,
        total_estudiantes=total_estudiantes,
        total_profesores=total_profesores
    )
#=========================
#PERMISOS 
#=========================
@app.route('/permisos_notas')
def permisos_notas():
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            p.id_profesor,
            p.nombre,
            p.apellido,
            pn.habilitado
        FROM profesor p
        JOIN permiso_notas pn
        ON p.id_profesor = pn.id_profesor
        ORDER BY p.id_profesor
    """)
    profesores = cursor.fetchall()
    cursor.close()
    return render_template(
        'permisos_notas.html',
        profesores=profesores
    )
#=========================
#CAMBIAR PERMISO 
#=========================
@app.route('/cambiar_permiso/<int:id_profesor>')
def cambiar_permiso(id_profesor):
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE permiso_notas
        SET habilitado = NOT habilitado
        WHERE id_profesor=%s
    """, (id_profesor,))
    conexion.commit()
    cursor.close()
    return redirect('/permisos_notas')
#=========================
#Ver Estudiantes 
#=========================
@app.route('/ver_estudiantes')
def ver_estudiantes():
    buscar = request.args.get('buscar', '')

    cursor = conexion.cursor()

    if buscar:
        cursor.execute("""
            SELECT
                e.id_estudiante,
                e.ci,
                e.nombre,
                e.apellido,
                c.grado,
                c.paralelo,
                e.fecha_ingreso
            FROM curso c
            LEFT JOIN estudiante e
                ON e.id_curso = c.id_curso
            WHERE e.ci LIKE %s OR e.ci IS NULL
            ORDER BY
                c.grado,
                c.paralelo,
                e.apellido,
                e.nombre
        """, ('%' + buscar + '%',))
    else:
        cursor.execute("""
            SELECT
                e.id_estudiante,
                e.ci,
                e.nombre,
                e.apellido,
                c.grado,
                c.paralelo,
                e.fecha_ingreso
            FROM curso c
            LEFT JOIN estudiante e
                ON e.id_curso = c.id_curso
            ORDER BY
                c.grado,
                c.paralelo,
                e.apellido,
                e.nombre
        """)

    datos = cursor.fetchall()
    cursor.close()

    cursos = {}

    for id_estudiante, ci, nombre, apellido, grado, paralelo, fecha_ingreso in datos:

        curso = f"{grado} {paralelo}"

        if curso not in cursos:
            cursos[curso] = []

        # si no hay estudiante, no lo metemos en lista
        if id_estudiante is not None:
            cursos[curso].append((id_estudiante, ci, apellido, nombre, fecha_ingreso))

    return render_template('ver_estudiantes.html', cursos=cursos)

#=========================
#Ver Promedios (lo ve el director)
#=========================
@app.route('/ver_promedios')
def ver_promedios():
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            e.id_estudiante,
            e.nombre,
            e.apellido,
            c.grado,
            c.paralelo,
            COALESCE(ROUND(AVG(n.nota),2), 0) AS promedio
        FROM estudiante e
        JOIN curso c
            ON e.id_curso = c.id_curso
        LEFT JOIN nota_trimestre n
            ON e.id_estudiante = n.id_estudiante
        GROUP BY
            e.id_estudiante,
            e.nombre,
            e.apellido,
            c.grado,
            c.paralelo
        ORDER BY
            c.grado,
            c.paralelo,
            e.apellido,
            e.nombre
    """)
    datos = cursor.fetchall()
    cursor.close()
    cursos = {}
    for id_estudiante, nombre, apellido, grado, paralelo, promedio in datos:
        curso = f"{grado} {paralelo}"
        if curso not in cursos:
            cursos[curso] = []
        cursos[curso].append(
            (nombre, apellido, promedio)
        )
    return render_template(
        'ver_promedios.html',
        cursos=cursos
    )
#=========================
#Ver Aprobados y Reprobados 
#=========================
@app.route('/ver_aprobados')
def ver_aprobados():
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            e.id_estudiante,
            e.nombre,
            e.apellido,
            c.grado,
            c.paralelo,
            COALESCE(ROUND(AVG(n.nota),2), 0) AS promedio,
            CASE
                WHEN AVG(n.nota) >= 51 THEN 'APROBADO'
                WHEN AVG(n.nota) IS NULL THEN 'SIN NOTAS'
                ELSE 'REPROBADO'
            END AS estado
        FROM estudiante e
        JOIN curso c
            ON e.id_curso = c.id_curso
        LEFT JOIN nota_trimestre n
            ON e.id_estudiante = n.id_estudiante
        GROUP BY
            e.id_estudiante,
            e.nombre,
            e.apellido,
            c.grado,
            c.paralelo
        ORDER BY
            c.grado,
            c.paralelo,
            e.apellido,
            e.nombre
    """)
    datos = cursor.fetchall()
    cursor.close()
    cursos = {}
    for id_est, nombre, apellido, grado, paralelo, promedio, estado in datos:
        curso = f"{grado} {paralelo}"
        if curso not in cursos:
            cursos[curso] = []
        cursos[curso].append(
            (nombre, apellido, promedio, estado)
        )
    return render_template(
        'ver_aprobados.html',
        cursos=cursos
    )
# =====================================
# FORMULARIO AGREGAR ESTUDIANTE 
# =====================================
@app.route('/agregar_estudiante')
def agregar_estudiante():
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            id_curso,
            grado,
            paralelo
        FROM curso
        ORDER BY grado, paralelo
    """)
    cursos = cursor.fetchall()
    cursor.close()
    return render_template(
        'agregar_estudiante.html',
        cursos=cursos
    )
# =====================================
# GUARDAR ESTUDIANTE
# =====================================
@app.route('/guardar_estudiante', methods=['POST'])
def guardar_estudiante():

    ci = request.form['ci']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    password = request.form['password']
    id_curso = request.form['id_curso']
    fecha_ingreso = request.form['fecha_ingreso']

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO estudiante
        (
            ci,
            nombre,
            apellido,
            password,
            id_curso,
            fecha_ingreso
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)
    """,
    (
        ci,
        nombre,
        apellido,
        password,
        id_curso,
        fecha_ingreso
    ))

    conexion.commit()

    cursor.close()

    return redirect('/ver_estudiantes')
# =====================================
# ELIMINAR ESTUDIANTE (lo elimina el director)
# =====================================
@app.route('/eliminar_estudiante/<int:id_estudiante>')
def eliminar_estudiante(id_estudiante):
    cursor = conexion.cursor()
    cursor.execute("""
        DELETE FROM estudiante
        WHERE id_estudiante = %s
    """, (id_estudiante,))
    conexion.commit()
    cursor.close()
    return redirect('/ver_estudiantes')
# =====================================
# EDITAR ESTUDIANTE 
# =====================================
@app.route('/editar_estudiante/<int:id_estudiante>')
def editar_estudiante(id_estudiante):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            id_estudiante,
            ci,
            nombre,
            apellido,
            password,
            id_curso
        FROM estudiante
        WHERE id_estudiante = %s
    """, (id_estudiante,))
    estudiante = cursor.fetchone()
    cursor.execute("""
        SELECT
            id_curso,
            grado,
            paralelo
        FROM curso
        ORDER BY grado, paralelo
    """)
    cursos = cursor.fetchall()
    cursor.close()
    return render_template(
        'editar_estudiante.html',
        estudiante=estudiante,
        cursos=cursos
    )
# =====================================
# ACTUALIZAR ESTUDIANTE
# =====================================
@app.route('/actualizar_estudiante', methods=['POST'])
def actualizar_estudiante():

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE estudiante
        SET
            ci = %s,
            nombre = %s,
            apellido = %s,
            password = %s,
            id_curso = %s,
            fecha_ingreso = %s
        WHERE id_estudiante = %s
    """,
    (
        request.form['ci'],
        request.form['nombre'],
        request.form['apellido'],
        request.form['password'],
        request.form['id_curso'],
        request.form['fecha_ingreso'],
        request.form['id_estudiante']
    ))

    conexion.commit()

    cursor.close()

    return redirect('/ver_estudiantes')
#======================================
#Agregar Curso
#======================================
@app.route('/agregar_curso')
def agregar_curso():
    return render_template('agregar_curso.html')
#=======================================
#Eliminar Curso
#======================================
@app.route('/eliminar_curso/<int:id_curso>')
def eliminar_curso(id_curso):
    cursor = conexion.cursor()

    # 1. quitar estudiantes de ese curso (o reasignar si quieres)
    cursor.execute("""
        UPDATE estudiante
        SET id_curso = NULL
        WHERE id_curso = %s
    """, (id_curso,))

    # 2. eliminar relaciones profesor_materia
    cursor.execute("""
        DELETE FROM profesor_materia
        WHERE id_curso = %s
    """, (id_curso,))

    # 3. eliminar curso
    cursor.execute("""
        DELETE FROM curso
        WHERE id_curso = %s
    """, (id_curso,))

    conexion.commit()
    cursor.close()

    return redirect('/ver_estudiantes')
#=======================================
#Ver Cursos
#======================================
@app.route('/ver_cursos')
def ver_cursos():
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_curso, grado, paralelo
        FROM curso
        ORDER BY grado, paralelo
    """)
    cursos = cursor.fetchall()
    cursor.close()

    return render_template('ver_cursos.html', cursos=cursos)
#=======================================
#Guardar Curso
#======================================
@app.route('/guardar_curso', methods=['POST'])
def guardar_curso():

    grado = request.form['grado']
    paralelo = request.form['paralelo']

    cursor = conexion.cursor()

    # evitar duplicados
    cursor.execute("""
        SELECT * FROM curso
        WHERE grado=%s AND paralelo=%s
    """, (grado, paralelo))

    existe = cursor.fetchone()

    if existe:
        cursor.close()
        return "Ese curso ya existe"

    cursor.execute("""
        INSERT INTO curso (grado, paralelo)
        VALUES (%s, %s)
    """, (grado, paralelo))

    conexion.commit()
    cursor.close()

    return redirect('/ver_estudiantes')
# =====================================
# VER PROFESORES 
# =====================================
@app.route('/ver_profesores')
def ver_profesores():
    cursor = conexion.cursor()
    cursor.execute("""
    SELECT
        p.id_profesor,
        p.apellido,
        p.nombre,
        m.nombre,
        c.grado,
        c.paralelo
    FROM profesor p
    LEFT JOIN profesor_materia pm
        ON p.id_profesor = pm.id_profesor
    LEFT JOIN materia m
        ON pm.id_materia = m.id_materia
    LEFT JOIN curso c
        ON pm.id_curso = c.id_curso
    ORDER BY
        p.apellido,
        p.nombre
""")
    datos = cursor.fetchall()
    cursor.close()
    profesores = {}
    for id_prof, apellido, nombre, materia, grado, paralelo in datos:
        key = id_prof
        curso = f"{grado} {paralelo}"
        if key not in profesores:
            profesores[key] = {
                "nombre": f"{apellido} {nombre}",
                "materias": set(),
                "cursos": set()
            }
        profesores[key]["materias"].add(materia)
        profesores[key]["cursos"].add(curso)
    return render_template(
        'ver_profesores.html',
        profesores=profesores
    )
# =====================================
#Eliminar Profesor 
# =====================================
@app.route('/eliminar_profesor/<int:id_profesor>')
def eliminar_profesor(id_profesor):
    cursor = conexion.cursor()
    # primero eliminar relaciones
    cursor.execute("""
        DELETE FROM profesor_materia
        WHERE id_profesor = %s
    """, (id_profesor,))
    cursor.execute("""
        DELETE FROM profesor
        WHERE id_profesor = %s
    """, (id_profesor,))
    conexion.commit()
    cursor.close()
    return redirect('/ver_profesores')
# =====================================
#Editar Profesor 
# =====================================
@app.route('/editar_profesor/<int:id_profesor>')
def editar_profesor(id_profesor):
    cursor = conexion.cursor()

    # datos del profesor
    cursor.execute("""
        SELECT id_profesor, nombre, apellido, ci, password
        FROM profesor
        WHERE id_profesor = %s
    """, (id_profesor,))
    profesor = cursor.fetchone()

    # materias disponibles
    cursor.execute("""
        SELECT id_materia, nombre
        FROM materia
    """)
    materias = cursor.fetchall()

    # cursos disponibles
    cursor.execute("""
        SELECT id_curso, grado, paralelo
        FROM curso
    """)
    cursos = cursor.fetchall()

    # asignaciones actuales del profesor
    cursor.execute("""
        SELECT id_materia, id_curso
        FROM profesor_materia
        WHERE id_profesor = %s
    """, (id_profesor,))
    asignaciones = cursor.fetchall()

    cursor.close()

    return render_template(
        'editar_profesor.html',
        profesor=profesor,
        materias=materias,
        cursos=cursos,
        asignaciones=asignaciones
    )
# =====================================
#agregar Profesor
# =====================================
@app.route('/agregar_profesor')
def mostrar_agregar_profesor():

    cursor = conexion.cursor()

    cursor.execute("SELECT id_materia, nombre FROM materia")
    materias = cursor.fetchall()

    cursor.execute("SELECT id_curso, grado, paralelo FROM curso")
    cursos = cursor.fetchall()

    cursor.close()

    return render_template(
        'agregar_profesor.html',
        materias=materias,
        cursos=cursos
    )
#======================================
#actualizar Profesor 
#======================================
@app.route('/actualizar_profesor/<int:id_profesor>', methods=['POST'])
def actualizar_profesor(id_profesor):

    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ci = request.form['ci']
    password = request.form['password']

    materias = request.form.getlist('materias')
    cursos = request.form.getlist('cursos')

    cursor = conexion.cursor()

    # 1. actualizar datos del profesor
    cursor.execute("""
        UPDATE profesor
        SET nombre=%s,
            apellido=%s,
            ci=%s,
            password=%s
        WHERE id_profesor=%s
    """, (nombre, apellido, ci, password, id_profesor))

    # 2. borrar relaciones anteriores
    cursor.execute("""
        DELETE FROM profesor_materia
        WHERE id_profesor=%s
    """, (id_profesor,))

    # 3. insertar nuevas relaciones (multi materia + multi curso)
    for id_materia in materias:
        for id_curso in cursos:
            cursor.execute("""
                INSERT INTO profesor_materia
                (id_profesor, id_materia, id_curso)
                VALUES (%s, %s, %s)
            """, (id_profesor, id_materia, id_curso))

    conexion.commit()
    cursor.close()

    return redirect('/ver_profesores')
# =====================================
#guardar Profesor 
# =====================================
@app.route('/guardar_profesor', methods=['POST'])
def guardar_profesor():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ci = request.form['ci']
    password = request.form['password']
    materias = request.form.getlist('materias')
    cursos = request.form.getlist('cursos')
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO profesor
        (nombre, apellido, ci, password)
        VALUES (%s, %s, %s, %s)
        RETURNING id_profesor
    """, (nombre, apellido, ci, password))
    id_profesor = cursor.fetchone()[0]
    for id_materia in materias:
        for id_curso in cursos:
            cursor.execute("""
                INSERT INTO profesor_materia
                (id_profesor, id_materia, id_curso)
                VALUES (%s, %s, %s)
            """, (id_profesor, id_materia, id_curso))
    conexion.commit()
    cursor.close()
    return redirect('/ver_profesores')

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )