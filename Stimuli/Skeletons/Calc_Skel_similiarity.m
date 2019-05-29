clear all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calculates the Euclidean distance between two skeletons by taking a point on
%a figure and calcualting the distance of that point from the closest point
%on the other figure. 
%systematically rotates each figure to find the maximal alignment between
%each.
%Does this for both figures and calculates the average distance 
%8.23.17
%Vlad Ayzenberg
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%

%List Skeleton files
skelFiles = dir(['Experiment 1\', '*.csv']);

%Create matrix for data
SkelComps = zeros(length(skelFiles) * (length(skelFiles)-1)/2, 3);

% # of degrees to rotate skeleton by to find best alignment
deg = 15;
currDeg = 0;

n= 1;
for kk = 1:length(skelFiles) %loops through all comparisons 
    %load skeleton 1
    Array1 = csvread(['Experiment 1\', skelFiles(kk).name]); % assign first array
    Array1 = Array1(:,1:3);
    Array1 = alignSkels(Array1); %Normalize skeleton to origin
    
    for ss = (kk+1):(length(skelFiles)-1)      
    n
    %Load second skeleton
    Array2 = csvread(['Experiment 1\', skelFiles(ss).name]); % assign second array
    Array2 = Array2(:,1:3);
    Array2 = alignSkels(Array2); %Normalize skeleton to origin
    
         xx = 0;
         yy = 0;    
         for pp = 1:360/deg 
            if pp > 1
            Array2 = rotateSkel(Array2, deg); %rotates each MA in the picture plan orientations
            end
            
         meanArray1 = 0;
         meanArray2 = 0;

         
         for mm = 1:2 %do all comparisons twice, once normal, once mirrored.
             
             if mm == 1
                mir = 1;
             else
                 mir = -1;
             end
             
            % find the closest point on array 2 from each point on array1
            for ii = 1:size(Array1,1);
                for jj = 1:size(Array2,1); 
                    %The distance of each point from every other point
                    q(ii,jj) = sqrt((Array1(ii,1) - Array2(jj,1))^2 + (Array1(ii,2) - (mir*Array2(jj,2)))^2 + (Array1(ii,3) - Array2(jj,3))^2);
                end
                  xx(ii,pp) = min(q(ii,:));  %the closest point
            end
            
            meanArray1(pp) = mean(xx(:,pp)); %The mean distance

                    % find the closest point on array 2 from each point on array1
            for ii = 1:size(Array2,1);
                for jj = 1:size(Array1,1);
                    d(ii,jj) = sqrt((Array2(ii,1) - Array1(jj,1))^2 + ((mir* Array2(ii,2)) - Array1(jj,2))^2 + (Array2(ii,3) - Array1(jj,3))^2);
                end
                    yy(ii,pp) = min(d(ii,:));  
            end
             meanArray2(pp) = mean(yy(:,pp));
        
         tempMean(mm) = (meanArray1(pp) + meanArray2(pp))/2; % add mean of mirror form
        
         end
        compositeMean(1, pp) = min(tempMean); % choose the smallest mean between the mirrored options
        
        currDeg = currDeg + 15; %move to the next degree
         
         end
         
        SkelComps(n,1) = str2double(cell2mat(regexp(skelFiles(kk).name,'\d*','Match'))); %Set Figure 1
        SkelComps(n,2) = str2double(cell2mat(regexp(skelFiles(ss).name,'\d*','Match'))); %Set Figure 2
        SkelComps(n,3) = min (compositeMean(1,:)); %Fine smallest average distance
        
        n = n +1;
        currDeg = 0;
    end
end

save('SkelComps', 'SkelComps');
