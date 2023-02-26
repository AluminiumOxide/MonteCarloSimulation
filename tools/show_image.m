% clc
% clear
% load("./bin_output/oppo112_F.mat");
% flux = flux / (0.003 * 0.003 * 0.003 *10000);
% flux_min = floor(min(min(min(flux))))
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
% ? 为什么我光通量都是加的正值，这东西能取出来负数
log_cut_1 = log(cut_1-min(min(cut_1)));
log_cut_2 = log(cut_2-min(min(cut_2)));
log_cut_3 = log(cut_3-min(min(cut_3)));

figure
subplot(131)
imagesc(cut_1)
subplot(132)
imagesc(cut_2)
subplot(133)
imagesc(cut_3)

figure
subplot(131)
imagesc(log_cut_1)
subplot(132)
imagesc(log_cut_2)
subplot(133)
imagesc(log_cut_3)
