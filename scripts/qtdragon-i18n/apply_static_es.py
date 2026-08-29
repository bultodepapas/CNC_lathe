#!/usr/bin/env python3
"""Apply the controlled first-pass Spanish terminology to QtDragon's static TS.

Only exact source strings listed below are finished. Everything else remains
unfinished, making coverage an honest indicator rather than an estimate.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET


TRANSLATIONS = {
    "MAIN": "PRINCIPAL",
    "FILE": "ARCHIVO",
    "OFFSETS": "COMPENSACIONES",
    "TOOL": "HERRAMIENTA",
    "STATUS": "ESTADO",
    "PROBE": "PALPADO",
    "CAMERA": "CÁMARA",
    "GCODES": "CÓDIGOS G",
    "SETUP": "CONFIGURACIÓN",
    "SETTINGS": "AJUSTES",
    "UTILS": "UTILIDADES",
    "USER": "USUARIO",
    "Toggle machine state": "Cambiar el estado de la máquina",
    "MACHINE\nOFF": "MÁQUINA\nDESHAB.",
    "MACHINE\nON": "MÁQUINA\nHABIL.",
    "ESTOP\nRESET": "REARMAR\nPARADA E.",
    "ESTOP\nSET": "ACTIVAR\nPARADA E.",
    "Exit LinuxCNC": "Salir de LinuxCNC",
    "EXIT": "SALIR",
    "History of loaded GCODE programs": "Historial de programas de código G cargados",
    "Distance from machine bed to top of workpiece": "Distancia desde la bancada hasta la cara superior de la pieza",
    "WORKPIECE HEIGHT": "ALTURA DE PIEZA",
    "Distance from machine bed to top of tool sensor": "Distancia desde la bancada hasta la cara superior del sensor de herramienta",
    "TOOL SENSOR HEIGHT": "ALTURA SENSOR HERRAMIENTA",
    "TOOL SENSOR LOCATION": "POSICIÓN SENSOR HERRAMIENTA",
    "LASER OFFSET": "COMPENSACIÓN LÁSER",
    "CAMERA OFFSET": "COMPENSACIÓN CÁMARA",
    "Go to Tool Sensor location": "Ir a la posición del sensor de herramienta",
    "GO TO\nSENSOR": "IR AL\nSENSOR",
    "Toggle laser crosshairs": "Mostrar u ocultar la retícula láser",
    "LASER\nOFF": "LÁSER\nAPAGADO",
    "LASER\nON": "LÁSER\nENCENDIDO",
    "Set laser crosshair reference": "Fijar la referencia de la retícula láser",
    "REF\nLASER": "REF.\nLÁSER",
    "REF\nCAMERA": "REF.\nCÁMARA",
    "TOUCHOFF TO TOOL SENSOR": "FIJAR REFERENCIA CON SENSOR DE HERRAMIENTA",
    "TOOL\nSENSOR": "SENSOR\nHERRAMIENTA",
    "TOOL DIAMETER": "DIÁMETRO HERRAMIENTA",
    "INCH": "PULGADA",
    "Distance from machine bed to top of touch plate": "Distancia desde la bancada hasta la cara superior de la placa de palpado",
    "TOUCH PLATE HEIGHT ": "ALTURA PLACA DE PALPADO ",
    "Add new tool to tooltable": "Añadir una herramienta a la tabla",
    "ADD": "AÑADIR",
    "Delete selected tools": "Eliminar las herramientas seleccionadas",
    "DELETE": "ELIMINAR",
    "Load selected tool": "Cargar la herramienta seleccionada",
    "TOUCHOFF TO TOOL TOUCHPLATE": "FIJAR REFERENCIA CON PLACA DE PALPADO",
    "TOUCH\nPLATE": "PLACA DE\nPALPADO",
    "Hold to save current view": "Mantener pulsado para guardar la vista actual",
    "User\nView": "Vista de\nusuario",
    "Set view P": "Seleccionar vista P",
    "Set view X": "Seleccionar vista X",
    "Set view Y": "Seleccionar vista Y",
    "Set view Z": "Seleccionar vista Z",
    "Toggle display dimensions": "Mostrar u ocultar las cotas",
    "Zoom in": "Acercar",
    "Zoom out": "Alejar",
    "Clear display": "Limpiar la vista",
    "Clear": "Limpiar",
    "Load selected file": "Cargar el archivo seleccionado",
    "LOAD\nFILE": "CARGAR\nARCHIVO",
    "Copy file from left to right": "Copiar el archivo de izquierda a derecha",
    "Copy file from right to left": "Copiar el archivo de derecha a izquierda",
    "Edit currently loaded gcode file": "Editar el archivo de código G cargado",
    "EDIT\nGCODE": "EDITAR\nCÓDIGO G",
    "ZERO\nROTATION": "ANULAR\nROTACIÓN",
    "ZERO G92": "ANULAR G92",
    "ZERO G5X": "ANULAR G5X",
    "Machine Log": "Registro de máquina",
    "Integrator Log": "Registro del integrador",
    "SYSTEM\nLOG": "REGISTRO\nSISTEMA",
    "MACHINE\nLOG": "REGISTRO\nMÁQUINA",
    "CLEAR\nSTATUS": "LIMPIAR\nESTADO",
    "Save status to file": "Guardar el estado en un archivo",
    "SAVE\nTO FILE": "GUARDAR\nEN ARCHIVO",
    "Recall\nError": "ÚLTIMO\nERROR",
    "ZOOM": "AUMENTO",
    "DIA": "DIÁM.",
    "ROT": "ROT.",
    "save Image to user/linuxcnc/nc_files/camImage.png": "Guardar imagen en user/linuxcnc/nc_files/camImage.png",
    "Save": "Guardar",
    "Parameters": "Parámetros",
    "PROPERTIES": "PROPIEDADES",
    "KEYBOARD MAPPING": "ATAJOS DE TECLADO",
    "ESC - Program Abort": "ESC - Abortar programa",
    "F1 - ESTOP": "F1 - Parada de emergencia",
    "F2 - Machine OFF": "F2 - Deshabilitar máquina",
    "F11 - Fullscreen": "F11 - Pantalla completa",
    "F12 - Style Sheet Editor": "F12 - Editor de estilos",
    "Home - HOME All": "Inicio - Referenciar todo",
    "Pause - Pause program": "Pausa - Pausar programa",
    "Make complicated 3D files more visible": "Mejorar la visualización de archivos 3D complejos",
    "ENABLE ALPHA MODE": "ACTIVAR MODO ALFA",
    "INHIBIT MOUSE SELECTION": "INHIBIR SELECCIÓN CON RATÓN",
    "Enable external offsets for spindle pause": "Activar compensaciones externas al pausar el husillo",
    "USE EXTERNAL OFFSETS": "USAR COMPENSACIONES EXTERNAS",
    "Reload last loaded tool": "Recargar la última herramienta",
    "RELOAD LAST TOOL": "RECARGAR ÚLTIMA HERRAMIENTA",
    "Reload last loaded program": "Recargar el último programa",
    "RELOAD LAST PROGRAM": "RECARGAR ÚLTIMO PROGRAMA",
    "Enable keyboard shortcuts": "Activar atajos de teclado",
    "USE KEYBOARD SHORTCUTS": "USAR ATAJOS DE TECLADO",
    "Enable run from line": "Permitir ejecutar desde una línea",
    "USE RUN FROM LINE": "EJECUTAR DESDE LÍNEA",
    "Enable use of onboard virtual keyboard": "Activar el teclado virtual integrado",
    "USE VIRTUAL KEYBOARD": "USAR TECLADO VIRTUAL",
    "Enable tool sensor": "Activar el sensor de herramienta",
    "USE TOOL SENSOR": "USAR SENSOR DE HERRAMIENTA",
    "Enable Webcam for work offset location": "Activar la cámara para ubicar el cero de pieza",
    "USE CAMERA": "USAR CÁMARA",
    "OVERRIDE LIMITS": "ANULAR LÍMITES",
    "HOME LOCATION": "POSICIÓN DE REFERENCIA",
    "TOUCHOFF PARAMETERS": "PARÁMETROS DE REFERENCIA",
    "Probe down search velocity": "Velocidad de búsqueda descendente del palpador",
    "SEARCH VELOCITY": "VELOCIDAD DE BÚSQUEDA",
    "Probe down final velocity": "Velocidad final descendente del palpador",
    "PROBE VELOCITY": "VELOCIDAD DE PALPADO",
    "Max probing distance": "Distancia máxima de palpado",
    "MAX PROBE": "RECORRIDO MÁX. PALPADO",
    "Distance to retract after G38.2 command": "Distancia de retirada después de G38.2",
    "RETRACT DISTANCE": "DISTANCIA DE RETIRADA",
    "Z safe travel height during rapid moves": "Altura segura de Z durante movimientos rápidos",
    "Z SAFE TRAVEL": "ALTURA SEGURA Z",
    "SPINDLE RAISE": "ELEVACIÓN DEL HUSILLO",
    "GCODE ZOOM": "AUMENTO CÓDIGO G",
    "ABOUT": "ACERCA DE",
    "TEST BUTTON": "PROBAR BOTÓN",
    "TEST LED": "PROBAR LED",
    "CALIBRATION": "CALIBRACIÓN",
    "True": "Verdadero",
    "False": "Falso",
    "HAL SCOPE": "OSCILOSCOPIO HAL",
    "HAL METER": "MEDIDOR HAL",
    "HAL SHOW": "VISOR HAL",
    "FACING": "REFRENTADO",
    "Bolt Hole Circle": "Círculo de agujeros",
    "Run Macro 0": "Ejecutar macro 0",
    "Run Macro 1": "Ejecutar macro 1",
    "Run Macro 2": "Ejecutar macro 2",
    "Run Macro 3": "Ejecutar macro 3",
    "Run Macro 4": "Ejecutar macro 4",
    "Run Macro 5": "Ejecutar macro 5",
    "Run Macro 6": "Ejecutar macro 6",
    "Run Macro 7": "Ejecutar macro 7",
    "Run Macro 8": "Ejecutar macro 8",
    "Run Macro 9": "Ejecutar macro 9",
    "UNITS": "UNIDADES",
    "JOG RATE\nMM/MIN": "VELOCIDAD MANUAL\nMM/MIN",
    "Adjust linear jog rate": "Ajustar la velocidad de movimiento manual lineal",
    "Toggle linear jog speed range": "Cambiar el rango de velocidad manual lineal",
    "FAST": "RÁPIDO",
    "SLOW": "LENTO",
    "LINEAR INCREMENT": "INCREMENTO LINEAL",
    "Select jog increment": "Seleccionar el incremento de movimiento manual",
    "ANGULAR INCREMENT": "INCREMENTO ANGULAR",
    "Toggle angular jog speed range": "Cambiar el rango de velocidad manual angular",
    "Adjust angular jog rate": "Ajustar la velocidad de movimiento manual angular",
    "CYCLE\nSTART": "INICIAR\nCICLO",
    "STOP": "DETENER",
    "PAUSE": "PAUSAR",
    "RESUME": "REANUDAR",
    "STEP": "PASO",
    "OPT\nBLOCK": "BLOQUE\nOPCIONAL",
    "OPT\nSTOP": "PARADA\nOPCIONAL",
    "MIST\nOFF": "NEBLINA\nAPAGADA",
    "MIST\nON": "NEBLINA\nENCENDIDA",
    "FLOOD\nOFF": "REFRIG.\nAPAGADO",
    "FLOOD\nON": "REFRIG.\nENCENDIDO",
    "RELOAD": "RECARGAR",
    "Spindle pause": "Pausa del husillo",
    "PAUSE\nSPINDLE": "PAUSAR\nHUSILLO",
    "SPINDLE\nPAUSED": "HUSILLO\nPAUSADO",
    "Surface cutting speed": "Velocidad de corte superficial",
    "No Tool Loaded": "Sin herramienta cargada",
    "Zero axis Y": "Poner a cero el eje Y",
    "ZERO": "CERO",
    "HOME": "REFERENCIAR",
    "UNHOME": "QUITAR REF.",
    "Show absolute coordinates": "Mostrar coordenadas absolutas",
    "Zero axis A": "Poner a cero el eje A",
    "CALCULATOR": "CALCULADORA",
    "Show relative coordinates": "Mostrar coordenadas relativas",
    "Show distance to go": "Mostrar distancia restante",
    "HOME ALL": "REFERENCIAR TODO",
    "Zero axis Z": "Poner a cero el eje Z",
    "Zero axis X": "Poner a cero el eje X",
    "Select work coordinate system": "Seleccionar sistema de coordenadas de trabajo",
    "GO TO\nZERO": "IR A\nCERO",
    "MAX VELOCITY OVERRIDE": "CORRECCIÓN VELOCIDAD MÁXIMA",
    "Set max velocity override to 50%": "Fijar corrección de velocidad máxima al 50 %",
    "Adjust max velocity override": "Ajustar la corrección de velocidad máxima",
    "Set max velocity override to 100%": "Fijar corrección de velocidad máxima al 100 %",
    "Actual max velocity rate": "Velocidad máxima actual",
    "Max velocity override": "Corrección de velocidad máxima",
    "RAPID OVERRIDE": "CORRECCIÓN DE RÁPIDO",
    "Set rapid override to 50%": "Fijar corrección de rápido al 50 %",
    "Adjust rapid rate override": "Ajustar la corrección de rápido",
    "Set rapid override to 100%": "Fijar corrección de rápido al 100 %",
    "Actual rapid rate": "Velocidad rápida actual",
    "Rapid rate override": "Corrección de rápido",
    "FEEDRATE OVERRIDE": "CORRECCIÓN DE AVANCE",
    "Set feedrate override to 50%": "Fijar corrección de avance al 50 %",
    "Adjust feed rate override": "Ajustar la corrección de avance",
    "Set feedrate override to 100%": "Fijar corrección de avance al 100 %",
    "Actual feedrate": "Avance actual",
    "Feedrate override": "Corrección de avance",
    "SPINDLE OVERRIDE": "CORRECCIÓN DE HUSILLO",
    "Set spindle override to 50%": "Fijar corrección del husillo al 50 %",
    "Adjust spindle override": "Ajustar la corrección del husillo",
    "Set spindle override to 100%": "Fijar corrección del husillo al 100 %",
    "Requested spindle RPM": "RPM solicitadas del husillo",
    "Spindle speed override": "Corrección de velocidad del husillo",
    "Set to Manual mode": "Cambiar a modo Manual",
    "MAN": "MANUAL",
    "Set to MDI mode": "Cambiar a modo MDI",
    "Set to Auto mode": "Cambiar a modo Automático",
    "AUTO": "AUTOMÁTICO",
    "SPINDLE RPM": "RPM DEL HUSILLO",
    "Spindle reverse": "Husillo en sentido inverso",
    "REV": "INV.",
    "Spindle forward": "Husillo en sentido directo",
    "FWD": "DIR.",
    "Spindle stop": "Detener el husillo",
    "Stop": "Detener",
    "AT SPEED": "A VELOCIDAD",
    "Spindle at speed": "Husillo a la velocidad solicitada",
    "Current spindle RPM": "RPM actuales del husillo",
    "POWER": "POTENCIA",
    "Spindle power": "Potencia del husillo",
    "MB ERRORS": "ERRORES MODBUS",
    "Total number of modbus errors": "Número total de errores Modbus",
    "VFD fault code": "Código de falla del variador",
    "Motion limited due to external offsets": "Movimiento limitado por compensaciones externas",
    "FAULT CODE": "CÓDIGO DE FALLA",
    "Spindle current": "Corriente del husillo",
    "AMPS": "AMPERIOS",
    "MOTION": "MOVIMIENTO",
    "RUN TIME": "TIEMPO DE EJECUCIÓN",
    "TIME": "HORA",
    "Exit": "Salir",
    "oPEN": "ABRIR",
    "Open": "Abrir",
    "Fullscreen": "Pantalla completa",
    "About": "Acerca de",
    "Rapid": "Rápido",
    "Feed": "Avance",
    "Arc": "Arco",
    "Tool Change": "Cambio de herramienta",
    "Probe": "Palpado",
    "Rotaty Index": "Índice giratorio",
}


PRESERVE = {
    "QT Dragon 2.0", "~/linuxcnc/configs/qtdragon/qtdragon.pref", "p", "P",
    "%1.2f mm", "%1.3f in", "MM", "X", "Y", "Z", "btn-laser-on",
    'print"Laser crosshair turned on"', 'print"Laser crosshair turned off"',
    "_toolsensor_", "%5.3f", "%10.3f", "led-probe",
    "INSTANCE.tooloffsetview.add_tool()", "INSTANCE.tooloffsetview.delete_tools()",
    "M61 Qn", "_touchplate_", "MDI:", "D", "+", "zoom-in", "-",
    "zoom-out", "C", "INSTANCE.stackedWidget_log.setCurrentIndex(1)",
    "INSTANCE.stackedWidget_log.setCurrentIndex(0)", "INSTANCE._NOTICE.show_last()",
    "INSTANCE.camview.saveImage()", "HTML", "PDF",
    "PROGRAM_LOADER.load_test_button()", "PROGRAM_LOADER.load_test_led()",
    'print"true command"', 'print"false command"', "tool.status", "tool.halscope",
    "tool.halmeter", "tool.halshow", "NgcGui", "Macro0", "Macro1", "Macro2",
    "Macro3", "Macro4", "Macro5", "Macro6", "Macro7", "Macro8", "Macro9",
    "A", "IN", "MM/MIN", "%.1f", "%d", "slider-jogspeed-linear", "slider_jog_linear",
    "slider_jog_angular", "slider-jogspeed-angular",
    "INSTANCE.progressBar.setFormat('STOPPED')", "SCS", "200.000", "200",
    "ABS", "REF Z", "G54", "REF Y", "DTG", "REFA", "REF X", "WCS",
    "G90 G0 A0", "G0 G0 G0 G0 G0 G0 G0 G0 G0 G0 G0 G0 G0",
    "M0 M0 M0 M0 M0 M0 M0 M0 M0", "50", "100", "%d %%",
    "slider-override-maxv", "slider-override-rapid", "slider-override-feed",
    "200.0", "slider-override-spindle", "MDI", "spindle-is-at-speed", "000",
    "0", "0x0", "00:00:00", "08:26:06 PM", "%I:%M:%S %p", "Ctrl+Q",
    "Ctrl+O", "F11",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--check", action="store_true", help="Report only; do not modify")
    args = parser.parse_args()
    tree = ET.parse(args.catalog)
    root = tree.getroot()
    counts = {"translated": 0, "preserved": 0, "unmapped": 0}
    unmapped = []

    for message in root.findall("./context/message"):
        source_element = message.find("source")
        translation = message.find("translation")
        source = "" if source_element is None else "".join(source_element.itertext())
        if translation is None:
            translation = ET.SubElement(message, "translation")
        if source in TRANSLATIONS:
            target = TRANSLATIONS[source]
            counts["translated"] += 1
        elif source in PRESERVE:
            target = source
            counts["preserved"] += 1
        else:
            counts["unmapped"] += 1
            unmapped.append(source)
            continue
        if not args.check:
            translation.attrib.pop("type", None)
            translation.text = target

    print(
        f"translated={counts['translated']} preserved={counts['preserved']} "
        f"unmapped={counts['unmapped']}"
    )
    for source in unmapped:
        print(f"UNMAPPED: {source!r}")
    if args.check:
        return 1 if unmapped else 0

    ET.indent(tree, space="    ")
    with tempfile.NamedTemporaryFile("wb", delete=False, dir=args.catalog.parent) as stream:
        stream.write(b'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE TS>\n')
        tree.write(stream, encoding="utf-8", xml_declaration=False)
        stream.write(b"\n")
        temporary = Path(stream.name)
    temporary.replace(args.catalog)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
