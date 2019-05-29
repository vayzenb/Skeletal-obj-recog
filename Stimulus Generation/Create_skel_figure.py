############################################
#Creates Novel Figures from their skeleton

#Vlad Ayzenberg
#Last Modified 4.25.19
############################################



import bpy 
import random
from math import * 
import numpy as np
import csv
import os
import sys


####################################
#This section calculates the points of the curve
def interpBez3(bp0, t, bp3):

	return interpBez3_(bp0.co, bp0.handle_right, bp3.handle_left, bp3.co, t)

def interpBez3_(p0, p1, p2, p3, t):
	r = 1-t
	return (r*r*r*p0 +
			3*r*r*t*p1 +
			3*r*t*t*p2 +
			t*t*t*p3)

def mission1(obj, t):
	points = []
	i1 = floor(t)

	curve = obj.data

	bp1 = curve.splines[0].bezier_points[i1]
	bp2 = curve.splines[0].bezier_points[i1+1]
	
	#This caluclates the points of the curve in "object space" then converts it to "world space"
	points = obj.matrix_world * interpBez3(bp1, t-i1, bp2)
	return points

def calcCurvePoints():
	points = []
	k = 0.000
	
	#Calculate a 1000 points of the curve by steps of .001
	for jj in range(0, 999):
		points.append(mission1(bpy.context.active_object, k))
		k += 0.001
	
	return points


####################
#This section takes pictures of the objects
def takePic(objName):
	#Rotation coordinates
	picRot = [[0, 0, -0.523598776], [0, -0.523598776, 0], [0, 0.785398163, 1.047197551]]
	
	rotName = ["Front", "Top", "Side"]

	for kk in range(0, 3):
		bpy.context.object.rotation_euler = picRot[kk]
		
		#Set file path for the render
		bpy.context.scene.render.filepath = mkdir + imDir + objName + "_" + rotName[kk] + ".png"
	
		#Take the picture
		bpy.ops.render.render(write_still = True)
	
	bpy.context.object.rotation_euler = [0, 0, 0]

