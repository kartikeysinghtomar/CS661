import vtk;
import sys;

def add_contour_segment(edge_points,points, lines):
    point_ids = []


    for point in edge_points:
        point_id = points.InsertNextPoint(point[0], point[1], 25.0)
        point_ids.append(point_id)
    
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, point_ids[0])
    line.GetPointIds().SetId(1, point_ids[1])
    lines.InsertNextCell(line)

def pressure_val(i,j,presssure_vals,dims):
  return presssure_vals.GetTuple1(j*dims[0]+i)

def process_cell(i,j,pressure_vals,isovalue,dims,lines,points):
  
  bottom_left = pressure_val(i,j,pressure_vals,dims)
  bottom_right = pressure_val(i,j+1,pressure_vals,dims)
  top_right = pressure_val(i+1,j+1,pressure_vals,dims)
  top_left = pressure_val(i+1,j,pressure_vals,dims)

  values = [bottom_left, bottom_right, top_right, top_left]
  vertex_pos = [(i,j), (i,j+1), (i+1,j+1), (i+1,j)]

  edge_points = []

  for vertex_idx in range(4):
    v1 = values[vertex_idx]
    v2 = values[(vertex_idx+1)%4]

    if(v1<=isovalue<=v2 or v1>=isovalue>=v2):
      pos1 = vertex_pos[vertex_idx]
      pos2 = vertex_pos[(vertex_idx+1)%4]

      t = (isovalue-v1)/(v2-v1)
      x = pos1[0] + t * (pos2[0] - pos1[0])
      y = pos1[1] + t * (pos2[1] - pos1[1])
      
      edge_points.append((x,y))

  if len(edge_points)==2:
    add_contour_segment(edge_points,points,lines)


def extract_isocontour(image_data,isovalue):
  dimensions = image_data.GetDimensions()
  pressure_vals = image_data.GetPointData().GetScalars("Pressure")
  rows = dimensions[0]-1
  cols = dimensions[1]-1
  lines = vtk.vtkCellArray()
  points = vtk.vtkPoints()
  

  for i in range(rows):
    for j in range(cols):
      process_cell(i,j,pressure_vals,isovalue,dimensions,lines,points)
  
  polydata = vtk.vtkPolyData()
  polydata.SetPoints(points)
  polydata.SetLines(lines)
  return polydata


def main():
  if len(sys.argv) != 4:
    print("Please enter: python vtk_ass1.py <input.vti> <isovalue> <output.vtp>")
    sys.exit(1)
    
  input_file = sys.argv[1]
  isovalue = float(sys.argv[2])
  output_file = sys.argv[3]

  reader = vtk.vtkXMLImageDataReader()
  reader.SetFileName("./Isabel_2D.vti")
  reader.Update()

  image_data = reader.GetOutput()

  contour_data = extract_isocontour(image_data,isovalue)
  writer = vtk.vtkXMLPolyDataWriter()
  writer.SetFileName(output_file)
  writer.SetInputData(contour_data)
  writer.Write()
    
  print(f"Isocontour extracted for value {isovalue} and saved to {output_file}")
  
main()