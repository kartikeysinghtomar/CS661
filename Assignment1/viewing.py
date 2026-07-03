import vtk

# Replace with your file path
file_path = "isocontour.vtp"

# Reader
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(file_path)
reader.Update()

# Mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)  # Background color

# Render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# Interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Start rendering
render_window.Render()
interactor.Start()
