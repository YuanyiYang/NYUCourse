package nyu.edu;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Lab_Module {

  private final String SPLIT_PATTERN = "\\s+";
  private final String SYM_PATTERN = "^[a-zA-Z][a-zA-Z0-9]*$";
  private final String INT_PATTERN = "^[0-9]+$";
  private final String INSTRCTION_PATTERN = "[AEIR]";
  // private final String FOUR_DIGIT = "[0-9]{4}";

  private File inputFile = null;
  private BufferedReader bfReader;

  private int line_num = 0;
  private int defNum = -1;
  private int useNum = -1;
  private int textNum = -1;

  private int relativeAddr = 0;
  private int baseAddr = 0;

  private int moduleNum = 0;
  private List<Integer> modulesDefCount = new ArrayList<Integer>();
  private List<Integer> modulesBaseAddress = new ArrayList<Integer>();
  private List<Integer> modulesSize = new ArrayList<Integer>();

  private Map<Integer, List<String>> moduleDefList = new HashMap<Integer, List<String>>();
  private Map<Integer, List<String>> moduleUseList = new HashMap<Integer, List<String>>();

  private LinkedList<Lab_Token> tokenList = new LinkedList<Lab_Token>();

  private List<KVPair> symbolTable = new ArrayList<KVPair>();
  private List<KVPair> memoryMap = new ArrayList<KVPair>();

  public Lab_Module(File inputFile) {
    this.inputFile = inputFile;
    try {
      bfReader = new BufferedReader(new FileReader(inputFile));
    } catch (FileNotFoundException e) {

    }
  }

  public void firstScanner() throws IOException {
    String line = null;
    Lab_Token placeHolder = null;
    while ((line = bfReader.readLine()) != null) {
      line_num++;
      line = line.trim();
      if (line.isEmpty()) {
        placeHolder = new Lab_Token(line_num, 1, "PlaceHolder Token");
        continue;
      }
      String[] parameter = line.split(SPLIT_PATTERN);
      if (parameter.length == 0){
        placeHolder = new Lab_Token(line_num, 1, "PlaceHolder Token");
        continue;
      }
       
      int offset = 1;
      for (int i = 0; i < parameter.length; i++) {
        Lab_Token token;
        if (i == 0) {
          token = new Lab_Token(line_num, offset, parameter[i]);
        } else {
          offset = offset + parameter[i - 1].length() + 1;
          token = new Lab_Token(line_num, offset, parameter[i]);
        }
        tokenList.add(token);
      }
      placeHolder = new Lab_Token(line_num, offset
          + parameter[parameter.length - 1].length(), "PlaceHolder Token");
    }
    tokenList.add(placeHolder);
    bfReader.close();

    while (tokenList.size() > 1) {

      // process definition list
      Lab_Token token = tokenList.removeFirst();
      defNum = Integer.parseInt(token.str);
      if (tokenList.isEmpty()) {
        printParseErrorMessage(0, token.line_num, token.offset); // num_expected
      } else if (defNum > 16) {
        printParseErrorMessage(4, token.line_num, token.offset); // to_many_def
      } else {
        for (int i = 0; i < defNum; i++) {
          // inside the definition list
          token = tokenList.removeFirst();
          // parse error
          if (tokenList.isEmpty()) {
            printParseErrorMessage(1, token.line_num, token.offset); // sym_expected
          } else if (token.str.length() > 16) {
            printParseErrorMessage(3, token.line_num, token.offset); // symbol_long
          } else if (!token.str.matches(SYM_PATTERN)) {
            printParseErrorMessage(1, token.line_num, token.offset); // sym_expected
          }
          Lab_Token symbol_token = token;
          token = tokenList.removeFirst();

          if (tokenList.isEmpty() || !token.str.matches(INT_PATTERN)) { // num_expected
            printParseErrorMessage(0, token.line_num, token.offset);
          }
          relativeAddr = Integer.parseInt(token.str);
          symbolTable.add(new KVPair(symbol_token.str, relativeAddr + baseAddr,
              moduleNum + 1));
        }
      }

      // process use list

      token = tokenList.removeFirst();
      useNum = Integer.parseInt(token.str);
      if (tokenList.isEmpty()) {
        printParseErrorMessage(0, token.line_num, token.offset);
      } else if (useNum > 16) {
        printParseErrorMessage(5, token.line_num, token.offset);
      } else {
        for (int i = 0; i < useNum; i++) {
          token = tokenList.removeFirst();
          if (tokenList.isEmpty()) {
            printParseErrorMessage(1, token.line_num, token.offset);
          } else if (token.str.length() > 16) {
            printParseErrorMessage(3, token.line_num, token.offset); // symbol_long
          } else if (!token.str.matches(SYM_PATTERN)) {
            printParseErrorMessage(1, token.line_num, token.offset); // sym_expected
          }
        }
      }

      // process instruction
      token = tokenList.removeFirst();
      textNum = Integer.parseInt(token.str);
      if (tokenList.isEmpty()) {
        printParseErrorMessage(0, token.line_num, token.offset);
      } else if (textNum + baseAddr >= 512) {
        printParseErrorMessage(6, token.line_num, token.offset);
      } else {
        for (int i = 0; i < textNum; i++) {
          // if (tokenList.isEmpty() || !token.str.matches(FOUR_DIGIT)) {
          if (tokenList.isEmpty()) {
            printParseErrorMessage(2, token.line_num, token.offset);
          }
          token = tokenList.removeFirst();
          if (tokenList.isEmpty() || !token.str.matches(INSTRCTION_PATTERN)) {
            printParseErrorMessage(2, token.line_num, token.offset);
          }
          token = tokenList.removeFirst();
        }
      }

      moduleNum++;
      modulesDefCount.add(defNum);
      modulesBaseAddress.add(baseAddr);
      modulesSize.add(textNum);
      baseAddr += textNum;
    }
  }

  public void printSymbolTable() {
    Set<String> uniqueSymbol = new HashSet<String>();
    Set<String> duplicate = new HashSet<String>();
    for (KVPair pair : symbolTable) {
      String symbol = pair.symbol;
      if (uniqueSymbol.contains(symbol)) {
        duplicate.add(symbol);
      } else {
        uniqueSymbol.add(symbol);
      }
    }

    StringBuilder sb = new StringBuilder();
    int begin = 0;
    for (int i = 0; i < moduleNum; i++) {
      int thisModuleSize = modulesSize.get(i);
      int thisModuleAddr = modulesBaseAddress.get(i);
      int def = modulesDefCount.get(i);
      int end = begin + def - 1;
      for (int j = begin; j <= end; j++) {
        KVPair pair = symbolTable.get(j);
        if (pair.value > thisModuleSize + thisModuleAddr) {
          sb.append("Warning: Module ").append(i + 1).append(" ")
              .append(pair.symbol).append(" to big ").append(pair.value);
          sb.append(" (max=").append(thisModuleSize - 1).append(")")
              .append(" assume zero relative\n");
          pair.value = 0;
        }
      }
      begin = end + 1;
    }
    if (sb.length() != 0) {
      System.out.print(sb.toString());
    }
    sb = new StringBuilder();
    sb.append("Symbol Table\n");
    Set<String> usedSymbol = new HashSet<String>();
    for (KVPair pair : symbolTable) {
      if (usedSymbol.contains(pair.symbol)) {
        continue;
      }
      sb.append(pair.symbol);
      sb.append("=");
      sb.append(pair.value);
      usedSymbol.add(pair.symbol);
      if (duplicate.contains(pair.symbol)) {
        sb.append(" Error: This variable is multiple times defined; first value used");
      }
      sb.append("\n");
    }
    System.out.println(sb.toString());
  }

  public void secondScanner() {
    try {
      bfReader = new BufferedReader(new FileReader(inputFile));
      String line;
      Lab_Token placeHolder = null;
      tokenList.clear();
      while ((line = bfReader.readLine()) != null) {
        line_num++;
        line = line.trim();
        if (line.isEmpty()) {
          continue;
        }
        String[] parameter = line.split(SPLIT_PATTERN);
        if (parameter.length == 0)
          continue;
        int offset = 1;
        for (int i = 0; i < parameter.length; i++) {
          Lab_Token token;
          if (i == 0) {
            token = new Lab_Token(line_num, offset, parameter[i]);
          } else {
            offset = offset + parameter[i - 1].length() + 1;
            token = new Lab_Token(line_num, offset, parameter[i]);
          }
          tokenList.add(token);
        }
        placeHolder = new Lab_Token(line_num, offset
            + parameter[parameter.length - 1].length(), "PlaceHolder Token");
      }
      tokenList.add(placeHolder);
      moduleNum = 0; // reset moduleNum
      while (tokenList.size() > 1) {
        // process defination list
        Lab_Token token = tokenList.removeFirst();
        defNum = Integer.parseInt(token.str);
        List<String> tempDef = new ArrayList<String>();
        for (int i = 0; i < defNum; i++) {
          if (moduleDefList.containsKey(moduleNum + 1)) {
            tempDef = moduleDefList.get(moduleNum + 1);
          }
          token = tokenList.removeFirst();
          tempDef.add(token.str);
          moduleDefList.put(moduleNum + 1, tempDef);
          tokenList.removeFirst();
        }

        // process use list
        token = tokenList.removeFirst();
        useNum = Integer.parseInt(token.str);
        List<String> tempUseList = new ArrayList<String>();
        for (int i = 0; i < useNum; i++) {
          if (moduleUseList.containsKey(moduleNum + 1)) {
            tempUseList = moduleUseList.get(moduleNum + 1);
          }
          token = tokenList.removeFirst();
          tempUseList.add(token.str);
          moduleUseList.put(moduleNum + 1, tempUseList);
        }

        // process instruction
        token = tokenList.removeFirst();
        textNum = Integer.parseInt(token.str);
        for (int i = 0; i < textNum; i++) {
          token = tokenList.removeFirst();
          String instructionType = token.str;
          token = tokenList.removeFirst();
          int instructionAddr = Integer.parseInt(token.str);
          memoryMap.add(new KVPair(instructionType, instructionAddr,
              moduleNum + 1));
        }
        moduleNum++;
      }
      printMemoryMap();
    } catch (IOException e) {

    } finally {
      try {
        bfReader.close();
      } catch (IOException e) {

      }
    }
  }

  public void printMemoryMap() {
    List<String> usedUsedList = new ArrayList<String>();
    StringBuilder result = new StringBuilder();
    StringBuilder warning = new StringBuilder();
    result.append("Memory Map\n");
    int count = 0;
    for (int i = 0; i < moduleNum; i++) {
      List<String> moduleUsedList = new ArrayList<String>();
      List<String> thisUseList = moduleUseList.get(i + 1);
      // i+1 represent the module number
      int moduleBaseAddr = modulesBaseAddress.get(i);
      int moduleSize = modulesSize.get(i);
      int begin = count;
      int end = count + moduleSize - 1;
      for (int j = begin; j <= end; j++) {
        KVPair pair = memoryMap.get(j);
        result.append(formatPrintInt(count, 3));
        result.append(":");
        String type = pair.symbol;
        int instr = pair.value;
        int opcode = instr / 1000;
        int oprand = instr % 1000;
        if ("I".equals(type)) {
          if (instr > 9999) {
            instr = 9999;
            result.append(instr);
            result.append(" Error: Illegal immediate value; treated as 9999\n");
          } else {
            result.append(formatPrintInt(instr, 4));
            result.append("\n");
          }
        } else if ("A".equals(type)) {
          if (instr > 9999) {
            instr = 9999;
            result.append(instr);
            result.append(" Error: Illegal opcode; treated as 9999\n");
          } else if (oprand > 512) {
            instr = opcode * 1000;
            result.append(instr);
            result
                .append(" Error: Absolute address exceeds machine size; zero used\n");
          } else {
            result.append(formatPrintInt(instr, 4));
            result.append("\n");
          }
        } else if ("R".equals(type)) {
          if (instr > 9999) {
            instr = 9999;
            result.append(instr);
            result.append(" Error: Illegal opcode; treated as 9999\n");
          } else if (oprand > moduleSize) {
            result.append(opcode * 1000 + moduleBaseAddr);
            result
                .append(" Error: Relative address exceeds module size; zero used\n");
          } else {
            result.append(formatPrintInt(instr + moduleBaseAddr, 4));
            result.append("\n");
          }
        } else if ("E".equals(type)) {
          if (instr > 9999) {
            instr = 9999;
            result.append(instr);
            result.append(" Error: Illegal opcode; treated as 9999\n");
          } else if (oprand >= thisUseList.size()) {
            result.append(formatPrintInt(instr, 4));
            result
                .append(" Error: External address exceeds length of uselist; treated as immediate\n");
          } else if (checkUsedNotDefine(thisUseList, oprand)) {
            result.append(opcode * 1000).append(" Error: ")
                .append(thisUseList.get(oprand))
                .append(" is not defined; zero used\n");
            usedUsedList.add(thisUseList.get(oprand));
            moduleUsedList.add(thisUseList.get(oprand));
          } else {
            String thisSymbol = thisUseList.get(oprand);
            usedUsedList.add(thisUseList.get(oprand));
            int new_instr = opcode * 1000
                + getExternalVaraibleValue(thisSymbol);
            result.append(formatPrintInt(new_instr, 4)).append("\n");
            moduleUsedList.add(thisUseList.get(oprand));
          }
        }
        count++;
      }
      System.out.print(result.toString());
      result = new StringBuilder();
      if (thisUseList != null && !thisUseList.isEmpty()) {
        for (String str : thisUseList) {
          if (!moduleUsedList.contains(str)) {
            warning.append("Warning: Module ").append(i + 1).append(": ")
                .append(str);
            warning
                .append(" appeared in the uselist but was not actually used\n");
            System.out.print(warning.toString());
            warning = new StringBuilder();
          }
        }
      }
    }
    // System.out.println(result.toString());
    for (Map.Entry<Integer, List<String>> entry : moduleDefList.entrySet()) {
      int moduleNumber = entry.getKey();
      List<String> useList = entry.getValue();
      for (String use : useList) {
        if (!usedUsedList.contains(use)) {
          warning.append("Warning: Module ").append(moduleNumber).append(":")
              .append(use);
          warning.append(" was defined but never used\n");
        }
      }
    }
    System.out.print(warning.toString());
  }

  private boolean checkUsedNotDefine(List<String> useList, int position) {
    String symbol = useList.get(position);
    for (KVPair pair : symbolTable) {
      if (pair.symbol.equals(symbol)) {
        return false;
      }
    }
    return true;
  }

  private int getExternalVaraibleValue(String symbol) {
    for (KVPair p : symbolTable) {
      if (p.symbol.equals(symbol)) {
        return p.value;
      }
    }
    return -1;
  }

  private String formatPrintInt(int instr, int count) {
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < count; i++) {
      sb.append(instr % 10);
      instr /= 10;
    }
    return sb.reverse().toString();
  }

  static class KVPair {
    String symbol;
    int value;
    int module;

    KVPair(String symbol, int value, int module) {
      this.symbol = symbol;
      this.value = value;
      this.module = module;
    }

    @Override
    public boolean equals(Object obj) {
      return this.symbol.equals(((KVPair) obj).symbol);
    }
  }

  public static void printParseErrorMessage(int errorCode, int lineNum,
      int charPlace) {
    switch (errorCode) {
    case 0:
      System.out.printf("Parse Error line %d offset %d: NUM_EXPECTED", lineNum,
          charPlace);
      System.exit(1);
    case 1:
      System.out.printf("Parse Error line %d offset %d: SYM_EXPECTED", lineNum,
          charPlace);
      System.exit(1);
    case 2:
      System.out.printf("Parse Error line %d offset %d: ADDR_EXPECTED",
          lineNum, charPlace);
      System.exit(1);
    case 3:
      System.out.printf("Parse Error line %d offset %d: SYM_TOLONG", lineNum,
          charPlace);
      System.exit(1);
    case 4:
      System.out.printf("Parse Error line %d offset %d: TO_MANY_DEF_IN_MODULE",
          lineNum, charPlace);
      System.exit(1);
    case 5:
      System.out.printf("Parse Error line %d offset %d: TO_MANY_USE_IN_MODULE",
          lineNum, charPlace);
      System.exit(1);
    case 6:
      System.out.printf("Parse Error line %d offset %d: TO_MANY_INSTR",
          lineNum, charPlace);
      System.exit(1);
    default:
      return;
    }
  }

//  public static void main(String[] args) {
//    String i = "".trim();
//    System.out.println(i.length());
//    String[] s = i.split("\\s+");
//    System.out.println(s.length);
//    for (String t : s) {
//      System.out.println(1);
//      System.out.println(t);
//    }
//    String SYM_PATTERN = "^[a-zA-Z][a-zA-Z0-9]*$";
//    System.out.println("s".matches(SYM_PATTERN));
//    String FOUR_DIGIT = "[0-9]{4}";
//    System.out.println("1234".matches(FOUR_DIGIT));
//  }
}
