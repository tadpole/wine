data_path := data/cluster_caffe/cluster_$(NUM)
lmdb := $(data_path)/*_lmdb
compute_mean := /home/tuke/raid/tools/caffe/build/tools/compute_image_mean
generate_train_val: src/generate_train_val_by_cluster.py
	python $< $(NUM)
create: caffe/create_wine.sh
	sh $< $(NUM)
mean: $(data_path)/wine_train_lmdb
	$(compute_mean) $< $(data_path)/wine_mean.binaryproto
push: $(data_path)/wine_*_lmdb $(data_path)/wine_mean.binaryproto
	ls -d $(lmdb) | xargs -i scp -r {} GPUServer:/data/tuke/caffe_clusters_$(NUM)/
	scp $(data_path)/wine_mean.binaryproto GPUServer:/data/tuke/caffe_clusters_$(NUM)/

.PHONY: clean-lmdb
clean-lmdb:
	rm data/cluster_caffe/cluster_$(NUM)/*_lmdb -r
