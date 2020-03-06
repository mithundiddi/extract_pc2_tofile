'''
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * MIT License                                                             *
 * @author     Mithun Diddi <diddi.m@husky.neu.edu>                       *
 * @website    https://mithundiddi.com                                     *
 * @copyright (c) 2020, Mithun Diddi                                       *
 *                                                                         *
 * Permission is hereby granted, free of charge, to any person obtaining   *
 * copy of this software and associated documentation files                *
 * (the "Software"), to deal in the Software without restriction,          *
 * including *without limitation the rights to use, copy, modify, merge,   *
 * publish, distribute, sublicense, and/or sell copies of the Software,    *
 * and to permit persons to whom the Software is furnished to do so,       *
 * subject to the following conditions:                                    *
 *                                                                         *
 * The above copyright notice and this permission notice shall be included *
 * in all copies or substantial portions of the Software.                  *
 *                                                                         *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS *
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF              *
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  *
 *                                                                         *
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR        *
 * ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF          *
 * CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH *
 * THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.              *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
'''
'''
converts the pointcloud2 msg in rosbag file into a text file with fields x,y,z,intensity

needs rosbag file  name, and pc2_topic, follow arg parse help

optionally can specify :number of msgs to parse,start_time, end_time in rosbag
'''

#! /usr/bin/env python

from rosbag import Bag
import sensor_msgs.point_cloud2 as pc2
import traceback
import argparse
import os

def writepc2frombag2file(input_bagfile, pc2_topic, out_file_path,start_time=None, end_time=None, msg_count=None):
    try:
        output_file_name = get_output_file_name(input_bagfile) + '_xyz.txt'
        if out_file_path.endswith('/'):
            output_file = out_file_path + output_file_name
        else:
            output_file = out_file_path+'/' +  output_file_name
        
        output_file_fh = open(output_file,'w')
        print('writing output_file at', output_file)

        # check start and end time condition 
        if start_time is not None and end_time is not None:
            assert (end_time - start_time) > 0 , "end_time should be higher than start time"

        if msg_count is None:
            use_msg_count = False
        else:
            use_msg_count = True
            # msg_count is already static casted in arg parse, just checking again for sanity ad if function is re used individially
            msg_count = int(msg_count)
            assert msg_count > 0, "should have positive msg_count"
        
        input_bag = Bag(input_bagfile,'r')
        print('bag load success')
        
        count = 0;
        for topic, msg, ts in input_bag.read_messages(topics=[pc2_topic],start_time=start_time, end_time=end_time):

            output_file_fh.write('msg_timestamp: %f\n' % msg.header.stamp.to_sec())
            output_file_fh.write('%d\n' %msg.width)
            for data_pts in pc2.read_points(msg, field_names=("x", "y", "z", "intensity"), skip_nans=True):
                output_file_fh.write('%f %f %f %d\n' % (data_pts[0], data_pts[1], data_pts[2], data_pts[3]))
            
            count +=1
            print(count,msg_count)         
            if use_msg_count and count >= msg_count:
                break

        input_bag.close()
        output_file_fh.close()

    except Exception as e_init:
        print(traceback.format_exc(e_init))

def get_output_file_name(inputbagpath):
    return os.path.basename(inputbagpath.split('.bag')[0])

def get_ouput_path(inputbagpath):
    return os.path.dirname(os.path.expanduser(inputbagpath))
 

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Extract x,y,z,i values of pc2 msg in ros bag into a text file')
        parser.add_argument('-i','--inputbag',required=True, help='input bag file')
        parser.add_argument('-t', '--pc2_topic', required=True,
                            help='PointCloud2 topic')
        parser.add_argument('-o','--outputfilepath',
                            help='output txt file with x,y,z,intensity  values, file path is optional, creates a file in input bag path if not provided')        
        parser.add_argument('-s', '--start_time', type=float, help='optional bag start_time')
        parser.add_argument('-e', '--end_time',type=float, help='optional msg end_time')
        parser.add_argument('-c', '--msg_count',type=int, help='optional msg_count')
        args = parser.parse_args()

        if args.outputfilepath is None:
            outputfilepath=get_ouput_path(args.inputbag)
        else:
            outputfilepath = os.path.expanduser(args.outputfilepath)

        writepc2frombag2file(input_bagfile=args.inputbag, pc2_topic=args.pc2_topic, out_file_path=outputfilepath, start_time=args.start_time, end_time=args.end_time, msg_count=args.msg_count)

    except Exception as e_main:
        print(traceback.format_exc(e_main))