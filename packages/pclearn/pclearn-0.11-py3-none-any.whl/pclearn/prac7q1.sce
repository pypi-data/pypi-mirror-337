clc;
close;
a = imread("C:\Users\Admin\Downloads\cat.jpg");
a = rgb2gray(a);
[m n] = size(a);
t = input('Enter threshold parameter: ');
for i = 1:m
 for j = 1:n
 if(a(i,j)<t)
 b(i,j)=0;
 else
 b(i,j) =255;
 end
 end
end
figure(1)
imshow(a);
title('Original Image')
figure(2)
imshow(b);
title('Threshold Image')
xlabel(sprintf('Threshold Value is %g ',t))
