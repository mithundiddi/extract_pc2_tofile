# lidarpc2_tofile

extract pc2 msgs into x,y,z,Intensity values and write them to a text file

usage: python extract_pc2_into_file.py [-h] -i INPUTBAG -t PC2_TOPIC
                                [-o OUTPUTFILEPATH] [-s START_TIME]
                                [-e END_TIME] [-c MSG_COUNT]


optional args [-o OUTPUTFILEPATH] [-s START_TIME] [-e END_TIME] [-c MSG_COUNT]

example:

Minimum args example

``` bash
$ python extract_pc2_into_file.py -i <rosabag file fullpath>.bag -t /ns1/velodyne_points
```
Save output file in home directory and parse only 5 pointcloud2 msgs from starting time of bag.
```bash
$ python extract_pc2_into_file.py -i <rosabag file fullpath>.bag -t /ns1/velodyne_points -o ~/ -c 5
```
