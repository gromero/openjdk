import sun.hotspot.WhiteBox;
import java.util.concurrent.CyclicBarrier;



class x { 

  Object monitor = new Object();
  WhiteBox wb;
  Thread thread0;
  Runnable work0; 
  CyclicBarrier barrier; 
  int sharedVariable = 0;
  int[] arrayx = new int[1024];
  int loopCounter;

  public x() { 
    System.out.println("Initializing monitor inflator with default loop value (1000000)...");
    loopCounter = 1000000;
//    this.monitor = new Object();
  }   


  public x(int value) {
     System.out.println("Initializing monitor inflator with loop value " + value);
     loopCounter = value;
   }   

  void isMonitorInflated() {
//    System.out.println("I'm A from x class");
    wb = WhiteBox.getWhiteBox();
    System.out.println("Is monitor inflated? " + (wb.isMonitorInflated(this.monitor) ? "Yes" : "No"));
  } 

  void inflateMonitor() throws Exception { 
   barrier = new CyclicBarrier(1);

   work0 = () -> {
      synchronized (monitor) {
      try {
         barrier.await(); 
      } catch (Exception e) {
        System.out.println("0");

      }
  

      try {
          // wait until primordial thread dies
        monitor.wait();
      } catch (Exception e) {
//          throw e;
        System.out.println("2");
        // do nothing.
      }

      }

    };

    
    System.out.println("Creating thread0...");

    thread0 = new Thread(work0);
    thread0.setDaemon(true);
   thread0.start();


  barrier.await();

    System.out.println("Trying to inflate lock...");
    synchronized (monitor) {
       sharedVariable++;
       }
    }


//    thread0.join();

}
class m  {
  protected Object monitor;
  static WhiteBox wb;
  static Runnable work0;
  static CyclicBarrier barrier = new CyclicBarrier(2);
  static Thread thread0; 
  private static int sharedVar = 0;

  public m() {
    this.monitor = new Object();
  }   

  private void A() {
     System.out.println("I'm A");
  }


  public static void main(String[] args) throws Exception {

/*
    work0 = () -> {
      synchronized (monitor) {
      try {
        barrier.await(); 
      } catch (Exception e) {
          System.out.println("1");
          // do nothing.
      }
      } 
    
      try {
          // wait until primordial thread dies
          monitor.wait();
      } catch (Exception e) {
//          throw e;
        System.out.println("2");
        // do nothing.
      }
    };

    thread0 = new Thread(work0);
    thread0.setDaemon(true);
    thread0.start();

    barrier.await();
    synchronized (monitor) {
        sharedVar++;
    }
*/
//    wb = WhiteBox.getWhiteBox();
//    System.out.println("state: " + wb.isMonitorInflated(this.monitor));

   int value = 1000000;
  
   try {
     value = Integer.parseInt(args[0]);
   } catch (Exception e) {
   }
  
   x a = new x(value); 
   a.inflateMonitor();
   a.isMonitorInflated();
   
  }

}
