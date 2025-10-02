
"""
Gestión de alertas de contrato
"""

from consultas_base.db_utils import DatabaseUtils
from tkinter import messagebox
#from plantillas.template_mails import _generar_html_reporte_seleccionadas
import win32com.client as win32
import pythoncom
import pandas as pd
from plantillas.template_mails import ReporteManager

db = DatabaseUtils()

def cargar_alertas(app):
    """Carga las alertas desde la BD y actualiza la interfaz"""
    
    app.alertas_df = db.obtener_alertas()
    app.incidencias_df = db.obtener_incidencias()    
    
    if not app.alertas_df.empty:
        print("Carga exitosa")
        # for i, col in enumerate(app.alertas_df.columns):
        #     print(f"  {i}: '{col}'")
    else:
        print("DataFrame vacío")

    if not app.incidencias_df.empty:
        print("Carga existosa de incidencias")
    else:
        print("Carga fallida de incidencias")
    
    app.actualizar_metricas()
    app.actualizar_tabla()

def enviar_alertas_seleccionadas(app):
    """Envía las alertas seleccionadas en la tabla."""
    seleccionados = app.alertas_tree.selection()

    report_generator = ReporteManager(app.incidencias_df)
    
    if not seleccionados:
        messagebox.showwarning("Sin selección", "Por favor selecciona al menos una alerta.")
        return
    
    confirmar_envio = messagebox.askyesno(
        "Confirmar envío",
        f"¿Enviar reporte con {len(seleccionados)} alerta(s) seleccionada(s)?"
    )
    
    if not confirmar_envio:
        return
    
    # Inicialización única de COM y Outlook FUERA del bucle
    outlook = None
    try:
        pythoncom.CoInitialize()
        outlook = win32.Dispatch("outlook.application")
    except Exception as e:
        messagebox.showerror("Error Outlook", f"No se pudo inicializar Outlook. Verifique la compatibilidad 32/64 bits: {e}")
        try:
            pythoncom.CoUninitialize()
        except:
            pass
        return
    
    db = report_generator.db # Usar la instancia de DB del ReporteManager
    alertas_exitosas = 0
    alertas_ya_procesadas = 0
    alertas_con_error = 0
    
    print(f"Enviando {len(seleccionados)} alertas")
    
    # Obtener los datos de las filas seleccionadas:
    for item in seleccionados:
        valores = app.alertas_tree.item(item)['values']
        empleado = valores[0]
        
        # Obtener el DataFrame de UNA SOLA FILA para el empleado actual
        fila_actual_df = app.alertas_df[app.alertas_df['Empleado'] == empleado]
        
        if not fila_actual_df.empty:
            
            rut = fila_actual_df.iloc[0]['RUT']
            correo_jefe = fila_actual_df.iloc[0]['Email Jefe']
            nombre_jefe = fila_actual_df.iloc[0]['Jefe']
            # Se mantienen las copias, etc.
            correo_copia = ["gpavez@cramer.cl", 'bgacitua@cramer.cl'] 
            email_prueba = "bgacitua@cramer.cl"

            tipo_alerta = db.obtener_tipo_alerta(rut)
            
            if tipo_alerta:
                print(f"Procesando: {empleado} - RUT: {rut} - Tipo: {tipo_alerta}, correo jefe: {correo_jefe}")
            
                if db.verificar_alerta_procesada(rut, tipo_alerta):
                    print(f"⚠️ SALTANDO: Alerta ya procesada para {empleado}")
                    alertas_ya_procesadas += 1
                    continue
                
                email_enviado = False
                
                try:
                    # Crear el item de correo DENTRO del bucle, usando el objeto 'outlook' inicializado
                    mail = outlook.CreateItem(0)
                    mail.To = email_prueba  # Modo prueba
                    # mail.To = correo_jefe  # Modo real
                    mail.CC = correo_copia
                    mail.Subject = f"Alerta de contrato pendiente de revisión: {empleado}" # Asunto específico
                    # 💡 CORRECCIÓN 1: Generar HTML solo para la fila actual
                    html = report_generator._generar_html_reporte_seleccionadas(fila_actual_df) 
                    mail.HTMLBody = html
                    mail.Send()
                    
                    email_enviado = True
                    print(f"Email enviado exitosamente a {nombre_jefe}")
                    
                except Exception as e:
                    # Si el error -2147352567 ocurre aquí, es casi seguro el problema 32/64 bit
                    print(f"❌ Error enviando correo: {e}")
                    messagebox.showerror("Error", f"Error enviando correo de {empleado}:\n{e}")
                    alertas_con_error += 1
                    email_enviado = False
                
                # Solo marcar como procesada Si el email se envió exitosamente
                if email_enviado:
                    if db.marcar_procesada(rut, tipo_alerta):
                        alertas_exitosas += 1
                        print(f"✅ Alerta enviada y registrada para {empleado}")
                    else:
                        print(f"⚠️ Email enviado pero error actualizando BD para {empleado}")
                        alertas_con_error += 1
                        
            else:
                print(f"❌ No se encontró tipo de alerta para {empleado}")
                alertas_con_error += 1
        else:
            print(f"❌ No se encontró el empleado {empleado} en el DataFrame")
            alertas_con_error += 1

    # Desinicialización al final de TODO el proceso
    try:
        pythoncom.CoUninitialize()
    except Exception as e:
        print(f"Advertencia al desinicializar COM: {e}")

    # Recargar los datos para reflejar los cambios
    cargar_alertas(app)
    
    # Mensaje final con resumen detallado
    mensaje_resumen = f"""RESUMEN:

Alertas Enviadas: {alertas_exitosas}
Alertas Omitidas: {alertas_ya_procesadas}  
Errores: {alertas_con_error}

Total procesadas: {len(seleccionados)}"""
    
    print(mensaje_resumen)
    
    if alertas_exitosas > 0:
        messagebox.showinfo("Proceso completado", mensaje_resumen)
    elif alertas_ya_procesadas > 0 and alertas_con_error == 0:
        messagebox.showwarning("Alertas ya procesadas", mensaje_resumen)
    else:
        messagebox.showerror("Errores en el proceso", mensaje_resumen)

