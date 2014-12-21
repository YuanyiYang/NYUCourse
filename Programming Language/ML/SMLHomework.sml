Control.Print.printDepth := 100;
Control.Print.printLength := 100;

fun partition pivot [] = ([], []) 
|   partition pivot (x::xs) = 
	let 
		val (left, right) = partition pivot xs
	in 
		if x < pivot then (x::left, right)
		else (left, x::right)
	end

fun intPartitionSort [] = []
	| intPartitionSort (pivot::xs) = 
		let
			val (left, right) = partition pivot xs
		in
			(intPartitionSort left) @ [pivot] @ (intPartitionSort right)
		end

fun alphaPartition (op <) pivot [] = ([], [])
	| alphaPartition (op <) pivot (x::xs) = 
	let 
		val (left, right) = alphaPartition (op <) pivot xs
	in
		if x < pivot then (x::left, right)
		else (left, x::right)
	end

fun partitionSort (op <) [] = []
	| partitionSort (op <) (pivot::xs) = 
		let 
			val (left, right) = alphaPartition (op <) pivot xs
		in 
			(partitionSort (op <) left) @ [pivot] @ (partitionSort (op <) right)
		end

datatype 'a tree = leaf of 'a | node of 'a tree list

fun sortTree (op <) (leaf children) = leaf (partitionSort (op <) children)
| 	sortTree (op <) (node []) = node []
| 	sortTree (op <) (node (n::nodes)) = node (map (sortTree (op <)) (n::nodes))

fun merge _ [] [] = []
|	merge _ (x::xs) [] = (x::xs)
|	merge _ [] (y::ys) = (y::ys)
|	merge (op <) (x::xs) (y::ys) =  
	if x < y then (x::(merge (op <) xs (y::ys)))
	else (y::(merge (op <) (x::xs) ys))

fun fringe (leaf x) = [x]
|	fringe (node []) = []
|	fringe (node (n::nodes)) = fringe n @ fringe (node nodes)

fun myfoldr _ b [] = b
|	myfoldr (op <) b (x::xs) = (op <) x (myfoldr (op <) b xs)

(*sort the tree and merge the list of leaf*)

fun mergeTree (op <) tree = 
	let 
		val sortedTree = sortTree (op <) tree
	in 
		myfoldr (merge (op <)) [] (fringe sortedTree)
	end
