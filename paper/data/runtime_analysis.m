clear all;
slave1 = load('simple/stat_slave_1_1.out');
slave2 = load('simple/stat_slave_2_1.out');
slave3 = load('simple/stat_slave_3_1.out');
slave4 = load('simple/stat_slave_4_1.out');
simple = [slave1(2500:length(slave1),:); 
          slave2(2500:length(slave2),:); 
          slave3(2500:length(slave3),:); 
          slave4(2500:length(slave4),:)];
runtime1 = simple(:,1) - simple(:,2);

slave1 = load('cloud-cache/stat_slave_1_1.out');
slave2 = load('cloud-cache/stat_slave_2_1.out');
slave3 = load('cloud-cache/stat_slave_3_1.out');
slave4 = load('cloud-cache/stat_slave_4_1.out');
ccache = [slave1; slave2; slave3; slave4];
runtime2 = ccache(:,1) - ccache(:,2);

[r1, x1] = ecdf(runtime1);
[r2, x2] = ecdf(runtime2);


figure(1); hold on;
plot(x1, r1, '-r', 'linewidth', 2);
plot(x2, r2, '-b', 'linewidth', 2);
axis([0 5 0 1]);
grid on;
set(gca, 'fontsize', 14);
xlabel('Problem Solving Time (second)');
ylabel('CDF');
legend('Brute-force solution', 'CloudCache Framework');
hold off;

% slave = sortrows(simple, 1);
% length(slave)
% 
% task = [0];
% start = 1367334283;
% k = 1
% t = 0
% for i = 1:length(slave)
%     if slave(i,1) < start + 300
%         task(k) = task(k) + (slave(i,1) - slave(i,2));
%         t = t + 1;
%     else
%         task(k) = task(k)/t;
%         t = 0;
%         start = start + 300;
%         k = k + 1;
%         task = [task 0];
%     end
% end
% figure(2);
% plot(1:length(task), task)
% axis([0 length(task)-10 0 0.5])