with hw1;
with text_io;
with hw1_sem;
use text_io;
use hw1;
use hw1_sem;
with reviseQuickSort;
use reviseQuickSort;

procedure testhw1 is
	package int_io is new integer_io(integer);
	use int_io;
	task printer is 
		entry inputDone;
		entry sorterDone;
		entry adderDone(total: In integer);
		entry stop;
	end printer;
	task adder is 
		entry sorterDone;
	end adder;
	task sorter is
		entry printerDone;
	end sorter;

	task body printer is
		begin
			accept inputDone do
				put_line("The printer is printing the original array: ");
				for i in in_array'First..in_array'Last loop
					put(in_array(i));
					new_line;
				end loop;
				sorter.printerDone;
			loop 
				select
					accept sorterDone do
						put_line("The printer is printing sorted array: ");
						for i in res_array'First..res_array'Last loop
							put(res_array(i));
							new_line;
						end loop;
					end sorterDone;
					accept adderDone(total: In integer) do
						put_line("The printer is printing the total value: ");
						put(total);
					end adderDone;
				or
					accept stop;
					semaphore.lock;
					semaphore.quit;
					exit;
				else
				    null; 
				end select;
			end loop;	
		end inputDone;
	end printer;

	task body adder is
		total:integer:=0;
		begin
			accept sorterDone;
			semaphore.lock;
			for i in in_array'First..in_array'Last loop
					total:=total+in_array(i);
				end loop;
			semaphore.unlock;
			printer.adderDone(total=>total);
			printer.stop;
	end adder;

	task body sorter is 
		begin
			accept printerDone do
				reviseQuickSort.initArray(in_array);
				reviseQuickSort.quicksort(begin_index=>1,end_index=>30);
				res_array:=reviseQuickSort.getArray;			
			end printerDone;
				printer.sorterDone;
				adder.sorterDone;
	end sorter;

begin
	--hw1.generateRandom;
	getUserInput;
	printer.inputDone;
	exception 
		when array_outOfBound =>
			put("You have more than 30 numbers in the array!");new_line;
end testhw1;