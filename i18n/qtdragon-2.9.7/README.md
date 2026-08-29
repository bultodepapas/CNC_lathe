# Catálogo QtDragon 2.9.7 — español

`qtdragon_es.ts` se extrajo el 29 de agosto de 2026 desde el `qtdragon.ui`
instalado en el torno, no desde una versión descargada de internet.

Fuente:

```text
vendor/linuxcnc-2.9.7-qtdragon/usr/share/qtvcp/screens/qtdragon/qtdragon.ui
SHA-256 d50bc9c3919302d7ec5fa7df9443ee8e852837b51f6adb555968a261b95d2039
```

Estado de primera pasada:

- contexto: `MainWindow`;
- mensajes activos: 346;
- mensajes terminados: 346;
- traducciones españolas: 250;
- cadenas técnicas conservadas explícitamente: 96;
- cobertura estructural: 100 %;
- idioma objetivo: `es`;
- idioma fuente: `en`.

No se importaron automáticamente las traducciones del core de LinuxCNC porque
su coincidencia es baja y contiene terminología que no cumple el glosario del
torno. La primera pasada proviene del mapa explícito en
`scripts/qtdragon-i18n/apply_static_es.py`; las cadenas no clasificadas nunca se
marcan como terminadas de forma implícita.

Artefactos actuales:

| Archivo | SHA-256 |
|---|---|
| `qtdragon_es.ts` | `0634f268d6640faf046b12fca2a994023b2b6e63b3f509682e978c0fa344125b` |
| `qtdragon_es.qm` | `ad69d88c35e4a4f4b14d095373e656794d73997f8be6a3efccba8fe7dea8318b` |

Antes de compilar:

```powershell
python scripts/qtdragon-i18n/validate_ts.py `
  i18n/qtdragon-2.9.7/qtdragon_es.ts `
  --min-coverage 98
```

Resultado actual: 346/346, 100 %, cero errores y cero advertencias. Falta la
revisión visual y del operador; por eso el archivo aún no es apto para
despliegue productivo.

Este catálogo cubre únicamente la UI estática. Los mensajes del handler y los
widgets QtVCP se incorporan en fases posteriores, según
`docs/plan-qtdragon-es.md`.
