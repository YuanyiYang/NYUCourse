package edu.nyu

class OInt(x: Int) extends Ordered[OInt] {
  val value = x
  def compare(that: OInt) = this.value - that.value
  override def toString(): String = "<" + x + ">"
}

abstract class OTree[T <: Ordered[T]] extends Ordered[OTree[T]]

case class OLeaf[T <: Ordered[T]](v: T) extends OTree[T] {
  def compare(other: OTree[T]) =
    other match {
      case OLeaf(other_v) => this.v.compare(other_v)
      case _ => -1
    }
}

case class ONode[T <: Ordered[T]](lis: List[OTree[T]]) extends OTree[T] {
  def compare(other: OTree[T]) =
    other match {
      case ONode(other_lis) => compareTreeList(lis, other_lis)
      case OLeaf(other_v) => 1
    }

  def compareTreeList(current: List[OTree[T]], other: List[OTree[T]]): Int = {
    (current, other) match {
      case (x :: xs, y :: ys) => {
        val res = x.compare(y)
        if (res != 0) {
          return res
        } else {
          return compareTreeList(xs, ys)
        }
      }
      case (List(), List()) => 0
      case (List(), (y :: ys)) => -1
      case ((x :: xs), List()) => 1
    }
  }
}

object Part2 {

  def compareTrees[T <: Ordered[T]](l: OTree[T], r: OTree[T]) = {
    val res = l.compare(r);
    if (res == 0) {
      println("Equal")
    } else if (res > 0) {
      println("Greater")
    } else {
      println("Less")
    }
  }
  def test() {

    val tree1 = ONode(List(OLeaf(new OInt(6))))

    val tree2 = ONode(List(OLeaf(new OInt(3)),
      OLeaf(new OInt(4)),
      ONode(List(OLeaf(new OInt(5)))),
      ONode(List(OLeaf(new OInt(6)),
        OLeaf(new OInt(7))))));

    val treeTree1: OTree[OTree[OInt]] =
      ONode(List(OLeaf(OLeaf(new OInt(1)))))

    val treeTree2: OTree[OTree[OInt]] =
      ONode(List(OLeaf(OLeaf(new OInt(1))),
        OLeaf(ONode(List(OLeaf(new OInt(2)),
          OLeaf(new OInt(2)))))))

    print("tree1: ")
    println(tree1)
    print("tree2: ")
    println(tree2)
    print("treeTree1: ")
    println(treeTree1)
    print("treeTree2: ")
    println(treeTree2)
    print("Comparing tree1 and tree2: ")
    compareTrees(tree1, tree2)
    print("Comparing tree2 and tree2: ")
    compareTrees(tree2, tree2)
    print("Comparing tree2 and tree1: ")
    compareTrees(tree2, tree1)
    print("Comparing treeTree1 and treeTree2: ")
    compareTrees(treeTree1, treeTree2)
    print("Comparing treeTree2 and treeTree2: ")
    compareTrees(treeTree2, treeTree2)
    print("Comparing treeTree2 and treeTree1: ")
    compareTrees(treeTree2, treeTree1)

  }

  def main(args: Array[String]) {
    test()
  }
}