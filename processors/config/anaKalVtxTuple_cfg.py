import HpstrConf
import sys
import os
import baseConfig


baseConfig.parser.add_option("-w","--tracking", type="string", dest="tracking",
                  help="Which tracking to use to make plots", metavar="tracking", default="KF")
(options,args) = baseConfig.parser.parse_args()


# Use the input file to set the output file name
infile = options.inFilename
outfile = options.outFilename

outfile = outfile.split(".root")[0]+"_"+options.tracking+".root"

print 'Input file: %s' % infile
print 'Output file: %s' % outfile

p = HpstrConf.Process()

p.run_mode = 1
#p.max_events = 1000

# Library containing processors
p.libraries.append("libprocessors.so")

###############################
#          Processors         #
###############################

recoana_kf = HpstrConf.Processor('vtxana_kf', 'VertexAnaProcessor')
recoana_gbl = HpstrConf.Processor('vtxana_gbl', 'VertexAnaProcessor')

###############################
#   Processor Configuration   #
###############################
#RecoHitAna
recoana_kf.parameters["debug"] = 1
recoana_kf.parameters["anaName"] = "vtxana_kf"
recoana_kf.parameters["trkColl"] = "KalmanFullTracks"
recoana_kf.parameters["vtxColl"] = "UnconstrainedV0Vertices_KF"
recoana_kf.parameters["mcColl"]  = ""#"MCParticle"
recoana_kf.parameters["hitColl"] = "RotatedHelicalOnTrackHits"
recoana_kf.parameters["vtxSelectionjson"] = os.environ['HPSTR_BASE']+'/analysis/selections/customCuts.json'
recoana_kf.parameters["histoCfg"] = os.environ['HPSTR_BASE']+"/analysis/plotconfigs/tracking/vtxAnalysis_2019.json"
recoana_kf.parameters["beamE"] = 4.55
recoana_kf.parameters["isData"] = options.isData
recoana_kf.parameters["debug"] = 1
CalTimeOffset=-999.

if (options.isData==1):
    CalTimeOffset=56.
    print "Running on data file: Setting CalTimeOffset %d"  % CalTimeOffset
    
elif (options.isData==0):
    CalTimeOffset=43.
    print "Running on MC file: Setting CalTimeOffset %d"  % CalTimeOffset
else:
    print "Specify which type of ntuple you are running on: -t 1 [for Data] / -t 0 [for MC]"


recoana_kf.parameters["CalTimeOffset"]=CalTimeOffset
#Region definitions

RegionPath=os.environ['HPSTR_BASE']+"/analysis/selections/"
#recoana_kf.parameters["regionDefinitions"] = [RegionPath+'Tight.json']

#RecoHitAna
recoana_gbl.parameters = recoana_kf.parameters.copy()
recoana_gbl.parameters["anaName"] = "vtxana_gbl"
recoana_gbl.parameters["vtxColl"] = "UnconstrainedV0Vertices"
recoana_gbl.parameters["trkColl"] = "GBLTracks"

#    
#    RegionPath+'ESumCR.json',
#    RegionPath+'TightNoSharedL0.json',
#    RegionPath+'TightNoShared.json',

# Sequence which the processors will run.
#p.sequence = [recoana_kf,recoana_gbl]
if (options.tracking == "KF"):
    print("Run KalmanFullTracks analysis")
    p.sequence = [recoana_kf]
elif (options.tracking == "GBL"):
    print("Run GBL analysis")
    p.sequence = [recoana_gbl]
else :
    print ("ERROR::Need to specify which tracks KF or GBL")
    exit(1)

if (options.nevents > 0):
    p.max_events = options.nevents

p.input_files=[infile]
p.output_files = [outfile]

p.printProcess()


