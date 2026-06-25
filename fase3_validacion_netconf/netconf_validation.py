#!/usr/bin/env python3
import yaml
import xml.dom.minidom
from ncclient import manager

# 1. Cargar las variables globales del alumno
with open("../vars/vars_juan_rojas.yaml", "r") as f:
    vars_data = yaml.safe_load(f)

router_ip = vars_data['router']['ip']
username = vars_data['router']['usuario']
password = vars_data['router']['password']
expected_hostname = vars_data['cliente']['hostname']

print(f"[*] Iniciando conexion NETCONF hacia {router_ip}:830...")

# 2. Filtro XML de tipo YANG para traer el Hostname nativo
netconf_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
  </native>
</filter>
"""

try:
    # 3. Conectarse al router vía NETCONF (Puerto 830)
    with manager.connect(
        host=router_ip,
        port=830,
        username=username,
        password=password,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    ) as m:
        
        print("[+] Conexión establecida de forma exitosa.")
        
        # 4. Obtener la configuración filtrada
        response = m.get_config(source='running', filter=netconf_filter)
        
        # 5. Guardar la respuesta XML cruda en evidencias
        xml_raw = response.xml
        with open("evidencias/response_netconf.xml", "w") as x_file:
            x_file.write(xml_raw)
        
        # 6. Parsear e imprimir el XML de forma legible (Pretty Print)
        dom = xml.dom.minidom.parseString(xml_raw)
        pretty_xml = dom.toprettyxml()
        print("\n--- [ Respuesta XML NETCONF (Pretty) ] ---")
        print(pretty_xml)
        
        # 7. Validar si el Hostname configurado es el correcto
        if expected_hostname in xml_raw:
            print(f"STATUS VALIDACION: [ PASSED ] - El hostname configurado coincide con '{expected_hostname}'")
            status_line = f"Validación Hostname NETCONF: PASSED (Encontrado: {expected_hostname})"
        else:
            print(f"STATUS VALIDACION: [ FAILED ] - No se encontro el hostname esperado '{expected_hostname}'")
            status_line = "Validación Hostname NETCONF: FAILED"

        # 8. Generar el reporte de salida final obligatorio de la Fase 3
        with open("evidencias/output_fase3.txt", "w") as out_file:
            out_file.write("=== REPORTE DE VALIDACIÓN NETCONF ===\n")
            out_file.write(f"Alumno Code : {vars_data['alumno']['codigo']}\n")
            out_file.write(f"Resultado   : {status_line}\n")
            out_file.write("=====================================\n\n")
            out_file.write(pretty_xml)
            
        print("\n[+] Archivos de evidencia guardados exitosamente en la carpeta 'evidencias/'.")

except Exception as e:
    print(f"[-] Error crítico durante la ejecucion de NETCONF: {e}")
