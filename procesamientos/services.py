
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
            mail.To = email_jefe
            mail.CC = "gpavez@cramer.cl"
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
