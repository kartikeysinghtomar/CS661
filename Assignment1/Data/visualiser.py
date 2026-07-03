from vtk import *

# Create the reader for .vtp file
reader = vtkXMLPolyDataReader()
reader.SetFileName(r"C:\Users\tomar\Downloads\CS661\isocontour.vtp")
reader.Update()

# Mapper to map the polydata
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor to represent the data in the scene
actor = vtkActor()
actor.SetMapper(mapper)
 # Red color line

# Renderer to render the actor
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)  # White background

# Render window to display the result
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# Interactor to interact with the window
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Start visualization
render_window.Render()
interactor.Start()
