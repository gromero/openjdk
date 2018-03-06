class BrokenClass {
  public static void main(String[] args) {
    String s0 = "abcd";
    String s1 = null;
     
    messageBroker(s0, 0);
    messageBroker(s0, 1);
    messageBroker(s1, 0); // will throw a NullPointerException
  }

  static void messageBroker(String msg, int selector) {
    if (selector == 0)
      printA(msg);
    else
      printB(msg);
  }

  static void printA(String s) {
    System.out.println("I'm method printA() and string given has length " + s.length());
  }

  static void printB(String s) {
    System.out.println("I'm method printB() and string given has length " + s.length());
  }
}
