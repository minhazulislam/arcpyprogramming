import arcpy

def line_extend_within_polygon(boundary_polygon, lines_to_extend):
	"""
	This python function can extend the lines within a boundary polygon upto the border line. 
	Here, boundary_polygon is the polygon shapefile and the lines_to_extend is the line shapefile which will be extended upto the border using the function.
	"""
	arcpy.PolygonToLine_management(in_features=boundary_polygon, out_feature_class="boundary_line", neighbor_option="IDENTIFY_NEIGHBORS")
	arcpy.RepairGeometry_management(in_features=lines_to_extend, delete_null="DELETE_NULL")

	coastline="boundary_line"
	directions=lines_to_extend
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
	return
