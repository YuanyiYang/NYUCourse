with Ada.Text_io,Ada.Integer_Text_io;
use Ada.Text_io,Ada.Integer_Text_io;
package body hw1_sem is 
	task body semaphore is
		begin 
			loop 
				accept lock;
				select 
					accept unlock;
				or
					accept quit;
					exit;
				end select;
			end loop;
	end semaphore;
end hw1_sem;
