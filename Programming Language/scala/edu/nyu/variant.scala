package edu.nyu

class One(a:Integer=0) {
  val x = a
  override def toString() = "One: " + x
}

class Two(a:Integer=0, b:Integer=0) extends One(a) {
  val y = b
  override def toString() = "Two: " + x + ", " + y
}

class MyList[+T](lis: List[T]) {
  val l: List[T] = lis
  def get = l

  def cons[B >: T](x: B): MyList[B] = new MyList[B](x :: lis)
  //def cons(x:T): MyList[T] = new MyList[T](x::lis)
  def hd = l match {
    case (x :: xs) => x
    case List() => throw new Exception()
  }

  def tl = l match {
    case (x :: xs) => xs
    case List() => throw new Exception()
  }

  override def toString() = l + ""

}

object variant{
  def foo(l:MyList[One]){
    println(l)
  }
  
  def main(args:Array[String]){
    //val l1 = new MyList(List(new One()))
    val l1 = new MyList(List(new One()))
    val hd1: One = l1.hd 
    foo(l1)
    //println(hd1)
    val l2 = new MyList(List(new Two()))
    foo(l2)
    //val hd2:One = l2.hd
    //println(hd2)
  }
}