def enviar_alertas_seleccionadas_por_jefe(app, jefes_filtro=None):
    """
    Envía las alertas, agrupadas por jefatura.
    Si se proporciona 'jefes_filtro' (lista de diccionarios con 'Jefe' y 'Email Jefe'),
    solo procesa las alertas de esos jefes.
    Si no se proporciona (ej. llamada desde otra parte), procesa todos los jefes con alertas pendientes.
    """
    if app.alertas_df.empty:
        messagebox.showwarning("Sin datos", "No hay alertas disponibles para enviar.")
        return
    
    db = DatabaseUtils()
    report_generator = ReporteManager(app.incidencias_df)
    # 1. Obtener TODAS las alertas pendientes
    alertas_pendientes = []
    
    for _, row in app.alertas_df.iterrows():
        rut = row['RUT']
        tipo_alerta = db.obtener_tipo_alerta(rut)
        
        if tipo_alerta and not db.verificar_alerta_procesada(rut, tipo_alerta):
            alertas_pendientes.append(row)
    
    if not alertas_pendientes:
        messagebox.showinfo("Sin alertas pendientes", "Todas las alertas ya han sido procesadas.")
        return
    
    df_pendientes = pd.DataFrame(alertas_pendientes)

    # 2. APLICAR FILTRO DE JEFES SELECCIONADOS
    df_a_procesar = df_pendientes.copy()

    if jefes_filtro:
        # Crea una lista de tuplas (Jefe, Email Jefe) a partir del filtro de la UI
        # Esto permite un filtrado eficiente en el DataFrame
        jefes_tuple = [(d['Jefe'], d['Email Jefe']) for d in jefes_filtro]
        
        # Filtra el DataFrame de alertas pendientes para incluir SOLO los jefes seleccionados
        df_a_procesar = df_pendientes[
            df_pendientes.set_index(['Jefe', 'Email Jefe']).index.isin(jefes_tuple)
        ].copy()
        
        if df_a_procesar.empty:
            messagebox.showinfo("Sin alertas pendientes", "Los jefes seleccionados no tienen alertas pendientes que requieran envío.")
            return

    # 3. Agrupar por jefe (Usando el DataFrame filtrado df_a_procesar)
    alertas_por_jefe = df_a_procesar.groupby(['Jefe', 'Email Jefe']).apply(lambda x: x.to_dict('records')).to_dict()
    
    total_jefes = len(alertas_por_jefe)
    total_empleados = len(df_a_procesar)
    
    confirmar_envio = messagebox.askyesno(
        "Confirmar envío masivo (Filtrado)",
        f"¿Enviar alertas a {total_jefes} jefe(s)?\n"
        f"Total de empleados afectados: {total_empleados} (solo pendientes/filtrados)\n\n"
        f"Se enviará un correo por jefe."
    )
    
    if not confirmar_envio:
        return
    
    # Contadores de resultados
    jefes_exitosos = 0
    jefes_con_error = 0
    alertas_enviadas = 0
    alertas_con_error = 0
    
    print(f"Iniciando envío masivo a {total_jefes} jefes (filtrados)")
    print("=" * 60)
    
    # 4. Procesar cada jefe en el grupo
    for (nombre_jefe, email_jefe), empleados_list in alertas_por_jefe.items():
        print(f"\nProcesando jefe: {nombre_jefe} ({email_jefe})")
        
        empleados_jefe = []
        ruts_procesados = []
        
        for emp_data in empleados_list:
            rut = emp_data['RUT']
            tipo_alerta = db.obtener_tipo_alerta(rut)
            
            if tipo_alerta:
                empleados_jefe.append({
                    'empleado': emp_data['Empleado'],
                    'rut': rut,
                    'cargo': emp_data['Cargo'],
                    # Ajusta 'Fecha Vencimiento' a la columna correcta si es necesario
                    'fecha_inicio': emp_data.get('Fecha Vencimiento', 'N/A'), 
                    'motivo': emp_data['Motivo'],
                    'tipo_alerta': tipo_alerta
                })
                ruts_procesados.append((rut, tipo_alerta))
        
        email_enviado = False
        report_generator = ReporteManager(app.incidencias_df)

        try:
            print(f"Enviando correo consolidado...")
            
            # --- CÓDIGO DE ENVÍO CON OUTLOOK (DESCOMENTAR CUANDO ESTÉ LISTO) ---
            pythoncom.CoInitialize()
            outlook = win32.Dispatch("outlook.application")
            mail = outlook.CreateItem(0)
            #mail.To = email_jefe
            mail.To = "bgacitua@cramer.cl"
            mail.Subject = f"Alertas de contratos - {len(empleados_jefe)} empleado(s) requieren atención"
            html = report_generator._generar_html_reporte_por_jefe(nombre_jefe, empleados_jefe)
            mail.HTMLBody = html
            mail.Send()
            pythoncom.CoUninitialize()
            
            # SIMULACIÓN (Borrar cuando se use Outlook real)
            email_enviado = True
            print(f"Correo enviado exitosamente a {nombre_jefe} con {len(empleados_jefe)} alerta(s)")
            
        except Exception as e:
            print(f"   ❌ Error enviando correo a {nombre_jefe}: {e}")
            email_enviado = False
        
        # 5. Marcar alertas como procesadas solo si el email se envió
        if email_enviado:
            alertas_marcadas = 0
            
            for rut, tipo_alerta in ruts_procesados:
                if db.marcar_procesada(rut, tipo_alerta):
                    alertas_marcadas += 1
                else:
                    print(f"   ⚠️ Error marcando como procesada: RUT {rut}")
            
            if alertas_marcadas == len(ruts_procesados):
                jefes_exitosos += 1
                alertas_enviadas += len(empleados_jefe)
                print(f"   ✅ {alertas_marcadas} alertas marcadas como procesadas")
            else:
                jefes_con_error += 1
                alertas_con_error += (len(empleados_jefe) - alertas_marcadas)
                print(f"   ⚠️ Solo {alertas_marcadas}/{len(ruts_procesados)} alertas marcadas")
        else:
            jefes_con_error += 1
            alertas_con_error += len(empleados_jefe)
    
    # 6. Recargar datos y mostrar resumen
    cargar_alertas(app) 
    
    print("\n" + "=" * 60)
    mensaje_resumen = f"""RESUMEN ENVÍO (Filtrado por Jefe):

Jefes notificados: {jefes_exitosos}
Jefes con errores: {jefes_con_error}

Alertas enviadas: {alertas_enviadas}
Alertas con error: {alertas_con_error}

Total procesado: {jefes_exitosos + jefes_con_error} jefe(s)"""
    
    print(mensaje_resumen)
    
    if jefes_exitosos > 0 and jefes_con_error == 0:
        messagebox.showinfo("Envío completado", mensaje_resumen)
    elif jefes_exitosos > 0 and jefes_con_error > 0:
        messagebox.showwarning("Envío parcial", mensaje_resumen)
    else:
        messagebox.showerror("Error en envío", mensaje_resumen)

    """
    Envía las alertas, agrupadas por jefatura.
    Si se proporciona 'jefes_filtro' (lista de diccionarios con 'Jefe' y 'Email Jefe'),
    solo procesa las alertas de esos jefes.
    Si no se proporciona, procesa todos los jefes con alertas pendientes.
    """
    if app.alertas_df.empty:
        messagebox.showwarning("Sin datos", "No hay alertas disponibles para enviar.")
        return
    
    db = DatabaseUtils()
    
    # 1. Obtener TODAS las alertas pendientes (filtrado por la BD)
    alertas_pendientes = []
    
    # Itera sobre el DataFrame principal para obtener solo las alertas que la BD
    # indica que AÚN no han sido procesadas (la lógica de first_alert_sent != 0, etc.)
    for _, row in app.alertas_df.iterrows():
        rut = row['RUT']
        # Suponemos que obtener_tipo_alerta también obtiene el estado de envío
        tipo_alerta = db.obtener_tipo_alerta(rut)
        
        # Filtramos las alertas que ya han sido procesadas
        if tipo_alerta and not db.verificar_alerta_procesada(rut, tipo_alerta):
            alertas_pendientes.append(row)
    
    if not alertas_pendientes:
        messagebox.showinfo("Sin alertas pendientes", "Todas las alertas ya han sido procesadas.")
        return
    
    df_pendientes = pd.DataFrame(alertas_pendientes)

    # 2. APLICAR FILTRO DE JEFES SELECCIONADOS (SI EXISTE)
    df_a_procesar = df_pendientes.copy()

    if jefes_filtro:
        # Crea una lista de tuplas (Jefe, Email Jefe) a partir del filtro de la UI
        jefes_tuple = [(d['Jefe'], d['Email Jefe']) for d in jefes_filtro]
        
        # Filtra el DataFrame de alertas pendientes para incluir SOLO los jefes seleccionados
        df_a_procesar = df_pendientes[
            df_pendientes.set_index(['Jefe', 'Email Jefe']).index.isin(jefes_tuple)
        ].copy()
        
        if df_a_procesar.empty:
            messagebox.showinfo("Sin alertas pendientes", "Los jefes seleccionados no tienen alertas pendientes.")
            return

    # 3. Agrupar por jefe (Usando el DataFrame filtrado df_a_procesar)
    # Crea el diccionario: { (Jefe, Email Jefe): [lista de dicts de empleados] }
    alertas_por_jefe = df_a_procesar.groupby(['Jefe', 'Email Jefe']).apply(lambda x: x.to_dict('records')).to_dict()
    
    total_jefes = len(alertas_por_jefe)
    total_empleados = len(df_a_procesar)
    
    confirmar_envio = messagebox.askyesno(
        "Confirmar envío masivo (Filtrado)",
        f"¿Enviar alertas a {total_jefes} jefe(s)?\n"
        f"Total de empleados afectados: {total_empleados} (solo pendientes/filtrados)\n\n"
        f"Se enviará un correo por jefe."
    )
    
    if not confirmar_envio:
        return
    
    # Contadores de resultados
    jefes_exitosos = 0
    jefes_con_error = 0
    alertas_enviadas = 0
    alertas_con_error = 0
    
    print(f"Iniciando envío masivo a {total_jefes} jefes (filtrados)")
    print("=" * 60)
    
    # 4. Procesar cada jefe en el grupo
    for (nombre_jefe, email_jefe), empleados_list in alertas_por_jefe.items():
        print(f"\nProcesando jefe: {nombre_jefe} ({email_jefe})")
        print(f"   Empleados a notificar: {len(empleados_list)}")
        
        empleados_jefe = []
        ruts_procesados = []
        
        for emp_data in empleados_list:
            rut = emp_data['RUT']
            tipo_alerta = db.obtener_tipo_alerta(rut)
            
            if tipo_alerta:
                empleados_jefe.append({
                    'empleado': emp_data['Empleado'],
                    'rut': rut,
                    'cargo': emp_data['Cargo'],
                    # Usamos 'Fecha Vencimiento' que es la columna del DataFrame, ajusta si es diferente en tu HTML/plantilla
                    'fecha_inicio': emp_data.get('Fecha Vencimiento', 'N/A'), 
                    'motivo': emp_data['Motivo'],
                    'tipo_alerta': tipo_alerta
                })
                ruts_procesados.append((rut, tipo_alerta))
        
        email_enviado = False
        
        try:
            print(f"Enviando correo consolidado...")
            
            # --- CÓDIGO DE ENVÍO CON OUTLOOK (DESCOMENTAR CUANDO ESTÉ LISTO) ---
            pythoncom.CoInitialize()
            outlook = win32.Dispatch("outlook.application")
            mail = outlook.CreateItem(0)
            mail.To = 'bgacitua@cramer.cl'
            #mail.To = email_jefe
            mail.Subject = f"Alertas de contratos - {len(empleados_jefe)} empleado(s) requieren atención"
            html = report_generator._generar_html_reporte_por_jefe(nombre_jefe, empleados_jefe) # Asume que esta función existe
            mail.HTMLBody = html
            mail.Send()
            pythoncom.CoUninitialize()
            
            # SIMULACIÓN (Borrar cuando se use Outlook real)
            email_enviado = True
            print(f"Correo enviado exitosamente a {nombre_jefe} con {len(empleados_jefe)} alerta(s)")
            
        except Exception as e:
            print(f"   ❌ Error enviando correo a {nombre_jefe}: {e}")
            email_enviado = False
        
        # 5. Marcar alertas como procesadas solo si el email se envió
        if email_enviado:
            alertas_marcadas = 0
            
            for rut, tipo_alerta in ruts_procesados:
                if db.marcar_procesada(rut, tipo_alerta):
                    alertas_marcadas += 1
                else:
                    print(f"   ⚠️ Error marcando como procesada: RUT {rut}")
            
            if alertas_marcadas == len(ruts_procesados):
                jefes_exitosos += 1
                alertas_enviadas += len(empleados_jefe)
                print(f"   ✅ {alertas_marcadas} alertas marcadas como procesadas")
            else:
                jefes_con_error += 1
                alertas_con_error += (len(empleados_jefe) - alertas_marcadas)
                print(f"   ⚠️ Solo {alertas_marcadas}/{len(ruts_procesados)} alertas marcadas")
        else:
            jefes_con_error += 1
            alertas_con_error += len(empleados_jefe)
    
    # 6. Recargar datos y mostrar resumen
    cargar_alertas(app) # Asume que esta función existe
    
    print("\n" + "=" * 60)
    mensaje_resumen = f"""RESUMEN ENVÍO (Filtrado por Jefe):

Jefes notificados: {jefes_exitosos}
Jefes con errores: {jefes_con_error}

Alertas enviadas: {alertas_enviadas}
Alertas con error: {alertas_con_error}

Total procesado: {jefes_exitosos + jefes_con_error} jefe(s)"""
    
    print(mensaje_resumen)
    
    if jefes_exitosos > 0 and jefes_con_error == 0:
        messagebox.showinfo("Envío completado", mensaje_resumen)
    elif jefes_exitosos > 0 and jefes_con_error > 0:
        messagebox.showwarning("Envío parcial", mensaje_resumen)
    else:
        messagebox.showerror("Error en envío", mensaje_resumen)