from vtk import *
import numpy as np

def interpolate(p1, p2, v1, v2, iso):
    t = (iso - v1) / (v2 - v1)
    return p1 + t * (p2 - p1)

reader = vtkXMLImageDataReader()
reader.SetFileName("C:\\Users\\tomar\\Downloads\\CS661\\Assignment_1_19c33418-0dc5-4fc2-a834-9a9586a936e3\\Assignment_1\\Data\\Isabel_2D.vti")
reader.Update()
data = reader.GetOutput()
numCells = data.GetNumberOfCells()
cells = np.empty((numCells,4,3))

for i in range(numCells):
    cell = data.GetCell(i)  
    for j in range(4):
        pid = cell.GetPointId(j)   
        coord = data.GetPoint(pid)    
        cells[i, j, :] = coord   
print(cells[3])

dataArr = data.GetPointData().GetArray('Pressure')
pressurevalues = np.empty((numCells, 4))

for i in range(numCells):
    cell = data.GetCell(i)
    for j in range(4):
        pid = cell.GetPointId(j)             
        pressurevalues[i, j] = dataArr.GetValue(pid)
print(pressurevalues[0])

iso = float(input("what isovalue do you want to take?? "))
isopoints = []
for i in range(numCells):
    coords = cells[i]        
    values = pressurevalues[i] 

    if (values[0] - iso) * (values[1] - iso) < 0:
        pt = interpolate(coords[0], coords[1], values[0], values[1], iso)
        isopoints.append(pt)

    if (values[1] - iso) * (values[3] - iso) < 0:
        pt = interpolate(coords[1], coords[3], values[1], values[3], iso)
        isopoints.append(pt)

    if (values[2] - iso) * (values[3] - iso) < 0:
        pt = interpolate(coords[2], coords[3], values[2], values[3], iso)
        isopoints.append(pt)
    
    if (values[2] - iso) * (values[0] - iso) < 0:
        pt = interpolate(coords[2], coords[0], values[2], values[0], iso)
        isopoints.append(pt)

isopoints = np.array(isopoints)
print(isopoints.shape)
print(isopoints.size)
points = vtkPoints()
for pt in isopoints:
    points.InsertNextPoint(pt)

polyline = vtkPolyLine()
num_pts = points.GetNumberOfPoints()
polyline.GetPointIds().SetNumberOfIds(num_pts)

for i in range(num_pts):
    polyline.GetPointIds().SetId(i, i)

lines = vtkCellArray()
lines.InsertNextCell(polyline)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(lines)

writer = vtkXMLPolyDataWriter()
writer.SetFileName("isocontour.vtp")
writer.SetInputData(polydata)
writer.Write()






















