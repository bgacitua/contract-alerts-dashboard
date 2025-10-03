from datetime import datetime

class ReporteManager:
    def __init__(self, incidencias_df):
        self.incidencias_df = incidencias_df

    def _generar_tabla_incidencias_html(self, rut_empleado):
        """Genera la tabla HTML de incidencias para un RUT específico con estilo mejorado."""
        
        # Filtrar el DataFrame de incidencias por el RUT del empleado
        incidencias_empleado = self.incidencias_df[self.incidencias_df['rut_empleado'] == rut_empleado]

        if incidencias_empleado.empty:
            # Mensaje sobrio y claro cuando no hay incidencias
            return "<p style='margin-left: 20px; color: #6c757d; font-style: italic; font-size: 13px;'>✅ Este colaborador/a no registra ausencias, permisos o licencias activas.</p>"

        # Generar el HTML de la tabla de incidencias
        tabla_html = """
        <div style='margin-left: 20px; margin-top: 10px; margin-bottom: 20px;'>
            <h4 style='color: #2c3e50; border-left: 4px solid #f39c12; padding-left: 10px; font-size: 14px; margin-bottom: 10px;'>
                📂 Permisos y Licencias Encontradas:
            </h4>
            
            <table style='width: 95%; border-collapse: collapse; margin-top: 5px; font-size: 12px; border: 1px solid #e0e0e0;'>
def _generar_html_para_jefe(self, jefe, email_jefe, alertas_jefe, modo_prueba=False):
    """Genera HTML personalizado para cada jefe"""
    modo_texto = "<div style='background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin-bottom: 20px; border-radius: 5px;'><strong>🧪 MODO PRUEBA:</strong> Este correo habría sido enviado a " + email_jefe + "</div>" if modo_prueba else ""

    html = f"""
    <html>
    <head>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                line-height: 1.6; 
                color: #333;
                background-color: #f5f5f5;
            }}
            .email-container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #2c3e50, #34495e);
                color: white;
                padding: 30px 25px;
                text-align: center;
            }}
            .header h2 {{
                margin: 0;
                font-size: 1.8em;
                font-weight: 300;
                letter-spacing: 0.5px;
            }}
            .header p {{
                margin: 8px 0 0 0;
                opacity: 0.9;
                font-size: 0.95em;
            }}
            .content {{
                padding: 30px 25px;
            }}
            .resumen {{
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 20px;
                margin-bottom: 25px;
                border-radius: 0 8px 8px 0;
            }}
            .resumen h3 {{
                margin: 0 0 15px 0;
                color: #2c3e50;
                font-size: 1.2em;
                font-weight: 500;
            }}
            .resumen p {{
                margin: 8px 0;
                color: #555;
            }}
            .saludo {{
                margin-bottom: 20px;
                color: #2c3e50;
            }}
            .alerta-container {{
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                background-color: #fafafa;
            }}
            .alerta-header {{
                font-weight: 600;
                font-size: 1.1em;
                color: #2c3e50;
                margin-bottom: 15px;
                padding-bottom: 8px;
                border-bottom: 2px solid #ecf0f1;
            }}
            .urgente {{
                background-color: #fff5f5;
                border-left: 4px solid #e74c3c;
            }}
            .vencida {{
                background-color: #fdf2f2;
                border-left: 4px solid #c53030;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 15px;
                border-radius: 6px;
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #e1e8ed;
            }}
            th {{
                background-color: #34495e;
                color: white;
                font-weight: 500;
                text-transform: uppercase;
                font-size: 0.85em;
                letter-spacing: 0.5px;
            }}
            td {{
                background-color: white;
            }}
            tr:hover td {{
                background-color: #f8f9fa;
            }}
            .footer {{
                background-color: #34495e;
                color: white;
                padding: 20px 25px;
                font-size: 0.9em;
                text-align: center;
                opacity: 0.9;
            }}
        </style>
    </head>
    <body>
        {modo_texto}
        
        <div class="email-container">
            <div class="header">
                <h2>Alertas de Contratos</h2>
                <p>Notificación de alertas pendientes para su equipo</p>
            </div>
            
            <div class="content">
                <div class="saludo">
                    <p>Estimado/a <strong>{jefe}</strong>,</p>
                    <p>Por medio de la presente, le informamos que existen <strong>{len(alertas_jefe)} alerta(s)</strong> de contratos que requieren su atención y revisión:</p>
                </div>
                <div class="resumen">
                    <h3>Resumen Ejecutivo</h3>
                    <p><strong>Total de alertas:</strong> {len(alertas_jefe)}</p>
                    <p><strong>Colaboradores involucrados:</strong> {', '.join(alertas_jefe['Empleado'].tolist())}</p>
                    <p><strong>Fecha de término:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                </div>
                """

    # Agregar cada alerta del jefe
    for _, row in alertas_jefe.iterrows():
        dias_hasta = row["Días hasta alerta"]
        clase_css = "vencida" if dias_hasta <= 0 else "urgente" if row["Urgente"] == 1 else ""
        
        # Filtrar permisos para el empleado actual
        incidencias_empleado = self.incidencias_df[self.incidencias_df['rut_empleado'] == row['RUT']]
        
        html += f"""
        <div class="alerta-container {clase_css}">
            <div class="alerta-header">👤 {row['Empleado']} - {row['Cargo']}</div>
            <p><strong>Motivo:</strong> {row['Motivo']}</p>
            <p><strong>Fecha de Renovación:</strong> {row['Fecha alerta']}</p>
            <p><strong>Días hasta la fecha:</strong> {dias_hasta} días</p>
        """
        
        # Tabla de permisos
        if not incidencias_empleado.empty:
            html += """
            <h4>📅 Permisos/Licencias Activas:</h4>
            <table>
                <thead>
                    <tr style='background-color: #34495e;'>
                        <th style='padding: 8px 12px; border: none; color: white; text-align: left;'>Tipo de Permiso</th>
                        <th style='padding: 8px 12px; border: none; color: white; text-align: left;'>Fecha Inicio</th>
                        <th style='padding: 8px 12px; border: none; color: white; text-align: left;'>Fecha Fin</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for i, row in incidencias_empleado.iterrows():
            # Aplicar un fondo sutil a las filas pares para mejorar la lectura (zebra stripe)
            row_style = "background-color: #f9f9f9;" if i % 2 == 0 else "background-color: white;"
            
            # Asumo que ya tienes las columnas formateadas:
            # 'Tipo_Permiso_Formateado', 'fecha_inicio_formato', 'fecha_fin_formato'
            
            tabla_html += f"""
                    <tr style='{row_style}'>
                        <td style='padding: 8px 12px; border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>{row['Tipo_Permiso_Formateado']}</td>
                        <td style='padding: 8px 12px; border-right: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>{row['fecha_inicio_formato']}</td>
                        <td style='padding: 8px 12px; border-bottom: 1px solid #e0e0e0;'>{row['fecha_fin_formato']}</td>
                    </tr>
            """
            
        tabla_html += """
                </tbody>
            </table>
        </div>
        """
        return tabla_html

    def _generar_html_reporte_por_jefe(self, nombre_jefe, empleados_data):
        """
        Genera HTML consolidado para un jefe específico, creando una tabla separada 
        para cada motivo de alerta, utilizando agrupación manual (sin itertools).
        """
        
        # 1. AGRUPAR LOS EMPLEADOS POR MOTIVO DE FORMA MANUAL
        empleados_por_motivo = {}
        for emp in empleados_data:
            motivo = emp['motivo']
            
            # Si el motivo no existe en el diccionario, inicializa una lista vacía
            if motivo not in empleados_por_motivo:
                empleados_por_motivo[motivo] = []
                
            # Agrega el empleado a la lista de su motivo
            empleados_por_motivo[motivo].append(emp)

        # 2. INICIO DEL HTML Y ESTILOS (Se mantiene la sección de estilos y encabezado general)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Alertas de Contratos</title>
            <style>
                /* ... (Tus estilos CSS) ... */
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                /* Se añade un estilo para el título de la tabla de grupo */
                .group-title {{
                    border-bottom: 2px solid #adb5bd; /* Separador sutil */
                    color: #1565c0; 
                    margin-top: 30px;
                    padding-bottom: 5px;
                }}

                /* ESTILOS DE TABLA */
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px; 
                    margin-bottom: 30px; 
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #007bff;
                    color: white;
                    font-weight: bold;
                }}
                /* Alternancia de filas */
                tr:nth-child(odd) {{
                    background-color: #ffffff;
                }}
                tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                
                /* Colores de Alerta Actualizados */
                .urgente {{
                    background-color: #f7f7f7 !important; /* Gris muy claro para fila Indefinido */
                }}
                .tipo-alerta {{
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .segundo-plazo {{
                    background: #fff3cd;
                    color: #856404;
                }}
                .indefinido {{
                    background: #dee2e6; /* Gris claro para el tag Indefinido */
                    color: #495057; 
                }}
                
                /* Estilo para filas de incidencia */
                .incidencia-row td {{
                    padding: 0;
                    border: none;
                    background-color: #f8f9fa; 
                }}
                
                /* Estilos generales */
                .header {{ text-align: center; border-bottom: 3px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }}
                .header h1 {{ color: #007bff; margin: 0; font-size: 28px; }}
                .jefe-info {{ background: #e3f2fd; padding: 15px; border-radius: 6px; margin-bottom: 25px; }}
                .jefe-info h2 {{ margin: 0; color: #1565c0; }}
                .summary {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 6px; margin-bottom: 25px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #dee2e6; text-align: center; color: #6c757d; font-size: 14px; }}

            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Alertas de Contratos</h1>
                    <p>Empleados que requieren atención inmediata</p>
                </div>
                
                <div class="jefe-info">
                    <h2>👤 {nombre_jefe}</h2>
                    <p>Los siguientes empleados bajo su supervisión requieren atención:</p>
                </div>
                
                <div class="summary">
                    <strong>📊 Resumen:</strong> {len(empleados_data)} empleado(s) requieren revisión de contrato
                </div>
                
        """
        
        # 3. GENERACIÓN DE TABLAS SEPARADAS
        # Usamos sorted() para asegurar un orden consistente en las tablas (ej: alfabético por motivo)
        for motivo in sorted(empleados_por_motivo.keys()):
            grupo_empleados = empleados_por_motivo[motivo]
            
            # 3.1. Encabezado del grupo (Tabla)
            html += f"""
                <h3 class="group-title">Motivo: {motivo} ({len(grupo_empleados)} Empleado(s))</h3>
                
                <table>
                    <thead>
                        <tr>
                            <th>👤 Empleado</th>
                            <th>💼 Cargo</th>
                            <th>📅 Fecha Inicio</th>
                            <th>📝 Tipo Alerta</th>
                            </tr>
                    </thead>
                    <tbody>
            """
            
            # 3.2. Iterar sobre los empleados del grupo para llenar la tabla
            # Se puede ordenar por otro campo aquí si se desea (ej: 'fecha_inicio')
            for emp in grupo_empleados:
                rut_empleado = emp.get('rut') 
                
                # Estilos de fila y etiqueta
                clase_fila = "urgente" if emp['tipo_alerta'] == 'INDEFINIDO' else ""
                clase_tipo = "indefinido" if emp['tipo_alerta'] == 'INDEFINIDO' else "segundo-plazo"
                
                html += f"""

def _generar_html_reporte_seleccionadas(self, alertas_seleccionadas):
    """Genera el HTML del reporte solo para las alertas seleccionadas"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h2 {{ color: #e74c3c; }}
            .alerta-container {{ border: 1px solid #ccc; border-radius: 8px; padding: 15px; margin-bottom: 20px; }}
            .alerta-header {{ font-weight: bold; font-size: 1.2em; color: #2c3e50; }}
            .urgente {{ background-color: #fce4e4; }}
            .vencida {{ background-color: #ffcdd2; }}
            .seleccionada {{ background-color: #e8f5e8; border-color: #27ae60; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #34495e; color: white; }}
        </style>
    </head>
    <body>

        <p>Estimado/a, junto con saludar</p>
        <p>Se adjunta el listado de colaboradores con contratos pendientes de revisión:</p>

        <div class="resumen">
            <h3>Reporte Vencimiento de Contrato</h3>
        </div>
    
    """

    # Bucle para crear una sección por cada alerta seleccionada
    for _, row in alertas_seleccionadas.iterrows():
        dias_hasta = row["Días hasta alerta"]
        clase_css = "vencida" if dias_hasta <= 0 else "urgente" if row["Urgente"] == 1 else ""
        clase_css += " seleccionada"  # Agregar clase para destacar que fue seleccionada
        
        # Filtrar permisos para el empleado actual
        incidencias_empleado = self.incidencias_df[self.incidencias_df['rut_empleado'] == row['RUT']]
        
        # HTML para la alerta del empleado
        html += f"""
        <div class="alerta-container {clase_css}">
            <div class="alerta-header">Termino Contrato: {row['Empleado']}</div>
            <p><strong>Cargo:</strong> {row['Cargo']}</p>
            <p><strong>Motivo:</strong> {row['Motivo']}</p>
            <p><strong>Jefe Directo:</strong> {row['Jefe']} </p>
            <p><strong>Fecha de Renovación:</strong> {row['Fecha alerta']}</p>
        """
        
        # HTML para la tabla de permisos
        if not incidencias_empleado.empty:
            html += """
            <h4>Permisos Activos:</h4>
            <table>
                <thead>
                    <tr>
                        <th>Tipo de Permiso</th>
                        <th>Fecha de Inicio</th>
                        <th>Fecha de Fin</th>
                    </tr>
                </thead>
                <tbody>
            """
            for _, inc_row in incidencias_empleado.iterrows():
                html += f"""
                    <tr>
                        <td>{inc_row['tipo_permiso']}</td>
                        <td>{inc_row['fecha_inicio']}</td>
                        <td>{inc_row['fecha_fin']}</td>
                    </tr>
                """
            html += """
                </tbody>
            </table>
            """
        else:
            html += "<p>Este colaborador/a no registra ausencias, permisos y/o licencias.</p>"
            
        html += """
        </div>
        """

    html += f"""
    <br>

    <p><em><strong>Generado automáticamente por el Sistema de Alertas de Contratos de RRHH</strong></em></p>
    </body>
    </html>
    """
    return html

def _generar_html_reporte_por_jefe(nombre_jefe, empleados_data):
    """Genera HTML consolidado para un jefe específico"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Alertas de Contratos</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #007bff;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #007bff;
                margin: 0;
                font-size: 28px;
            }}
            .jefe-info {{
                background: #e3f2fd;
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 25px;
            }}
            .jefe-info h2 {{
                margin: 0;
                color: #1565c0;
            }}
            .summary {{
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 25px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #007bff;
                color: white;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            .urgente {{
                background-color: #ffebee !important;
            }}
            .tipo-alerta {{
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }}
            .segundo-plazo {{
                background: #fff3cd;
                color: #856404;
            }}
            .indefinido {{
                background: #f8d7da;
                color: #721c24;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #dee2e6;
                text-align: center;
                color: #6c757d;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚠️ Alertas de Contratos</h1>
                <p>Empleados que requieren atención inmediata</p>
            </div>
            
            <div class="jefe-info">
                <h2>👤 {nombre_jefe}</h2>
                <p>Los siguientes empleados bajo su supervisión requieren atención:</p>
            </div>
            
            <div class="summary">
                <strong>📊 Resumen:</strong> {len(empleados_data)} empleado(s) requieren revisión de contrato
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>👤 Empleado</th>
                        <th>💼 Cargo</th>
                        <th>📅 Fecha Inicio</th>
                        <th>📝 Motivo</th>
                        <th>🏷️ Tipo Alerta</th>
                    </tr>
                </thead>
                <tbody>
    """

    for emp in empleados_data:
        clase_fila = "urgente" if emp['tipo_alerta'] == 'INDEFINIDO' else ""
        clase_tipo = "indefinido" if emp['tipo_alerta'] == 'INDEFINIDO' else "segundo-plazo"
        
        html += f"""
                    <tr class="{clase_fila}">
                        <td><strong>{emp['empleado']}</strong></td>
                        <td>{emp['cargo']}</td>
                        <td>{emp['fecha_inicio']}</td>
                        <td><span class="tipo-alerta {clase_tipo}">{emp['tipo_alerta']}</span></td>
                    </tr>
                """
                
                # 3.3. Fila de Subtabla de Incidencias
                tabla_incidencias_html = self._generar_tabla_incidencias_html(rut_empleado)
                
                # El colspan es 4
                html += f"""
                    <tr class="incidencia-row">
                        <td colspan="4" style="padding: 0; border: none;"> 
                            {tabla_incidencias_html}
                        </td>
                    </tr>
                """
            
            # 3.4. Cerrar la tabla actual
            html += """
                    </tbody>
                </table>
            """
            
        # 4. CIERRE DEL HTML (Footer)
        html += """
                <div class="footer">
                    <p><strong>⏰ Acción requerida:</strong> Por favor revise y tome las acciones necesarias para estos contratos.</p>
                    <p>📧 Este es un correo automático generado por el Sistema de Alertas de Contratos</p>
                    <hr>
                    <small>Para consultas, contacte al área de Recursos Humanos</small>
                </div>
            </div>
        </body>
        </html>
        """
        return html
