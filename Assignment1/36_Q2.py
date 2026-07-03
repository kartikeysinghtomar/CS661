# import vtk
from vtk import *

# Read the .vti volume data file
reader = vtkXMLImageDataReader()
reader.SetFileName('Isabel_3D.vti')  # Replace with the path to your VTI file
reader.Update()
data = reader.GetOutput()

# Create an opacity transfer function to map scalar values to opacity
opacitytransferfunc = vtkPiecewiseFunction()
opacitytransferfunc.AddPoint(2594.97, 0.0)     
opacitytransferfunc.AddPoint(-4931.54, 1.0)  
opacitytransferfunc.AddPoint(101.815, 0.002) 

# Create a color transfer function to map scalar values to colors
colortransferfunc = vtkColorTransferFunction()
colortransferfunc.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
colortransferfunc.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
colortransferfunc.AddRGBPoint(-1873.90, 0.0, 0.0, 0.5) 
colortransferfunc.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
colortransferfunc.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)  
colortransferfunc.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)   

# Define volume rendering properties using the color and opacity functions
volumeproperty = vtkVolumeProperty()
volumeproperty.SetColor(colortransferfunc)
volumeproperty.SetScalarOpacity(opacitytransferfunc)
volumeproperty.SetInterpolationTypeToLinear()  # linear interpolation

# Ask user whether to apply Phong shading or not
choice = input("Do you want to use the Phong Shading filter?yes or no \n").strip().lower()
if choice == "yes":
    volumeproperty.ShadeOn()           # Enable shading if user chooses yes
    volumeproperty.SetAmbient(0.5)   
    volumeproperty.SetDiffuse(0.5)   
    volumeproperty.SetSpecular(0.5)    

# Create the volume mapper to render the volumetric data
volumemapper = vtkSmartVolumeMapper()
volumemapper.SetInputConnection(reader.GetOutputPort())

# Create the volume actor with mapper and properties
volume = vtkVolume()
volume.SetMapper(volumemapper)
volume.SetProperty(volumeproperty)

# Create an outline around the dataset
outlined = vtkOutlineFilter()
outlined.SetInputConnection(reader.GetOutputPort())

# Map the outline data to a polygonal actor
outlinemapper = vtkPolyDataMapper()
outlinemapper.SetInputConnection(outlined.GetOutputPort())

outlineactor = vtkActor()
outlineactor.SetMapper(outlinemapper)

# Set up the renderer
renderer = vtkRenderer()

# Set up the render window
renderWindow = vtkRenderWindow()
renderWindow.SetSize(1000,1000)           # Window size
renderWindow.AddRenderer(renderer)

# Set up the render window interactor for user interaction
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Add the outline and volume to the scene
renderer.AddActor(outlineactor)
renderer.SetBackground(1.0, 1.0, 1.0)      # Set white background
renderer.AddVolume(volume)

# Render the scene and start
renderWindow.Render()
print("Image has been generated.")
renderWindowInteractor.Start()


