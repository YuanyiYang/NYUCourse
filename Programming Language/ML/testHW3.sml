use "SMLHomework.sml";

intPartitionSort [3,5,1,8,4];
partitionSort (op <) [1,9, 3, 6, 7];	
partitionSort (fn(a,b) => length a < length b) [[1, 9, 3, 6], [1], [2,4,6], [5,5],[]];
val myTree = node [
node [node [leaf [4,2,14],leaf [9,83,32],leaf [96,123,4]],
	  node [leaf [47,71,82]],
	  node [leaf [19,27,10],leaf [111,77,22,66]],
	  leaf [120,42,16]],
node [],
leaf [83,13],
leaf []];
sortTree (op <) myTree;
sortTree (op <) (node [leaf [4,2,3,1], leaf [7,2,5,0]]);
merge (op <) [] [];
merge (op >) [2,4,6,8] [1,3,5,7];
merge (fn (a,b) => a > b) [8,6,4,2] [7,5,3,1];
mergeTree (op <) myTree;
mergeTree (op >) myTree;