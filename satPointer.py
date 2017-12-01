#****************************************************************************#
#***************************** Satellite Pointer ****************************#
#****************************************************************************#
# Copyright (c) 2017, Kristian Husum Terkildsen <khte@mmmi.sdu.dk>
#    
# All rights reserved.

# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#   1. Redistributions of source code must retain the above copyright 
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in the 
#      documentation and/or other materials provided with the distribution.
#   3. Neither the name of the copyright holder nor the names of its 
#      contributors may be used to endorse or promote products derived from 
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#****************************************************************************#
"""
2017-12-01 KHT ... 
"""

#Imports
import math
from lib.utm import utmconv #Geodetic to UTM conversion class created by Kjeld Jensen

class satPointer():
	def __init__(self):
		test = 0
	
	def calcYawAngle(self, discPosX, discPosY): #Assumes uav to be the center of the world, calculates relative angle to disc with north as reference
		yawAngle = math.degrees(math.atan2(discPosX, discPosY))
		if yawAngle < 0:
			yawAngle = 360 + yawAngle
		return yawAngle
	
	def calcPitchAngle(self, discRelAlt, discDist):
		pitchAngle = math.degrees(math.atan2(discDist, discRelAlt))
		return pitchAngle
		
class coordinateManipulation():
	def __init__(self):
		self.uc = utmconv()
		self.uavEasting = 0
		self.uavNorthing = 0
		self.discEasting = 0
		self.discNorthing = 0
	
	def calcRelativePlanePos(self, uavLat, uavLon, discLat, discLon):
		(_, _, _, self.uavEasting, self.uavNorthing) = self.uc.geodetic_to_utm(uavLat, uavLon)
		(_, _, _, self.discEasting, self.discNorthing) = self.uc.geodetic_to_utm(discLat, discLon)
		eastingDiff = self.discEasting - self.uavEasting
		northingDiff = self.discNorthing - self.uavNorthing
		return eastingDiff, northingDiff
	
	def calcDistAndHeightDiff(self, uavAlt, discAlt):
		dist = math.hypot(self.discEasting - self.uavEasting, self.discNorthing - self.uavNorthing)
		relAlt = discAlt - uavAlt
		return dist, relAlt
	
if __name__ == "__main__":
	sp = satPointer()
	cm = coordinateManipulation()
	
	posX, posY = cm.calcRelativePlanePos(55.366661, 10.431477, 55.367615, 10.432678)
	dist, relAlt = cm.calcDistAndHeightDiff(30, 10)
	print dist, relAlt
	
	print sp.calcYawAngle(posX, posY)
	print sp.calcPitchAngle(relAlt, dist)
