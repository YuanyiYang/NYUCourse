package edu.nyu

class Contra[-T]() {
  var v : List[Any] = List()
  def insert(x:T){
    v = x :: v
  }
  
  override def toString() = {
    def elementsToString(l:List[Any]) : String = l match {
      case List() => ""
      case (x::xs) => x.toString() + " " + elementsToString(xs)
    }
    "Contra[" + elementsToString(v) + "]"
  }
}

class newA(x:Integer=0) {
  override def toString() = "A<" + x + ">"
}

class newB(x:Integer=0, y:Integer=0) extends newA(x) {
  override def toString() = "B<" + x + "," + y + ">"
}

class newC(x:Integer=0, z:Integer=0) extends newA(x) {
  override def toString() = "C<" + x + "," + z + ">"
}

object foo {
  def test(m:Contra[newB], z:newB){
    m.insert(z)
  }
  
  def main(args:Array[String]){
    val la = new Contra[newA]()
    val lb = new Contra[newB]()
    val lc = new Contra[newC]()
    la.insert(new newB())
    la.insert(new newC())
    println(la)
  }
}

