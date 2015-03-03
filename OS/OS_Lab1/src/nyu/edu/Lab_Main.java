package nyu.edu;

import java.io.File;
import java.io.IOException;

public class Lab_Main {
  public static void main(String[] args) {
    if (args.length != 1) {
      System.err.println("Error! Usage: Lab_Main <input filename>");
      System.exit(1);
    }
    String filename = args[0];
    File inputFile = new File(filename);
    if (!inputFile.exists()) {
      System.err.println("Error! Input file does not exist");
      System.exit(1);
    }
    Lab_Module module = new Lab_Module(inputFile);
    try {
      module.firstScanner();
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
    module.printSymbolTable();
    module.secondScanner();
  }
}
