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
pressure_values = np.empty((numCells, 4))

for i in range(numCells):
    cell = data.GetCell(i)
    for j in range(4):
        pid = cell.GetPointId(j)             
        pressure_values[i, j] = dataArr.GetValue(pid)
print(pressure_values[0])

iso = float(input("what isovalue do you want to take?? "))
isopoints = []
for i in range(numCells):
    coords = cells[i]        
    values = pressure_values[i] 

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
lines = vtkCellArray()
line_points = vtkPoints()

for i in range(0, len(isopoints), 2):
    if i + 1 < len(isopoints):
        pt1 = isopoints[i]
        pt2 = isopoints[i + 1]

        id1 = line_points.InsertNextPoint(pt1)
        id2 = line_points.InsertNextPoint(pt2)

        line = vtkLine()
        line.GetPointIds().SetId(0, id1)
        line.GetPointIds().SetId(1, id2)

        lines.InsertNextCell(line)

polydata = vtkPolyData()
polydata.SetPoints(line_points)
polydata.SetLines(lines)


writer = vtkXMLPolyDataWriter()
writer.SetFileName("isocontour.vtp")
writer.SetInputData(polydata)
writer.Write()






















