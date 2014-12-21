with hw1;
use hw1;
with text_io;
use text_io;

package reviseQuickSort is 
	--task type workingTask(begin_index:integer; end_index:integer);
	--type task_pointer is access workingTask;
	sort_array : input_array;
	procedure initArray(in_Array : input_array);
	function partition(begin_index:integer; end_index:integer) return integer;
	function getArray return input_array; 
	procedure quicksort(begin_index:integer; end_index:integer);
end reviseQuickSort;