tool_dir="/home/mjl/DataSet/convert2Yolo"
py_file="${tool_dir}/example.py"
names="${tool_dir}/voc.names"
manifast_file="./manifast.txt"
datasets=VOC
root_dir=
img_type=
convert_output_path=

if [ -f ${manifast_file} ];then
	rm -f ${manifast_file}
fi

if [ "$#" -ne 2 ];then
	echo "usage $0 <root_dir> <img_type>"
	echo "notice to run this sh, u should have mjfind and lsdir sh"
	echo "notice xml name should be same with png/jpg name"
	exit 1
fi

if [ ! -d $1 ];then
	echo "usage $0 <root_dir> <img_type>"
	python /home/mjl/DataSet/convert2Yolo/example.py -h
## TODO
	echo "more see $0 -h for help"
	exit 1
fi

root_dir=$1
img_type="."$2

for file in `lsdir ${root_dir}`;do
	convert_output_path=${file}
	python ${py_file} --datasets ${datasets} --img_path ${file} --label ${file} --convert_output_path ${convert_output_path} --img_type ${img_type} --cls_list_file ${names}
done

if [ "${datasets}" == "VOC" ];then
	xml=`mjfind ls ${root_dir} xml | wc -l`
	txt=`mjfind ls ${root_dir} txt | wc -l`

	echo "success convert ${txt} xml to txt, $((${xml} - ${txt})) convert failed"
fi
