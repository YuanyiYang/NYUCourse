package hw1_sem is 
	task semaphore is 
		entry lock;
		entry unlock;
		entry quit;
	end semaphore;
end hw1_sem;