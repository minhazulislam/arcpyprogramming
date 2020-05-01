import arcpy

# converting the polygon boundary to a line
# the geometry of the prepndicular line was Null. So, I used the repair geometry tool to delete the NULL values.

# inputs
boundary_polygon = "boundary" # give the polygon boundary layer 
lines_to_extend = "perpendicular_lines_for_polygon_30m2" # give the line layer to extend

# don't need to change anything for the rest of the code
arcpy.PolygonToLine_management(in_features="boundary", out_feature_class="boundary_line", neighbor_option="IDENTIFY_NEIGHBORS")
arcpy.RepairGeometry_management(in_features="perpendicular_lines_for_polygon_30m2", delete_null="DELETE_NULL")

coastline="boundary_line"
directions="perpendicular_lines_for_polygon_30m2"
g=arcpy.Geometry()
bank=arcpy.CopyFeatures_management(coastline,g)[0]

for i in range(2):
	with arcpy.da.UpdateCursor(directions,"Shape@") as cursor:
		for row in cursor:
			line=row[0]
			pStart=line.firstPoint
			pEnd=line.lastPoint
			L=line.length
			dX=(pEnd.X-pStart.X)/L;dY=(pEnd.Y-pStart.Y)/L
			p=pEnd
			m=0
			while True:
				l=bank.distanceTo(p)
				L+=l
				p.X=pStart.X+dX*L
				p.Y=pStart.Y+dY*L
				m+=1
				if m>100:break
				if l<0.001:break
			if m>100:continue
			row[0]=arcpy.Polyline(arcpy.Array([pStart,p]))
			cursor.updateRow(row)
	if i == 0:
		arcpy.FlipLine_edit(in_features=directions)

# deleting the boundary_line layer
arcpy.Delete_management(coastline)
