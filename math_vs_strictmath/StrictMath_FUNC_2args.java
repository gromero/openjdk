public class StrictMath_FUNC {
  public static void main(String[] args) {
     double x = 0.0;
     for (int j=1; j<=100000000;j++) {
        x += StrictMath.FUNC(j,3000);
     }
     System.out.println(x);
  }
}
