function rotAxis = rotateAxis(skel, deg)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Created 10.12.16
%Vlad Ayzenberg
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%This script takes in a series of skeletal points and then
%rotates the skeleton by a certain number of degrees



% define the x- and y-data for the original line we would like to rotate
x = transpose(skel(:,2));
y = transpose(skel(:,3));

% create a matrix of these points, which will be useful in future calculations
v = [x;y];
% choose a point which will be the center of rotation
x_center = mean(skel(:,2));
y_center = mean(skel(:,3));
% create a matrix which will be used later in calculations
center = repmat([x_center; y_center], 1, length(x));
% define a 60 degree counter-clockwise rotation matrix
theta = deg2rad(deg);       % pi/3 radians = 60 degrees
R = [cos(theta) -sin(theta); sin(theta) cos(theta)];
% do the rotation...
s = v - center;     % shift points in the plane so that the center of rotation is at the origin
so = R*s;           % apply the rotation about the origin
vo = so + center;   % shift again so the origin goes back to the desired center of rotation
% this can be done in one line as:
% vo = R*(v - center) + center
% pick out the vectors of rotated x- and y-data
x_rotated = vo(1,:);
y_rotated = vo(2,:);

rotAxis = [skel(:,1), transpose(x_rotated), transpose(y_rotated)];
