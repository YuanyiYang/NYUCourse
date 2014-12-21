package edu.nyu

abstract class Tree[T <: Ordered[T]]  

case class Node[T <: Ordered[T]](v: T, l: Tree[T], r: Tree[T]) extends Tree[T] 

case class Leaf[T <: Ordered[T]](v: T) extends Tree[T] 


class myInt(x: Int) extends Ordered[myInt] {
  val value = x
  def compare(other:myInt) : Int = value.compareTo(other.value)
  override def toString(): String = value.toString()
}

class myString(x: String) extends Ordered[myString] {
  val value = x
  def compare(other:myString) : Int = value.compareTo(other.value)
  override def toString(): String = value.toString()
}

object Pat {
  
  val leaf = Leaf(new myInt(4))
  val myTree = Node(new myInt(10),Leaf(new myInt(4)),Node(new myInt(5),Leaf(new myInt(6)),Leaf(new myInt(7))))
  val yourTree = Node(new myString("3"), Leaf(new myString("4")), Node(new myString("5"), Leaf(new myString("6")), Leaf(new myString("7"))))
  
  def getBigest[T <: Ordered[T]](t : Tree[T]) : T = {
     t match {
       case Leaf(other_v) => other_v
       case Node(v,l,r) => {
         val lRes = getBigest(l);
         val rRes = getBigest(r);
         var temp = largest(v,lRes);
         temp = largest(temp,rRes);
         temp;
       }
     }
  }
  
  def largest[T<:Ordered[T]](l1:T, l2:T) : T = {
    if(l1.compareTo(l2)>0) l1
    else l2
  }    
  
  
  def printTree[T<:Ordered[T]](t: Tree[T]) {
    t match {
      case Node(v, l, r) =>
        print("( "); printTree(l); print(", "); print(v); print(", "); printTree(r);
        print(" )");
      case Leaf(v) => print(v);
    }
  }
  
  def main(args: Array[String]) {
    println(getBigest(yourTree))
    println(getBigest(myTree))
    println(getBigest(leaf))
    //printTree(myTree);
    //printTree(yourTree);
  }
}

