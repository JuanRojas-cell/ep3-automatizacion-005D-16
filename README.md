# Informe Técnico: Automatización e Infraestructura como Código (IaC)

**Cliente:** Servicios Portuarios Ltda  
**Proyecto:** Aprovisionamiento y Auditoría Programática del Core Router  
**Consultor / Auditor:** Juan Manuel Rojas Bustamante (Código: 005D-16)  

---

### 1. Objetivo del Proyecto
El proyecto consistió en el despliegue automático de la configuración base y de seguridad para el router perimetral `RTR-SERPOR` perteneciente a la empresa Servicios Portuarios Ltda. El objetivo primordial consistió en mitigar los errores humanos de configuración manual a través del uso de Infraestructura como Código (IaC) y establecer auditorías automatizadas capaces de certificar el cumplimiento de las normativas de la organización de forma 100% programática.

### 2. Alcance
* **Dentro de Alcance:** Automatización del cambio de Hostname; publicación del Banner de seguridad corporativo; aprovisionamiento descriptivo de la interfaz WAN GigabitEthernet1; instanciación de la Interfaz lógica Loopback 10 utilizando el direccionamiento oficial asignado a la fila 16; y la configuración global del servidor NTP corporativo. Asimismo, abarca la captura de snapshots de estado antes y después del aprovisionamiento mediante APIs de Red.
* **Fuera de Alcance:** Configuración de protocolos de enrutamiento dinámico (OSPF/BGP), políticas de Firewall aplicadas al plano de datos (ACLs) y tunelización VPN hacia dependencias secundarias.
* **Límites de Trabajo:** El proyecto se circunscribe exclusivamente al entorno virtualizado de laboratorio sobre el dispositivo Cisco CSR1kv mediante interfaces de control locales.

### 3. Infraestructura Utilizada
* **Dispositivo de Red:** Cisco CSR1kv (Cloud Services Router 1000V), operando bajo el sistema operativo Cisco IOS-XE versión 17.03.
* **Estación de Automatización:** Máquina Virtual DEVASC VM corriendo sobre Ubuntu Linux de 64 bits.
* **Software de Gestión:** Ansible versión 2.10+, Python 3.8+, pyATS framework con librerías Genie, y suites de protocolos para NETCONF/RESTCONF activos en el dispositivo de red.

### 4. Tecnologías Empleadas y Justificación
* **pyATS / Genie:** Se utilizó en la Fase 1 y Fase 5 debido a su alta eficiencia para extraer estados operativos complejos (como parsing de plataformas e interfaces) en estructuras de datos nativas y realizar análisis de discrepancias dinámicas (`diff`) en segundos.
* **Ansible:** Empleado en la Fase 2 gracias a su arquitectura sin agentes (*agentless*) impulsada por SSH, lo que permite el despliegue masivo, rápido y estandarizado de plantillas de configuración sobre plataformas Cisco heredadas.
* **NETCONF:** Implementado en la Fase 3 con la finalidad de validar de forma transaccional el Hostname de la máquina a través del puerto TCP 830 utilizando esquemas de datos estructurados e inmutables del modelo YANG.
* **RESTCONF:** Utilizado en la Fase 4 para interactuar con el router mediante llamadas HTTP REST comunes (GET/POST) permitiendo que aplicaciones web externas lean el estado del servidor NTP corporativo de forma ágil mediante payloads JSON ligeros.

### 5. Configuración Aplicada
A continuación se detallan los parámetros estandarizados aplicados al dispositivo en base a las variables oficiales de la fila 16:

| Parámetro | Valor Configurado |
| :--- | :--- |
| **Hostname** | `RTR-SERPOR` |
| **Banner MOTD** | `ACCESO RESTRINGIDO - Servicios Portuarios Ltda` |
| **Descripción GE1** | `Enlace Principal WAN - Fila 16` |
| **ID Loopback** | `10` |
| **IP Loopback 10** | `10.5.16.1` |
| **Máscara Loopback 10** | `255.255.255.0` |
| **Servidor NTP** | `208.67.222.222` |

### 6. Resultados de Validación
Las auditorías programáticas arrojaron las siguientes evaluaciones de cumplimiento técnico:

| Criterio de Validación | Protocolo / Interfaz | Estado de Cumplimiento |
| :--- | :--- | :--- |
| Extracción y comprobación de Hostname | NETCONF / XML (Puerto 830) | **CONFORME** |
| Verificación de consistencia Servidor NTP | RESTCONF / JSON (Puerto 443) | **CONFORME** |
| Integridad del Estado de Interfaces (Post-Cambio) | pyATS Diff Engine | **CONFORME** |

### 7. Conclusiones
El dispositivo `RTR-SERPOR` se encuentra operando bajo las configuraciones correctas, estables y sin desvíos de código respecto al baseline corporativo aprobado. La implementación de automatización por NETCONF y RESTCONF demostró un funcionamiento robusto, respondiendo con códigos de éxito HTTP 200 y validaciones sin alertas en los esquemas YANG. El equipo es entregado formalmente al área de operaciones de red.
