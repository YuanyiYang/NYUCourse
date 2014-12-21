with Ada.Text_io,Ada.Integer_Text_io;
use Ada.Text_io,Ada.Integer_Text_io;
package hw1 is
	subtype array_index is integer range 1..30;
	type input_array is array(array_index) of integer;
	in_array : input_array;
	res_array : input_array;
	index: integer:=1;
	procedure generateRandom; -- generate an array of 30 integers as the input
	procedure getUserInput;
	array_outOfBound : exception;
end hw1;