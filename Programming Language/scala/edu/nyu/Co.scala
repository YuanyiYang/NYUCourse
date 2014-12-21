package edu.nyu

class NodeA(a:Integer=0) {
  val x = a
  override def toString() = "A<" + x + ">"
}

class NodeB(a:Integer=0, b:Integer=0) extends NodeA(a) {
  val y = b
  override def toString() = "B<" + x + "," + y + ">"
}

class CoStack[+T] {
  
  def push[E>:T](x:E): CoStack[E] = new CoStack[E] {
    override def top: E = x
    override def pop: CoStack[E] = CoStack.this
    override def toString() = x.toString + " " + CoStack.this.toString()
  }
  def top: T = throw new Exception()
  def pop: CoStack[T] = throw new Exception()
  override def toString() = ""
}

class ContraStack[-T] {
  def push[E<:T](x:T): ContraStack[T] = new ContraStack[T]{
    override def top: T = x
    override def pop: ContraStack[T] = ContraStack.this
    override def toString() = x.toString + " " + ContraStack.this.toString()
  }
  def top: Any = throw new Exception()
  def pop: ContraStack[T] = throw new Exception()
  override def toString() = ""
}
object test {
  
  def test() {
    var p : ContraStack[NodeB] = new ContraStack()
    var c : ContraStack[NodeA] = new ContraStack()
    p = p.push(new NodeB())
    println(p)
    c = c.push(new NodeA())
    println(c.push(new NodeB(1,2)))
  }
  
  def main(args:Array[String]){
    test()
    /*
     var p: CoStack[NodeA] = new CoStack()
     var c: CoStack[NodeB] = new CoStack()
     p = p.push(new NodeA())
     println(c.push(new NodeA(1)))
     println(p)
     */
  }
}