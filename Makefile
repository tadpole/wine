data_path := data/cluster_caffe/cluster_$(NUM)
lmdb := $(data_path)/wine_train_lmdb $(data_path)/wine_val_lmdb
train_val := $(data_path)/train.txt $(data_path)/val.txt
compute_mean := /home/tuke/raid/tools/caffe/build/tools/compute_image_mean
mean := $(data_path)/wine_mean.binaryproto

create: $(train_val)
$(train_val): src/generate_train_val_by_cluster.py
	python $< $(NUM)
$(lmdb): caffe/create_wine.sh $(train_val)
	sh $< $(NUM)
$(mean): $(data_path)/wine_train_lmdb
	$(compute_mean) $< $@
push: $(lmdb) $(mean)
	for i in $^; do scp -r $$i GPUServer:/data/tuke/caffe_clusters_$(NUM)/; done

.PHONY: clean-lmdb create
clean-lmdb:
	rm data/cluster_caffe/cluster_$(NUM)/*_lmdb -r
