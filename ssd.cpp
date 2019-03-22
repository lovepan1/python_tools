// Tencent is pleased to support the open source community by making ncnn available.
//
// Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
//
// Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
// in compliance with the License. You may obtain a copy of the License at
//
// https://opensource.org/licenses/BSD-3-Clause
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.

#include <stdio.h>
#include <vector>
#include "net.h"
#include "opencv/cv.hpp"
using namespace cv;

long st_ncnn_initLib(char *model_path, char *prototxt_path)
{
    ncnn::Net *ssd = new ncnn::Net();
	if(!ssd)
		return 0;

	ssd->load_param(prototxt_path);
	ssd->load_model(model_path);

	return (long )ssd;
}

int st_ncnn_process(long handle, cv::Mat& img, int width, int height)
{
	printf("%s  %d\n", __func__, __LINE__);
	ncnn::Net *ssd = (ncnn::Net *)handle;
	if(!ssd)
		return -1;
    const float mean_vals[3] = {127.5f, 127.5f, 127.5f};
    const float norm_vals[3] = {1.0/127.5,1.0/127.5,1.0/127.5};

    ncnn::Extractor ex = ssd->create_extractor();
	cv::Mat dst = img.clone();
    ncnn::Mat in = ncnn::Mat::from_pixels_resize(img.data, ncnn::Mat::PIXEL_BGR, width, height, 300, 300);
    in.substract_mean_normalize(mean_vals, norm_vals);
    ex.input("data", in);
    ncnn::Mat out;
	printf("%s  %d\n", __func__, __LINE__);
    ex.extract("detection_out",out);
	printf("%s  %d  %d  %d\n", __func__, __LINE__, out.h, out.w);
    for (int i=0; i<out.h; i++)
    {
        
		const float* values = out.row(i);
        int label = values[0];
        float score = values[1];
		int x = values[2] * width;
        int y = values[3] * height;
        int x1 = values[4] * width;
        int y1 = values[5] * height;
		if(score > 0.60)
		{
			cv::rectangle(dst, Point(x,y), Point(x1,y1), 1, 4);	
      	printf("%s  %d i: %d  h: %d  label: %d  score: %f\n", __func__, __LINE__, i, out.h, label, score);
		}
	}
	cv::imshow("dst", dst);
	cv::waitKey(0);
	return 0;
}

int st_ncnn_deinitLib(long handle)
{
	ncnn::Net *ssd = (ncnn::Net *)handle;
	if(!ssd)
		return -1;
	ssd->~Net();
	return 0;
}


int main(int argc, char **argv)
{

	long handle = st_ncnn_initLib((char*)"caffe_mobilenet_ssd_20190305.bin", (char*)"caffe_mobilenet_20190305.param");
//	long handle = st_ncnn_initLib((char*)"dianli.bin", (char*)"dianli.param");
	if(handle == 0)
	{
		printf("st_ncnn_initLib error\n");
		return -1;
	}

	cv::Mat img = cv::imread(argv[1], -1);
	if(img.empty())
		return -1;

	//resize(img, img, Size(512,512));
	cv::imshow("org", img);
	cv::waitKey(0);
		
	st_ncnn_process(handle, img, img.cols,img.rows);
	st_ncnn_deinitLib(handle);
	return 0;
}
