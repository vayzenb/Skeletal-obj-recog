function AxisNormed = alignSkels(currAxis)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Created 10.12.16
%Vlad Ayzenberg
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%This script takes in a series of skeletal points and then
%centers their the center of mass (COM) to an origin point [0,0,0] 
%Each model is centered in order to subsequently compare models in aligned
%same coordinate system

%the currAxis argument is the the axis that is being translated; feed it a
%series of 3D coordinates



origin = [0,0,0]; %Origin point on which to align the COM
    
COM = [mean(currAxis(:,1)), mean(currAxis(:,2)), mean(currAxis(:,3))]; %Find COM of Skeleton       

    
TranCom = repmat(origin - COM, length(currAxis), 1); %calculate how far points need to be translated in order to be centered around the origin
    
AxisNormed = currAxis + TranCom; %translate points to center them around the origin
    
    
