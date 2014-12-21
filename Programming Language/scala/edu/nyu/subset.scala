package edu.nyu

class Vehicle(s: Int=0){
  val speed: Int = s
}
class Plane(s: Int=1, l: Int=1) extends Vehicle(s: Int){
  val latitude: Int = l
}

object subset {
  def foo(p: Plane): Unit = {
      println("The speed of plane is " + p.speed);
      println("The latitude of plane is " + p.latitude);
  }
  def bar(v: Vehicle): Unit = {
      println("The speed of vehicle is " + v.speed)
  }
  def f(g:Plane=>Unit, p:Plane): Unit = {
    g(p)
  }
  def main(args:Array[String]){
    f(bar, new Plane());
  }
}
