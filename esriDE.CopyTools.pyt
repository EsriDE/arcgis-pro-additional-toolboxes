
# -*- coding: utf-8 -*-
import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = "Data Copy Tools (Esri DE)"
        self.alias = "copytools"
        self.tools = [CopyLayer]


class CopyLayer(object):
    def __init__(self):
        self.label = "Copy Layer (Map -> Map)"
        self.description = "Kopiert Features zwischen Layern in beliebigen Karten desselben Projekts"
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Kartenwahl
        p_src_map = arcpy.Parameter(
            displayName="Source Map",
            name="source_map",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        p_trg_map = arcpy.Parameter(
            displayName="Target Map",
            name="target_map",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )

        # Layere Auswahl (wird dynamisch befüllt)
        p_src_layer = arcpy.Parameter(
            displayName="Source Layer",
            name="source_layer",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        p_trg_layer = arcpy.Parameter(
            displayName="Target Layer",
            name="target_layer",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )

        # Optional: Ziel vor Kopieren leeren
        p_clear = arcpy.Parameter(
            displayName="Ziel vor dem Kopieren leeren",
            name="clear_target",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
        )
        p_clear.value = True

        return [p_src_map, p_trg_map, p_src_layer, p_trg_layer, p_clear]

    def _list_map_names(self, aprx):
        return [m.name for m in aprx.listMaps()]

    def _list_feature_layer_names(self, m):
        # Nur sichtbare FeatureLayer-Namen (flach) – erweitere bei Bedarf um rekursive Suche in Grouplayern
        names = []
        for lyr in m.listLayers():
            try:
                if lyr.isFeatureLayer:
                    names.append(lyr.name)
            except Exception:
                # Manche Layerobjekte haben keine isFeatureLayer-Eigenschaft
                pass
        return names

    def updateParameters(self, parameters):
        aprx = arcpy.mp.ArcGISProject("CURRENT")

        # Kartenliste für beide Karten-Parameter
        map_names = self._list_map_names(aprx)
        parameters[0].filter.list = map_names
        parameters[1].filter.list = map_names

        # Wenn Source Map gewählt ist, Layerliste füllen
        if parameters[0].value:
            src_map = aprx.listMaps(parameters[0].valueAsText)[0]
            parameters[2].filter.list = self._list_feature_layer_names(src_map)
        else:
            parameters[2].filter.list = []

        # Wenn Target Map gewählt ist, Layerliste füllen
        if parameters[1].value:
            trg_map = aprx.listMaps(parameters[1].valueAsText)[0]
            parameters[3].filter.list = self._list_feature_layer_names(trg_map)
        else:
            parameters[3].filter.list = []

        return

    def updateMessages(self, parameters):
        # Plausibilitätschecks (optional)
        return

    def execute(self, params, messages):
        aprx = arcpy.mp.ArcGISProject("CURRENT")

        src_map_name = params[0].valueAsText
        trg_map_name = params[1].valueAsText
        src_layer_name = params[2].valueAsText
        trg_layer_name = params[3].valueAsText
        clear_target = bool(params[4].value) if params[4].altered else True

        # Layerobjekte auflösen
        src_map = aprx.listMaps(src_map_name)[0]
        trg_map = aprx.listMaps(trg_map_name)[0]

        src_layer = src_map.listLayers(src_layer_name)[0]
        trg_layer = trg_map.listLayers(trg_layer_name)[0]

        messages.addMessage(f"Quelle: [{src_map_name}] {src_layer_name}")
        messages.addMessage(f"Ziel:   [{trg_map_name}] {trg_layer_name}")

        self._copy_layer(src_layer, trg_layer, clear_target, messages)
        messages.addMessage("Kopieren abgeschlossen.")

    def _copy_layer(self, source_layer, target_layer, clear_target=True, messages=None):
        source_fields = [f.name for f in arcpy.ListFields(source_layer.dataSource)]
        target_fields = [f.name for f in arcpy.ListFields(target_layer.dataSource)]

        common_fields = [f for f in source_fields if f in target_fields and f.upper() not in ("SHAPE")]
        if "SHAPE@" not in common_fields:
            common_fields.insert(0, "SHAPE@")
        if "OBJECTID" not in common_fields:
            common_fields.insert(1, "OBJECTID")

        if messages:
            messages.addMessage("Gemeinsame Felder: " + ", ".join(common_fields))

        if clear_target:
            arcpy.management.DeleteRows(target_layer)

        # Anzahl der zu kopierenden Datensätze ermitteln
        total_count = int(arcpy.management.GetCount(source_layer)[0])

        # Progressor vorbereiten
        arcpy.SetProgressor("step", "Kopiere Features ...", 0, total_count, 1)

        copied_count = 0
        failed_count = 0

        # Index des ObjectID-Feldes ermitteln
        # Falls das Feld anders heißt (z.B. OID_), holen wir das automatische OID-Feld
        oid_field = arcpy.Describe(source_layer).OIDFieldName
        oid_index = common_fields.index(oid_field) if oid_field in common_fields else None

        with arcpy.da.SearchCursor(source_layer, common_fields) as s_cur, \
            arcpy.da.InsertCursor(target_layer, common_fields) as i_cur:

            for row in s_cur:
                try:
                    i_cur.insertRow(row)
                    copied_count += 1

                except Exception as ex:
                    failed_count += 1

                    # ObjectID bestimmen
                    if oid_index is not None:
                        oid_val = row[oid_index]
                    else:
                        oid_val = "<ObjectID nicht ermittelbar>"

                    if messages:
                        messages.addWarningMessage(
                            f"❌ Fehler beim Kopieren von ObjectID {oid_val}: {ex}"
                        )

                finally:
                    # Fortschrittsbalken weitersetzen
                    arcpy.SetProgressorPosition()

        # Fortschrittsbalken abschließen
        arcpy.ResetProgressor()

        # Zusammenfassung ausgeben
        if messages:
            messages.addMessage(f"✔ {copied_count} Features erfolgreich kopiert.")
            if failed_count > 0:
                messages.addWarningMessage(f"⚠ {failed_count} Features konnten nicht kopiert werden.")