###############################
#This section creates the figures
def createFigure(figNum, armNum, randScale):
	medialPoints = []
	
	#######################
	#Add the body curve
	bpy.ops.curve.primitive_bezier_curve_add(view_align=False, enter_editmode=False, location=(0.0,0.0, 0.0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

	#changes object name
	bpy.context.object.name = "BodyCurve"

	BodyCurve = bpy.context.selected_objects[0] 

	#go to edit mode
	bpy.ops.object.editmode_toggle()

	#Deselect all
	bpy.ops.curve.select_all(action='TOGGLE')


	#Select the one handle
	BodyCurve.data.splines[0].bezier_points[0].select_right_handle = True

	#Flatten it
	bpy.ops.transform.translate(value=(0.5, -0.5, -0.0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

	#Deselect all
	bpy.ops.curve.select_all(action='TOGGLE')

	#Select the one control point and apply random curve
	BodyCurve.data.splines[0].bezier_points[0].select_control_point = True
	bpy.ops.transform.translate(value=(random.uniform(-randScale-0.1,randScale+0.1), random.uniform(-randScale-0.1,randScale+0.1), random.uniform(-randScale-0.1,randScale+0.1)), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	#Deselect all
	bpy.ops.curve.select_all(action='TOGGLE')

	#Select the one control point and apply random curve
	BodyCurve.data.splines[0].bezier_points[1].select_control_point = True
	bpy.ops.transform.translate(value=(random.uniform(-randScale-0.1,randScale+0.1), random.uniform(-randScale-0.1,randScale+0.1), random.uniform(-randScale-0.1,randScale+0.1)), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	#Deselect all
	bpy.ops.curve.select_all(action='TOGGLE')

	#Select the one handle and apply random curve
	BodyCurve.data.splines[0].bezier_points[0].select_right_handle = True
	bpy.ops.transform.translate(value=(random.uniform(-randScale-0.1,randScale+0.1), random.uniform(-randScale-0.1,randScale+0.1), random.uniform(-randScale-0.1,randScale+0.1)), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	#Deselect all
	bpy.ops.curve.select_all(action='TOGGLE')

	#Select the one handle and apply random curve
	BodyCurve.data.splines[0].bezier_points[1].select_left_handle = True
	bpy.ops.transform.translate(value=(random.uniform(-randScale-0.1,randScale+0.1), random.uniform(-randScale-0.1,randScale+0.1), random.uniform(-randScale-0.1,randScale+0.1)), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)   

	#Make Random size
	BodySize = random.uniform(0.05,.25)
	bpy.context.object.scale = [BodySize, BodySize, BodySize]

	#go to object mode, recenter, and deselect all
	bpy.ops.object.editmode_toggle()
	bpy.context.object.location = [0.0, 0.0, 0.0]

	#Calculate points of the curve of the body and appends to medial points array
	points = []
	k = 0.000
	#Calculate a 1000 points of the curve by steps of .001
	for jj in range(0, 999):
		points.append(mission1(bpy.context.active_object, k))
		k += 0.001
		
	print("first curve was fine")

	#Deselect all
	bpy.ops.object.select_all(action='TOGGLE')

	#####################################
	#Add arm in a loop
	Arm = [0] * (armNum + 1)
	ArmName = [0] * (armNum + 1)
	#ii = 1
	#####################################

	for ii in range(1,armNum + 1):
			
		bpy.ops.curve.primitive_bezier_curve_add(view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

		#changes object name
		bpy.context.object.name = "Arm" + str(ii)
		ArmName[ii] = "Arm" + str(ii)

		Arm[ii] = bpy.context.selected_objects[0]

		#go to edit mode and deselect all
		bpy.ops.object.editmode_toggle()
		bpy.ops.curve.select_all(action='TOGGLE')

		#Select the one handle
		Arm[ii].data.splines[0].bezier_points[0].select_right_handle = True

		#Flatten it
		bpy.ops.transform.translate(value=(0.5, -0.5, -0.0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

		#Make Random size
		BodySize = random.uniform(0.05, 0.25)
		bpy.context.object.scale = [BodySize, BodySize, BodySize]

		randOrient = random.randint(1,2) #Orient randomly (either vertically or horizontally
		randSign = random.randint(0,1) #Pick the sign of the orientation (left vs. right; top vs. bottom
		if randSign == 0 and randOrient == 1:
			rotSign = 1
			transSign = -1
		elif randSign == 1 and randOrient == 1:
			rotSign = -1
			transSign = 1
		elif randOrient == 2: 
			if randSign == 0:
				rotSign = 1
				transSign = 1
			elif randSign == 1:
				rotSign = -1
				transSign = -1

		#Change orientation      
		bpy.context.object.rotation_euler[randOrient] = rotSign* 1.5708
		print(randOrient)


			
		#central body
		bpy.context.object.location = points[random.randint(1,999)]
		#Move end point when pointed up

		#When rot is 1 (Up), trans = 2 (move up); when rot is 2 (side), trans = 1 (move side)
		if randOrient == 1:
			transLoc = 2
		elif randOrient == 2:
			transLoc = 1

		#Make the movement    
		bpy.context.object.location[transLoc] =  bpy.context.object.location[transLoc] + (BodySize * transSign)

		##Deselect all
		bpy.ops.curve.select_all(action='TOGGLE')

		#Select the one handle
		Arm[ii].data.splines[0].bezier_points[0].select_right_handle = True

		#Random curve 
		bpy.ops.transform.translate(value=(random.uniform(-randScale,randScale), random.uniform(-randScale,randScale), random.uniform(-randScale,randScale)), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

		#Deselect all
		bpy.ops.curve.select_all(action='TOGGLE')

		#Select the one handle
		Arm[ii].data.splines[0].bezier_points[1].select_left_handle = True

		#Random curve 
		bpy.ops.transform.translate(value=(random.uniform(-randScale,randScale), random.uniform(-randScale,randScale), random.uniform(-randScale,randScale)), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

		#Go to object mode and deselect all
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.select_all(action='TOGGLE')
		
		bpy.context.scene.objects.active = bpy.data.objects[ArmName[ii]]
		bpy.data.objects[ArmName[ii]].select = True
		#Calculate points of the curve of the arm and appends to medial points array
		#points = []
		k = 0.000
		#Calculate a 1000 points of the curve by steps of .001
		for jj in range(0, 999):
			points.append(mission1(bpy.context.active_object, k))
			k += 0.001
		print(len(points))
		
		bpy.ops.object.select_all(action='TOGGLE')

	############################################
	#Join everything and center  
	
	#Select body and arm, then join
	bpy.data.objects['BodyCurve'].select = True
	for ii in range(1,armNum + 1):
		bpy.data.objects[ArmName[ii]].select = True

	bpy.ops.object.join()

	#rename final object
	finalObj = bpy.context.selected_objects[0]
	bpy.context.object.name = "Figure_" + str(figNum)
	#Normalize to .25
	bpy.context.object.scale = [0.25, .25, .25]
	
	#medialPoints = medialPoints
	np.savetxt(mkdir + "\\Skel Points\\Figure_" + str(figNum) + ".csv", points, delimiter=",")

	#Sets the origin (pivot) point of the object to the absolute center
	bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

	bpy.context.object.location = [0, 0, 0] #Reset location
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=False) #Set current rotation as 0

	bpy.ops.object.editmode_toggle()

	###########################################
	#Apply Bezier curve and apply taper

	#Assign tapers and bevels
	bevelObj = ["SkelBevel", "BalloonBevel"]
	taperObj = ["BalloonTaper", "BulgeTaper", "ShrinkTaper", "WaveTaper"]

	#Assign skel bevel and balloon taper
	bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj[0]]
	bpy.context.object.data.taper_object = bpy.data.objects[taperObj[0]]
	bpy.context.object.data.resolution_u = 512

	bpy.ops.object.editmode_toggle()

	#Change color of object to red
	mat = bpy.data.materials.new(name="ColorMat") #Create new material
	finalObj.data.materials.append(mat) #add material to object
	bpy.context.object.active_material.diffuse_color = (1, 0, 0) #change color



	if boolTakePic == True:
		#Take Skel pic
		takePic("Figure_" + str(figNum) + "_" + "SkelTaper")

		#Set bevel for remaining features
		bpy.context.object.data.bevel_object = bpy.data.objects[bevelObj[1]]
		
		for kk in range(0,len(taperObj)):
			bpy.context.object.data.taper_object = bpy.data.objects[taperObj[kk]]
			takePic("Figure_" + str(figNum) + "_" + taperObj[kk])

args = sys.argv
args = args[args.index("--"):]

#Working directories
#CHANGE ME
mkdir = "C:\\Users\\vayzenb\\Desktop\\GitHub Repos\\Skeletal-obj-recog\\Stimulus Generation"
rawDir = "\\Raw Blend Files\\Figures_" 
imDir = "\\Object Images\\"

#Change color of world to white
bpy.context.scene.world.horizon_color = (.184, .184, .184)

#If the number of figures isn't specified set to default (5), else set to specified number
if len(args) == 1:
	figureNum = 5
else:
	figureNum = int(args[1])

#Specify whether to take pictures of figure after creation
if args[2] == "1":
	boolTakePic = True
elif args[2] == "0":
	boolTakePic = False
else:
	boolTakePic = True

#amount by which to deform the figure
if len(args) < 3:
	randScale = 0.15 #If value isn't specified defer to default
else:
	randScale = float(args[3])

for jj in range(1, figureNum  + 1):
	createFigure(jj,2, randScale)
	bpy.ops.wm.save_as_mainfile(filepath= mkdir + rawDir + str(jj) + ".blend") 
	bpy.ops.object.delete(use_global=False)
