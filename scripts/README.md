

## Installing `cpupower` and `perf`

cd to linux source tree and the folder `tools`

```shell
sudo make cpupower_install
sudo make perf_install
```

## Collecting page fault trace

```shell
sudo ~/bin/perf trace -F all -o \
	./vpm-50-1-1-extraOPS9-nowarmup-noftouch-50-nopdf-flatstore-ph-etc/pm-pf-trace-withtimestamp-perf.log \
	./eval_etc.sh 2 1 \
	&> ./vpm-50-1-1-extraOPS9-nowarmup-noftouch-50-nopdf-flatstore-ph-etc/pm-pf-trace-withtimestamp.log
```

## Evaluating Init Phase

Run experiments.

```shell
./vpm eval init run
```

Analyze data.

```shell
./vpm eval init draw
```

