package nyu.edu;

public class Lab_Token {

  int line_num;
  int offset;
  String str;

  Lab_Token(int line_num, int offset, String str) {
    this.line_num = line_num;
    this.offset = offset;
    this.str = str;
  }
  
  @Override
  public String toString(){
    return "Token: "+ str + " at "+ line_num + " line position " + offset;
  }
}
