# import vtk and NumPy
from vtk import *
import numpy as np

# Linear interpolation function to find isocontour points 
def interpolate(p1, p2, v1, v2, iso):
    t = (iso - v1) / (v2 - v1)
    return p1 + t * (p2 - p1)

# Read the 2D VTI dataset
reader = vtkXMLImageDataReader()
reader.SetFileName("Isabel_2D.vti")  # Replace with the path to your file
reader.Update()
data = reader.GetOutput()

# Get number of cells and initialize an array to store 4 points with coordinates per cell
numCells = data.GetNumberOfCells()
cells = np.empty((numCells, 4, 3))  

# Extract coordinates for all 4 points of each cell
for i in range(numCells):
    cell = data.GetCell(i)  
    for j in range(4):
        pid = cell.GetPointId(j)           
        coord = data.GetPoint(pid)         
        cells[i, j, :] = coord     

# print(cells[3])        

# Extract pressure value at each point in every cell and store in an array
dataArr = data.GetPointData().GetArray('Pressure')
pressurevalues = np.empty((numCells, 4))
for i in range(numCells):
    cell = data.GetCell(i)
    for j in range(4):
        pid = cell.GetPointId(j)
        pressurevalues[i, j] = dataArr.GetValue(pid)

# print(pressure_values[0])

# Ask user for the isovalue to extract the contour at
iso = float(input("what isovalue do you want to take?? "))

# List to store isocontour points got by interpolation
isopoints = []

# print(isopoints.shape)
# print(isopoints.size)

# Loop through each cell and check for isopoints
for i in range(numCells):
    coords = cells[i]             # Get 4 point coordinates of the cell
    values = pressurevalues[i]   # Get scalar values of the 4 points

    
    if (values[0] - iso) * (values[1] - iso) < 0:   #to check if one of the value is less than the isovalue and one is greater
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

# you can check that the indexes for the square in this format      2 3  
# by printing cordinates, that's why we have traversed in this way  0 1

# Convert isopoints list to a NumPy array
isopoints = np.array(isopoints)

# Initialize VTK structures for storing lines and points
lines = vtkCellArray()
linepoints = vtkPoints()

# Connect every two consecutive isocontour points into a line segment
for i in range(0, len(isopoints), 2):
    if i + 1 < len(isopoints):
        pt1 = isopoints[i]
        pt2 = isopoints[i + 1]

        id1 = linepoints.InsertNextPoint(pt1)
        id2 = linepoints.InsertNextPoint(pt2)

        line = vtkLine()
        line.GetPointIds().SetId(0, id1)
        line.GetPointIds().SetId(1, id2)

        lines.InsertNextCell(line)

# Create VTK polydata object to hold lines and points
polydata = vtkPolyData()
polydata.SetPoints(linepoints)
polydata.SetLines(lines)

# Write the resulting isocontour lines to a .vtp file
writer = vtkXMLPolyDataWriter()
writer.SetFileName("isocontour.vtp") #put the path where you want the file to be stored if not in the same directory
writer.SetInputData(polydata)
writer.Write()
print("File has been generated.")
