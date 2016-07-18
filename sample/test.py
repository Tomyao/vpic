
from paraview.simple import *
from paraview import coprocessing


#--------------------------------------------------------------
# Code generated from cpstate.py to create the CoProcessor.
# ParaView 5.1.0 64 bits


# ----------------------- CoProcessor definition -----------------------

def CreateCoProcessor():
  def _CreatePipeline(coprocessor, datadescription):
    class Pipeline:
      # state file generated using paraview version 5.1.0

      # ----------------------------------------------------------------
      # setup views used in the visualization
      # ----------------------------------------------------------------

      #### disable automatic camera reset on 'Show'
      paraview.simple._DisableFirstRenderCameraReset()

      # Create a new 'Render View'
      renderView1 = CreateView('RenderView')
      renderView1.ViewSize = [659, 621]
      renderView1.AxesGrid = 'GridAxes3DActor'
      renderView1.CenterOfRotation = [14.8828125, -0.1171875, -0.1171875]
      renderView1.StereoType = 0
      renderView1.CameraPosition = [-16.331702117140257, -11.972087171753932, 61.681154834284065]
      renderView1.CameraFocalPoint = [14.8828125, -0.11718749999999904, -0.11718750000000272]
      renderView1.CameraViewUp = [-0.8259265409848415, 0.45753180807429816, -0.32940855103818834]
      renderView1.CameraParallelScale = 18.179932583221223
      renderView1.Background = [0.32, 0.34, 0.43]

      # register the view with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the images, etc.
      coprocessor.RegisterView(renderView1,
          filename='image_%t.png', freq=1, fittoscreen=0, magnification=1, width=659, height=621, cinema={"composite":True, "camera":"Spherical", "phi":[-180,-150,-120,-90,-60,-30,0,30,60,90,120,150],"theta":[-180,-150,-120,-90,-60,-30,0,30,60,90,120,150], "initial":{ "eye": [-16.3317,-11.9721,61.6812], "at": [14.8828,-0.117188,-0.117188], "up": [-0.825927,0.457532,-0.329409] } })
      renderView1.ViewTime = datadescription.GetTime()

      # ----------------------------------------------------------------
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      # create a new 'XML Partitioned Polydata Reader'
      # create a producer from a simulation input
      contour_0pvtp = coprocessor.CreateProducer(datadescription, 'input')

      # ----------------------------------------------------------------
      # setup color maps and opacity mapes used in the visualization
      # note: the Get..() functions create a new object, if needed
      # ----------------------------------------------------------------

      # get color transfer function/color map for 'ChargeDensityHhydro'
      chargeDensityHhydroLUT = GetColorTransferFunction('ChargeDensityHhydro')
      chargeDensityHhydroLUT.RGBPoints = [0.9125778675079346, 0.231373, 0.298039, 0.752941, 1.0047980546951294, 0.865003, 0.865003, 0.865003, 1.0970182418823242, 0.705882, 0.0156863, 0.14902]
      chargeDensityHhydroLUT.ScalarRangeInitialized = 1.0

      # get opacity transfer function/opacity map for 'ChargeDensityHhydro'
      chargeDensityHhydroPWF = GetOpacityTransferFunction('ChargeDensityHhydro')
      chargeDensityHhydroPWF.Points = [0.9125778675079346, 0.0, 0.5, 0.0, 1.0970182418823242, 1.0, 0.5, 0.0]
      chargeDensityHhydroPWF.ScalarRangeInitialized = 1

      # ----------------------------------------------------------------
      # setup the visualization in view 'renderView1'
      # ----------------------------------------------------------------

      # show data from contour_0pvtp
      contour_0pvtpDisplay = Show(contour_0pvtp, renderView1)
      # trace defaults for the display properties.
      contour_0pvtpDisplay.ColorArrayName = ['POINTS', 'Charge Density(Hhydro)']
      contour_0pvtpDisplay.LookupTable = chargeDensityHhydroLUT
      contour_0pvtpDisplay.OSPRayScaleArray = 'Charge Density(Hhydro)'
      contour_0pvtpDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
      contour_0pvtpDisplay.GlyphType = 'Arrow'
      contour_0pvtpDisplay.SetScaleArray = ['POINTS', 'Charge Density(Hhydro)']
      contour_0pvtpDisplay.ScaleTransferFunction = 'PiecewiseFunction'
      contour_0pvtpDisplay.OpacityArray = ['POINTS', 'Charge Density(Hhydro)']
      contour_0pvtpDisplay.OpacityTransferFunction = 'PiecewiseFunction'

      # show color legend
      contour_0pvtpDisplay.SetScalarBarVisibility(renderView1, True)

      # setup the color legend parameters for each legend in this view

      # get color legend/bar for chargeDensityHhydroLUT in view renderView1
      chargeDensityHhydroLUTColorBar = GetScalarBar(chargeDensityHhydroLUT, renderView1)
      chargeDensityHhydroLUTColorBar.Title = 'Charge Density(Hhydro)'
      chargeDensityHhydroLUTColorBar.ComponentTitle = ''

      # ----------------------------------------------------------------
      # finally, restore active source
      SetActiveSource(contour_0pvtp)
      # ----------------------------------------------------------------
    return Pipeline()

  class CoProcessor(coprocessing.CoProcessor):
    def CreatePipeline(self, datadescription):
      self.Pipeline = _CreatePipeline(self, datadescription)

  coprocessor = CoProcessor()
  # these are the frequencies at which the coprocessor updates.
  freqs = {'input': [1]}
  coprocessor.SetUpdateFrequencies(freqs)
  return coprocessor

#--------------------------------------------------------------
# Global variables that will hold the pipeline for each timestep
# Creating the CoProcessor object, doesn't actually create the ParaView pipeline.
# It will be automatically setup when coprocessor.UpdateProducers() is called the
# first time.
coprocessor = CreateCoProcessor()

#--------------------------------------------------------------
# Enable Live-Visualizaton with ParaView
coprocessor.EnableLiveVisualization(False, 1)


# ---------------------- Data Selection method ----------------------

def RequestDataDescription(datadescription):
    "Callback to populate the request for current timestep"
    global coprocessor
    if datadescription.GetForceOutput() == True:
        # We are just going to request all fields and meshes from the simulation
        # code/adaptor.
        for i in range(datadescription.GetNumberOfInputDescriptions()):
            datadescription.GetInputDescription(i).AllFieldsOn()
            datadescription.GetInputDescription(i).GenerateMeshOn()
        return

    # setup requests for all inputs based on the requirements of the
    # pipeline.
    coprocessor.LoadRequestedData(datadescription)

# ------------------------ Processing method ------------------------

def DoCoProcessing(datadescription):
    "Callback to do co-processing for current timestep"
    global coprocessor

    # Update the coprocessor by providing it the newly generated simulation data.
    # If the pipeline hasn't been setup yet, this will setup the pipeline.
    coprocessor.UpdateProducers(datadescription)

    # Write output data, if appropriate.
    coprocessor.WriteData(datadescription);

    # Write image capture (Last arg: rescale lookup table), if appropriate.
    coprocessor.WriteImages(datadescription, rescale_lookuptable=False)

    # Live Visualization, if enabled.
    coprocessor.DoLiveVisualization(datadescription, "localhost", 22222)
