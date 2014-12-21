with text_io;
with Ada.Numerics.Discrete_Random;
use text_io;

package body hw1 is
	package int_io is new integer_io(integer);
	use int_io;	
		
	procedure generateRandom is
		type Rand_Range is range 1..1000;
		package Rand_Int is new Ada.Numerics.Discrete_Random(Rand_Range);
		seed:Rand_Int.Generator;
		Num:Rand_Range;
	begin
		for i in 1..30 loop
			if(index>30) then
				raise array_outOfBound;
			else 
				Rand_Int.Reset(seed);
				Num:=Rand_Int.Random(seed);
				in_array(index):=Integer'Value(Rand_Range'Image(Num));
				index:=index+1;
			end if;
		end loop;		
	end generateRandom;

	procedure getUserInput is
		x:integer;
		begin
			for i in 1..30 loop
				--put("Please input the ");int_io.put(i);put_line(" number");
				int_io.get(Item=>x);
				in_array(i):=x;
			end loop;
		end getUserInput;
end hw1;
