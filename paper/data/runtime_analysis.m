clear all;
slave1 = load('stat_slave_1.out');
slave2 = load('stat_slave_2.out');
slave3 = load('stat_slave_3.out');
slave4 = load('stat_slave_4.out');

runtime1 = slave1(:,1) - slave1(:,2);
runtime2 = slave2(:,1) - slave2(:,2);
runtime3 = slave3(:,1) - slave3(:,2);
runtime4 = slave4(:,1) - slave4(:,2);


[r1, x1] = ecdf(runtime1*1000);
[r2, x2] = ecdf(runtime2*1000);
[r3, x3] = ecdf(runtime3*1000);
[r4, x4] = ecdf(runtime4*1000);

figure(1); hold on;
plot(x1, r1, '-r', 'linewidth', 2);
plot(x2, r2, '-b', 'linewidth', 2);
plot(x3, r3, '-g', 'linewidth', 2);
plot(x4, r4, '-m', 'linewidth', 2);
axis([0 1000 0 1]);