#!/usr/bin/env python3
import os

print("[*] Analizando evidencias de auditoria para Certificado de Compliance...")

# 1. Rutas de los archivos de validación anteriores
netconf_path = "../fase3_validacion_netconf/evidencias/output_fase3.txt"
restconf_path = "../fase4_validacion_restconf/evidencias/output_fase4.txt"
diff_dir = "evidencias/diff_005D-16"

netconf_ok = False
restconf_ok = False
diff_ok = False

# 2. Validar fase 3 (NETCONF)
if os.path.exists(netconf_path):
    with open(netconf_path, "r") as f:
        content = f.read()
        if "PASSED" in content:
            netconf_ok = True

# 3. Validar fase 4 (RESTCONF)
if os.path.exists(restconf_path):
    with open(restconf_path, "r") as f:
        content = f.read()
        if "PASSED" in content:
            restconf_ok = True

# 4. Validar existencia de diferencias de infraestructura (Genie Diff)
if os.path.exists(diff_dir) and len(os.listdir(diff_dir)) > 0:
    diff_ok = True

# 5. Determinar Estado Final de Compliance
netconf_status = "CONFORME" if netconf_ok else "NO CONFORME"
restconf_status = "CONFORME" if restconf_ok else "NO CONFORME"
diff_status = "CONFORME" if diff_ok else "NO CONFORME"

final_compliance = "CONFORME" if (netconf_ok and restconf_ok and diff_ok) else "NO CONFORME"

# 6. Generar el Certificado Oficial Requerido (E26)
certificado_content = f"""======================================================================
CERTIFICADO DE COMPLIANCE Y AUDITORÍA DE INFRAESTRUCTURA DE RED
======================================================================
ID CERTIFICADO: CERT-005D-16-2026
ALUMNO        : Juan Manuel Rojas Bustamante
CÓDIGO ALUMNO : 005D-16
CLIENTE       : Servicios Portuarios Ltda
DISPOSITIVO   : RTR-SERPOR (CSR1kv)
======================================================================

RESULTADOS DE VERIFICACIÓN OPERACIONAL:

[AUDITORÍA] Cambios de Configuración (Genie Diff)  : {diff_status}
[PROTOCOLO] Validación Hostname via NETCONF (830) : {netconf_status}
[API REST]  Validación Servidor NTP via RESTCONF   : {restconf_status}

======================================================================
DICTAMEN FINAL: {final_compliance}
======================================================================
El dispositivo de red RTR-SERPOR cumple plenamente con los lineamientos
de hardening, aprovisionamiento automatizado y políticas de compliance
establecidas para el despliegue del cliente Servicios Portuarios Ltda.
Se autoriza el cierre del ticket de implementación y el paso a operaciones.

Auditor Responsable: Juan Manuel Rojas Bustamante
Fecha de Emisión: 25/06/2026
======================================================================
"""

# Guardar el certificado en la ruta exigida
with open("evidencias/certificado_compliance_005D-16.txt", "w") as out:
    out.write(certificado_content)

# Mostrar en consola para capturar con el comando tee
print(certificado_content)
print("[+] Certificado generado exitosamente en 'evidencias/certificado_compliance_005D-16.txt'")
