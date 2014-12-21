
package body reviseQuickSort is 
	
	--subtype workingTask_sub is workingTask;
	--main_task : task_pointer;
	package int_io is new integer_io(integer);
	use int_io;

	--task body workingTask is
			--pivot : integer;
			-- left : task_pointer;
			-- right: task_pointer;
		--begin
		--if begin_index<end_index then
				--pivot := partition(begin_index,end_index);
				-- if begin_index<end_index then
				-- 	quicksort(begin_index=>begin_index,end_index=>end_index);
				-- end if;
				-- if pivot<end_index then
				-- 	right := new workingTask_sub(begin_index=>pivot,end_index=>end_index);
				-- end if;
			--end if;
		--end workingTask;
		
	procedure quicksort(begin_index:integer; end_index:integer) is
		newPivot:integer;
		-- left : task_pointer;
		-- right: task_pointer;
		procedure helper(begin_index:integer;end_index:integer; pivot:integer) is

			task left;
			task right;

			task body left is 
				begin
					if begin_index<pivot-1 then 
						quicksort(begin_index, pivot-1);
					end if;
				end left;

			task body right is 
				begin
					if pivot<end_index then
						quicksort(pivot,end_index);
					end if;
				end right;

			begin
				null;
				--left := new workingTask(begin_index=>begin_index,end_index=>pivot-1);
				--right := new workingTask(begin_index=>pivot,end_index=>end_index);
			end helper;

		begin
			newPivot := partition(begin_index,end_index);
			helper(begin_index=>begin_index,end_index=>end_index,pivot=>newPivot);
		end quicksort;

	procedure initArray(in_array : input_array) is
		
		begin
			sort_array := in_array;
			-- main_task := new workingTask(begin_index=>1,end_index=>30);
			-- delay(3.0);
		end initArray;		

	function partition(begin_index:integer;end_index:integer) return integer is
		
		m : integer;
		pivot:integer;
		mid_index :integer := (begin_index+end_index)/2;
		i : integer := begin_index;
		j : integer := end_index;
		temp:integer;

		begin
			if (mid_index=begin_index) then
				if(sort_array(mid_index)>sort_array(end_index)) then
					m := sort_array(end_index);
				else	
					m := sort_array(begin_index);
				end if;
			else
				m := (sort_array(begin_index)+sort_array(mid_index)+sort_array(end_index))/3;
			end if;
			while i<=j
				loop
					while sort_array(i) < m
						loop
							i := i+1;
						end loop;
					while sort_array(j) > m
						loop
							j := j-1;
						end loop;
					if i<=j then
						temp:=sort_array(i);
						sort_array(i):=sort_array(j);
						sort_array(j):=temp;
						i:=i+1;
						j:=j-1;
					end if;
				end loop;
			pivot:=i;
			return pivot;
		end partition;

		function getArray return input_array is 
		out_Array : input_array;
		begin
			out_Array:=sort_array;
			return out_Array;
		end getArray;

end reviseQuickSort;