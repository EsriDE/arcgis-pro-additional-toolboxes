
# -*- coding: utf-8 -*-
# MobileMaps.pyt — Gemeinsame Toolbox "Mobile Maps" mit 2 Tools:
#  - Validate MMPK: prüft .mmpk via ExtractPackage + Minimalstruktur
#  - Pack MMPK:     packt entpacktes MMPK-Verzeichnis zu .mmpk (ZIP_STORED) mit Auto-Output, Validierung & Overwrite-Flag

import arcpy
import os
import zipfile
import tempfile
import shutil

# ---------------------------------------------------------------------
# Toolbox-Definition
# ---------------------------------------------------------------------

class Toolbox(object):
    def __init__(self):
        self.label = "Mobile Maps"
        self.alias = "mobilemaps"
        self.description = "Tools for validating and packing Mobile Map Packages (MMPK)."
        self.tools = [ValidateMMPK, PackMMPK]

# ---------------------------------------------------------------------
# Tool 1: Validate MMPK
# ---------------------------------------------------------------------

class ValidateMMPK(object):
    def __init__(self):
        self.label = "Validate MMPK"
        self.description = "Validates a Mobile Map Package (.mmpk) using ExtractPackage and minimal structure checks."
        self.canRunInBackground = True

    def getParameterInfo(self):
        in_mmpk = arcpy.Parameter(
            displayName="Input MMPK",
            name="in_mmpk",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        in_mmpk.filter.list = ["mmpk"]
        in_mmpk.description = "Input Mobile Map Package (.mmpk)."

        keep_files = arcpy.Parameter(
            displayName="Keep Unpacked Files",
            name="keep_unpacked",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        keep_files.value = False  # Default
        keep_files.description = "If True, keeps the unpacked files and exposes 'UnpackDirectory' (Default: False)."

        unpack_dir_out = arcpy.Parameter(
            displayName="UnpackDirectory",
            name="unpack_dir_out",
            datatype="DEFolder",
            parameterType="Derived",   # abgeleitet; wird befüllt, wenn keep=True
            direction="Output"
        )
        unpack_dir_out.description = "Output folder where the package was unpacked (filled only when 'Keep Unpacked Files' = True)."

        return [in_mmpk, keep_files, unpack_dir_out]

    def execute(self, parameters, messages):
        mmpk_path = parameters[0].valueAsText
        keep = bool(parameters[1].value) if parameters[1].value is not None else False

        tmpdir = tempfile.mkdtemp(prefix="mmpk_validate_")
        arcpy.AddMessage(f"Unpack directory: {tmpdir}")

        ok = False
        try:
            # Entpacken (ExtractPackage + esriinfo-only)
            if not extract_package_with_esriinfo(mmpk_path, tmpdir):
                arcpy.AddWarning("VALIDATE MMPK – failure (ExtractPackage/esriinfo).")
                return

            # Minimalstruktur prüfen
            try:
                p_dir = validate_mmpk_folder_minimal(tmpdir)
                arcpy.AddMessage(f"Structure OK (esriinfo, {p_dir}, *.info).")
                ok = True
            except Exception as ex:
                arcpy.AddWarning(f"Structure invalid: {ex}")
                ok = False

            # Output-Parameter befüllen, falls Keep=True
            if keep and ok:
                parameters[2].value = tmpdir
                arcpy.AddMessage(f"UnpackDirectory set: {tmpdir}")

            # Abschlussmeldung
            if ok:
                arcpy.AddMessage("VALIDATE MMPK – success.")
            else:
                arcpy.AddWarning("VALIDATE MMPK – failure.")
        finally:
            # Nur löschen, wenn keep=False
            if not keep:
                try:
                    shutil.rmtree(tmpdir, ignore_errors=True)
                except Exception:
                    pass

# ---------------------------------------------------------------------
# Tool 2: Pack MMPK
# ---------------------------------------------------------------------

class PackMMPK(object):
    def __init__(self):
        self.label = "Pack MMPK"
        self.description = "Creates an MMPK file from a directory that is valid as an MMPK."
        self.canRunInBackground = True

    def getParameterInfo(self):
        source_dir = arcpy.Parameter(
            displayName="Source Folder (unpacked MMPK)",
            name="source_dir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        source_dir.description = "Folder containing the unpacked MMPK contents (must include 'esriinfo', one 'p..' folder, and at least one '*.info' in root)."

        out_mmpk = arcpy.Parameter(
            displayName="Output MMPK (optional)",
            name="out_mmpk",
            datatype="DEFile",
            parameterType="Optional",
            direction="Output"
        )
        out_mmpk.filter.list = ["mmpk"]
        out_mmpk.description = "Target MMPK path. If left empty, it will auto-fill to '<parent>/<foldername>.mmpk' after selecting the source folder."

        allow_overwrite = arcpy.Parameter(
            displayName="Allow Overwrite",
            name="allow_overwrite",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        allow_overwrite.value = False  # Default
        allow_overwrite.description = "If True, allows overwriting the output MMPK when it already exists (Default: False)."

        delete_src = arcpy.Parameter(
            displayName="Delete Source After Packing",
            name="delete_source",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        delete_src.value = False  # Default
        delete_src.description = "If True, deletes the source folder after successful packing (Default: False)."

        return [source_dir, out_mmpk, allow_overwrite, delete_src]

    # --- Dynamische Parametervalidierung / Auto-Setzen des Output ---
    def updateParameters(self, parameters):
        """
        Setzt den Output-Pfad automatisch, sobald ein Source Folder gewählt wurde,
        falls Output leer ist.
        """
        source_dir = parameters[0].valueAsText
        out_mmpk = parameters[1].valueAsText

        if parameters[0].altered and source_dir and (not out_mmpk or out_mmpk.strip() == ""):
            parent = os.path.dirname(source_dir.rstrip(os.sep))
            name = os.path.basename(source_dir.rstrip(os.sep))
            auto_out = os.path.join(parent, f"{name}.mmpk")
            parameters[1].value = auto_out  # Auto-fill sichtbar in der UI

    def updateMessages(self, parameters):
        """
        Prüft, ob die Output-Datei bereits existiert und zeigt direkt in der UI
        eine Warning (wenn Allow Overwrite=True) oder Error (wenn False).
        """
        out_mmpk = parameters[1].valueAsText
        allow_overwrite = bool(parameters[2].value) if parameters[2].value is not None else False

        # Validierung der Endung
        if out_mmpk and not out_mmpk.lower().endswith(".mmpk"):
            parameters[1].setErrorMessage("Output file must have the '.mmpk' extension.")

        # Existenzprüfung
        if out_mmpk and os.path.exists(out_mmpk):
            if allow_overwrite:
                parameters[1].setWarningMessage("Output file already exists and will be overwritten.")
            else:
                parameters[1].setErrorMessage("Output file already exists. Enable 'Allow Overwrite' to proceed.")

    def execute(self, parameters, messages):
        src_dir = parameters[0].valueAsText
        out_mmpk = parameters[1].valueAsText
        allow_overwrite = bool(parameters[2].value) if parameters[2].value is not None else False
        delete_source = bool(parameters[3].value) if parameters[3].value is not None else False

        # Zielpfad bestimmen, wenn leer (Failsafe — sollte durch updateParameters bereits gesetzt sein)
        if not out_mmpk:
            parent = os.path.dirname(src_dir.rstrip(os.sep))
            name = os.path.basename(src_dir.rstrip(os.sep))
            out_mmpk = os.path.join(parent, f"{name}.mmpk")

        arcpy.AddMessage(f"Source: {src_dir}")
        arcpy.AddMessage(f"Output: {out_mmpk}")

        try:
            # Vorab-Minimalprüfung am Ordner
            p_dir = validate_mmpk_folder_minimal(src_dir)
            arcpy.AddMessage(f"Structure OK (esriinfo, {p_dir}, *.info).")

            # Overwrite-Handhabung
            if os.path.exists(out_mmpk) and not allow_overwrite:
                raise RuntimeError("Output file already exists and overwriting is disabled.")

            # Packen
            pack_mmpk_from_folder(src_dir, out_mmpk)
            arcpy.AddMessage("PACK MMPK – success.")

            # Optional: Quelle löschen
            if delete_source:
                try:
                    shutil.rmtree(src_dir, ignore_errors=True)
                    arcpy.AddMessage("Source folder deleted.")
                except Exception as ex_del:
                    arcpy.AddWarning(f"Failed to delete source folder: {ex_del}")

        except Exception as ex:
            arcpy.AddWarning(f"PACK MMPK – failure: {ex}")

# ---------------------------------------------------------------------
# Gemeinsame Utilities
# ---------------------------------------------------------------------

def relwalk(root):
    """Yield (abs_path, rel_path) für alle Dateien unterhalb root."""
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            abs_path = os.path.join(dirpath, fn)
            rel_path = os.path.relpath(abs_path, root).replace(os.sep, "/")
            yield abs_path, rel_path

def validate_mmpk_folder_minimal(src_dir):
    """
    Mindeststruktur eines entpackten MMPK-Ordners prüfen.
    Bedingungen:
      - 'esriinfo' (Verzeichnis im Root) vorhanden
      - genau ein 'p..'-Ordner (3 Zeichen, beginnt mit 'p') im Root
      - mind. eine '*.info'-Datei im Root
    Raises: RuntimeError bei Verstoß. Gibt den Namen des 'p..'-Ordners zurück.
    """
    root_entries = os.listdir(src_dir)

    # 1) esriinfo/
    esriinfo_dir = os.path.join(src_dir, "esriinfo")
    if not os.path.isdir(esriinfo_dir):
        raise RuntimeError("Expected: 'esriinfo' directory missing in root.")

    # 2) p?? (genau 3 Zeichen, beginnt mit 'p')
    p_dirs = [d for d in root_entries
              if len(d) == 3 and d.startswith("p") and os.path.isdir(os.path.join(src_dir, d))]
    if len(p_dirs) != 1:
        raise RuntimeError("Expected: exactly one 'p..' directory (e.g., p14) in root.")

    # 3) mindestens eine *.info-Datei im Root
    has_info = any(
        os.path.isfile(os.path.join(src_dir, f)) and f.lower().endswith(".info")
        for f in root_entries
    )
    if not has_info:
        raise RuntimeError("Expected: at least one '*.info' file in root.")

    # optionaler Hinweis: mind. eine .mmap in p?? prüfen (nicht zwingend Fehler)
    p_root = os.path.join(src_dir, p_dirs[0])
    mmap_found = False
    for _, rel in relwalk(p_root):
        if rel.lower().endswith(".mmap"):
            mmap_found = True
            break
    if not mmap_found:
        arcpy.AddWarning("Note: No '.mmap' found inside the 'p..' directory.")

    return p_dirs[0]

def extract_package_with_esriinfo(mmpk_path, out_dir):
    """
    Entpackt ein .mmpk mit ArcGIS ExtractPackage nach out_dir
    und ergänzt anschließend ausschließlich den Ordner 'esriinfo'
    aus dem ZIP, falls vorhanden. Liefert True/False.
    """
    try:
        arcpy.management.ExtractPackage(mmpk_path, out_dir)
        arcpy.AddMessage("ExtractPackage: successful.")
    except Exception as ex:
        arcpy.AddWarning(f"ExtractPackage failed: {ex}")
        try:
            gp_msgs = arcpy.GetMessages()
            if gp_msgs:
                arcpy.AddWarning(gp_msgs)
        except Exception:
            pass
        return False

    # 'esriinfo/' gezielt aus dem ZIP extrahieren (falls ExtractPackage es auslässt)
    try:
        with zipfile.ZipFile(mmpk_path, "r") as zf:
            members = [n for n in zf.namelist() if n.lower().startswith("esriinfo/")]
            if not members:
                arcpy.AddMessage("Raw extract: No 'esriinfo/' found in package (ok).")
                return True

            for name in members:
                if name.endswith("/"):
                    dst_dir = os.path.join(out_dir, name)
                    os.makedirs(dst_dir, exist_ok=True)
                    continue
                dst = os.path.join(out_dir, name)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with zf.open(name) as src, open(dst, "wb") as f:
                    f.write(src.read())
            arcpy.AddMessage("Raw extract: 'esriinfo/' added.")
            return True

    except Exception as ex:
        arcpy.AddWarning(f"Raw extract of 'esriinfo/' failed: {ex}")
        return False

def pack_mmpk_from_folder(src_dir, out_mmpk_path):
    """
    Packt den kompletten Inhalt eines entpackten MMPK-Verzeichnisses
    erneut zu einer .mmpk-Datei – alle Dateien STORED, ZIP64 aktiviert.
    """
    with zipfile.ZipFile(out_mmpk_path, "w",
                         compression=zipfile.ZIP_STORED, allowZip64=True) as zf:
        for abs_path, rel_path in relwalk(src_dir):
            zf.write(abs_path, rel_path, compress_type=zipfile.ZIP_STORED)
