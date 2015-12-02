files=dir('C:\Users\Prithviraj Dhar\Downloads\Jersey Numbers-New\Jersey Numbers-New\Sahana\Orignal');
target = 'C:\Users\Prithviraj Dhar\Downloads\Jersey Numbers-New\Jersey Numbers-New\Sahana\Orignal\patches\';%%%% TARGET FOLDER
mkdir(target);
for file = files(4:length(files))'
    if(file.bytes>8000)
        
        file
        colorImage = imread(strcat('C:\Users\Prithviraj Dhar\Downloads\Jersey Numbers-New\Jersey Numbers-New\Sahana\Orignal\',file.name));
        ntarget=strcat('C:\Users\Prithviraj Dhar\Downloads\Jersey Numbers-New\Jersey Numbers-New\Sahana\Orignal\patches\',file.name,'\');
        mkdir(ntarget);
        I=rgb2gray(colorImage);
        % Detect MSER regions.
        [mserRegions] = detectMSERFeatures(I, ...
            'RegionAreaRange',[200 8000],'ThresholdDelta',4);

        sz = size(I);
        pixelIdxList = cellfun(@(xy)sub2ind(sz, xy(:,2), xy(:,1)), ...
            mserRegions.PixelList, 'UniformOutput', false);

        % Next, pack the data into a connected component struct.
        mserConnComp.Connectivity = 8;
        mserConnComp.ImageSize = sz;
        mserConnComp.NumObjects = mserRegions.Count;
        mserConnComp.PixelIdxList = pixelIdxList;

        % Use regionprops to measure MSER properties
        mserStats = regionprops(mserConnComp, 'BoundingBox', 'Eccentricity', ...
            'Solidity', 'Extent', 'Euler', 'Image');

        % Compute the aspect ratio using bounding box data.
        bbox = vertcat(mserStats.BoundingBox);
        w = bbox(:,3);
        h = bbox(:,4);
        aspectRatio = w./h;

        % Threshold the data to determine which regions to remove. These thresholds
        % may need to be tuned for other images.
        filterIdx = aspectRatio' > 3;
        filterIdx = filterIdx | [mserStats.Eccentricity] > .995 ;
        filterIdx = filterIdx | [mserStats.Solidity] < .3;
        filterIdx = filterIdx | [mserStats.Extent] < 0.2 | [mserStats.Extent] > 0.9;
        filterIdx = filterIdx | [mserStats.EulerNumber] < -4;

        % Remove regions
        mserStats(filterIdx) = [];
        mserRegions(filterIdx) = [];

        % Show remaining regions
        regionImage = mserStats(6).Image;
        regionImage = padarray(regionImage, [1 1]);

        % Compute the stroke width image.
        distanceImage = bwdist(~regionImage);
        skeletonImage = bwmorph(regionImage, 'thin', inf);

        strokeWidthImage = distanceImage;
        strokeWidthImage(~skeletonImage) = 0;

        % Show the region image alongside the stroke width image.
        strokeWidthValues = distanceImage(skeletonImage);
        strokeWidthMetric = std(strokeWidthValues)/mean(strokeWidthValues);
        % Threshold the stroke width variation metric
        strokeWidthThreshold = 0.4;
        strokeWidthFilterIdx = strokeWidthMetric > strokeWidthThreshold;
        % Process the remaining regions
        for j = 1:numel(mserStats)

            regionImage = mserStats(j).Image;
            regionImage = padarray(regionImage, [1 1], 0);

            distanceImage = bwdist(~regionImage);
            skeletonImage = bwmorph(regionImage, 'thin', inf);

            strokeWidthValues = distanceImage(skeletonImage);

            strokeWidthMetric = std(strokeWidthValues)/mean(strokeWidthValues);

            strokeWidthFilterIdx(j) = strokeWidthMetric > strokeWidthThreshold;

        end

        % Remove regions based on the stroke width variation
        mserRegions(strokeWidthFilterIdx) = [];
        mserStats(strokeWidthFilterIdx) = [];

        % Show remaining regions
        % Get bounding boxes for all the regions
        bboxes = vertcat(mserStats.BoundingBox);

        % Convert from the [x y width height] bounding box format to the [xmin ymin
        % xmax ymax] format for convenience.
        xmin = bboxes(:,1);
        ymin = bboxes(:,2);
        xmax = xmin + bboxes(:,3) - 1;
        ymax = ymin + bboxes(:,4) - 1;

        % Expand the bounding boxes by a small amount.
        expansionAmount = 0.02;
        xmin = (1-expansionAmount) * xmin;
        ymin = (1-expansionAmount) * ymin;
        xmax = (1+expansionAmount) * xmax;
        ymax = (1+expansionAmount) * ymax;

        % Clip the bounding boxes to be within the image bounds
        xmin = max(xmin, 1);
        ymin = max(ymin, 1);
        xmax = min(xmax, size(I,2));
        ymax = min(ymax, size(I,1));

        % Show the expanded bounding boxes
        expandedBBoxes = [xmin ymin xmax-xmin+1 ymax-ymin+1];
        [Y,I]=sort(expandedBBoxes(:,1));
        rexpandedBBoxes=expandedBBoxes(I,:);

        IExpandedBBoxes = insertShape(colorImage,'Rectangle',rexpandedBBoxes,'LineWidth',3);

        for i=1:size(rexpandedBBoxes,1)
            imwrite((imcrop(colorImage, rexpandedBBoxes(i,:))),strcat('C:\Users\Prithviraj Dhar\Downloads\Jersey Numbers-New\Jersey Numbers-New\Sahana\Orignal\patches\',file.name,'\',num2str(i),'.jpg'));

        end
    end    
end
