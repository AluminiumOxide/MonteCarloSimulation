clc
clear
load("flux.mat");
flux = flux / (0.003 * 0.003 * 0.003 *10000);
flux_max = round(max(max(max(flux))))
flux_sum = sum(sum(sum(flux)))
value = max(max(flux));
[row,col] = find(value == flux);
% for i=1:200
%     
% end
cut_1 = flux(:,:,100);
cut_2 = flux(:,100,:);
cut_2 = squeeze(cut_2);
cut_3 = flux(100,:,:);
cut_3 = squeeze(cut_3);
figure
subplot(131)
imagesc(cut_1)
subplot(132)
imagesc(cut_2)
subplot(133)
imagesc(cut_3)
