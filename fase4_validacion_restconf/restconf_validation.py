#!/usr/bin/env python3
import yaml
import json
import requests

# Desactivar advertencias de certificados SSL no válidos en entorno de laboratorio
requests.packages.urllib3.disable_warnings()

# 1. Cargar las variables globales del alumno (Fila 16)
with open("../vars/vars_juan_rojas.yaml", "r") as f:
    vars_data = yaml.safe_load(f)

router_ip = vars_data['router']['ip']
username = vars_data['router']['usuario']
password = vars_data['router']['password']
expected_ntp = vars_data['router']['ntp_server']

# 2. Configurar los parámetros de la API RESTCONF
url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-native:native/ntp"
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

print(f"[*] Realizando peticion GET RESTCONF hacia {url}...")

try:
    # 3. Hacer la consulta HTTP con autenticación básica
    response = requests.get(
        url,
        headers=headers,
        auth=(username, password),
        verify=False
    )
    
    if response.status_code == 200:
        print("[+] Conexión RESTCONF exitosa (Código 200).")
        
        # 4. Parsear la respuesta JSON del router
        json_data = response.json()
        
        # 5. Guardar el JSON crudo en la carpeta de respuestas de evidencia
        with open("responses/ntp_response.json", "w") as j_file:
            json.dump(json_data, j_file, indent=4)
            
        pretty_json = json.dumps(json_data, indent=4)
        print("\n--- [ Respuesta JSON RESTCONF ] ---")
        print(pretty_json)
        
        # 6. Validar si el servidor NTP coincide con la fila del alumno
        # Buscamos la IP dentro del string JSON para una validación directa
        if expected_ntp in pretty_json:
            print(f"\nSTATUS VALIDACION: [ PASSED ] - El servidor NTP coincide con '{expected_ntp}'")
            status_line = f"Validación NTP RESTCONF: PASSED (Encontrado: {expected_ntp})"
        else:
            print(f"\nSTATUS VALIDACION: [ FAILED ] - No se encontró el servidor NTP esperado '{expected_ntp}'")
            status_line = "Validación NTP RESTCONF: FAILED"
            
        # 7. Generar el archivo de reporte obligatorio de la Fase 4
        with open("evidencias/output_fase4.txt", "w") as out_file:
            out_file.write("=== REPORTE DE VALIDACIÓN RESTCONF ===\n")
            out_file.write(f"Alumno Code : {vars_data['alumno']['codigo']}\n")
            out_file.write(f"Resultado   : {status_line}\n")
            out_file.write("======================================\n\n")
            out_file.write(pretty_json)
            
        print("\n[+] Archivos de evidencia guardados exitosamente en la carpeta de la Fase 4.")
        
    else:
        print(f"[-] Error de comunicación. El router respondió con código HTTP: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"[-] Error crítico durante la ejecución de RESTCONF: {e}")
