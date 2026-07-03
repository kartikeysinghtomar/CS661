from vtk import *

reader = vtkXMLImageDataReader()
reader.SetFileName(r'C:\Users\tomar\Downloads\CS661\Assignment_1_19c33418-0dc5-4fc2-a834-9a9586a936e3\Assignment_1\Data\Isabel_3D.vti')
reader.Update()
data = reader.GetOutput()

opacitytransferfunc = vtkPiecewiseFunction()
opacitytransferfunc.AddPoint(2594.97, 0.0)
opacitytransferfunc.AddPoint(-4931.54, 1.0)
opacitytransferfunc.AddPoint(101.815, 0.002)

colortransferfunc = vtkColorTransferFunction()
colortransferfunc.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
colortransferfunc.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
colortransferfunc.AddRGBPoint(-1873.90, 0.0, 0.0, 0.5)
colortransferfunc.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
colortransferfunc.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
colortransferfunc.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)

volumeproperty = vtkVolumeProperty()
volumeproperty.SetColor(colortransferfunc)
volumeproperty.SetScalarOpacity(opacitytransferfunc)
volumeproperty.SetInterpolationTypeToLinear()
choice = input("Do you want to use the Phong Shading filter?yes or no \n").strip().lower()
if choice == "yes":
 volumeproperty.ShadeOn()
 volumeproperty.SetAmbient(0.5)      
 volumeproperty.SetDiffuse(0.5)    
 volumeproperty.SetSpecular(0.5)  

volumemapper = vtkSmartVolumeMapper()
volumemapper.SetInputConnection(reader.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volumemapper)
volume.SetProperty(volumeproperty)

outlined = vtkOutlineFilter()
outlined.SetInputConnection(reader.GetOutputPort())

outlinemapper = vtkPolyDataMapper()
outlinemapper.SetInputConnection(outlined.GetOutputPort())

outlineactor = vtkActor()
outlineactor.SetMapper(outlinemapper)
renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.SetSize(1000,1000)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(outlineactor)
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddVolume(volume)
renderWindow.Render()

print("Image Generated.")
renderWindowInteractor.Start()


