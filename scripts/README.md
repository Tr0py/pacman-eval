
## Virtualization overhead

Run the experiments using

```
./vpm-eval-etc.sh ./eval_baseline.sh <config>
```

Here, we ran 5 configs, all using Linux 6.1:
1. eval_pmbaseline_xfs_v5_4k: XFS DAX with 4K pages only. Set `PMEM_DEV_NOT_USING_PMD` in Linux kernel.
2. eval_pmbaseline_xfs_v5_2m: XFS DAX with 2M pages enabled. Default Linux kernel. Set `VPM_HUGE` in pacman.
3. eval_vpmbaseline_xfs_v5_4k_order0: VPM with 4K pages only. Set `PMEM_DEV_FORCE_4KB` in Linux kernel.  Unset `VPM_HUGE` in pacman.
4. eval_vpmbaseline_xfs_v5_4k_default: VPM with default Linux6.1 file THP policy, allocating up to 32K pages. Default Linux kernel. Set `VPM_HUGE` in pacman.
5. eval_vpmbaseline_xfs_v5_2m: VPM with 2M pages enabled, aggressively allocating 2M pages. Set `PMEM_DEV_AGGRESSIVE_2MB` in Linux kernel. Set `VPM_HUGE` in pacman.

Collect the data into csv file using

```
python3 ./collect_data.py  eval_pmbaseline_xfs_v5_4k eval_pmbaseline_xfs_v5_2m eval_vpmbaseline_xfs_v5_4k_order0 eval_vpmbaseline_xfs_v5_4k_default  eval_vpmbaseline_xfs_v5_2m
```

Draw the figure from the csv file:

```
python3 ./vpm-scripts.py  plot_throughput eval_pmbaseline_xfs_v5_4k_eval_pmbaseline_xfs_v5_2m_eval_vpmbaseline_xfs_v5_4k_order0_eval_vpmbaseline_xfs_v5_4k_default_eval_vpmbaseline_xfs_v5_2m_th
roughput.csv False "['PMEM-4K', 'PMEM-2M', 'VPM-4K', 'VPM-32K', 'VPM-2M']"
```

The figure is saved to `PMEM-4K_PMEM-2M_VPM-4K_VPM-32K_VPM-2M_throughput.pdf`.

The results should desmontrate that:
1. VPM-2M has competible performance as PMEM-2M.  They should have within 5% performance difference except PMEMRocksDB.
2. VPM-4K is faster than PMEM-4K.
3. VPM benefits from file mTHP optimizations in kernel: VPM-2M >= VPM-32K >= VPM-4K in throughput.
4. Larger page sizes result in higher throughput for most applications for both PMEM and VPM.

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

