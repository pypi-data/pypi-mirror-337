# VERTEX: Accelerated fMRI Functional Connectivity Tools
VERTEX is a a python for functional connectivity analysis at the voxel / vertex level that utilizes pytorch for GPU speed ups and scipy sparse matrices for memory savings.

# Tools:
	[] list tools: vFC tools
	[] clustering methods:
		[] PM: infomaps - for individual parcellations
		[] PM: with other clustering techniques
		[] PM: integrate with Sparse-Low Rank Clustering


# Acceleration Effects:
Comparisons are with `wb_command` package (~~version~~):

### Time Speed Up
	[] Creating dconns:
	[] Creating sparse dconns:
	[] Dconn comparisons

### Memory Savings
	[] Creating dconns
	[] Sparse dconns
	[] Dconn comparisons

### Storage Savings
	[] Sparse dconns
	[] Dconn comparisons

# TODO:
	[] plots:
		[] migrate SFM plotting script into this -> dont want to have plots - less clean, just output ciftis
	[] benchmarking
		[] create time benchmark plots for devices
		[] benchmark script:
			[] runs on machine: records time of set functions
			[] outputs: pkl with memory over time, time to run each function, device info
			[] plots: 
	[] main:
		[] vFC sparsity
		[] vFC thresholded
		[] vFC compare: 
