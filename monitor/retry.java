import sun.hotspot.WhiteBox;
import java.util.concurrent.CyclicBarrier;
import jdk.internal.misc.Unsafe;



class x { 

  private static final Unsafe UNSAFE = Unsafe.getUnsafe();
  final int conflictLoop = 1000000;
  protected final Object monitor = new Object();
  WhiteBox wb;
  Thread thread0;
  Thread thread1; // conflicting thread
  Runnable work0; 
  Runnable work1; // conflicting task
  CyclicBarrier barrier; 
  private static int sharedVariable = 0;
  private static final byte[] arrayx = new byte[1024*1024*100];
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
   barrier = new CyclicBarrier(2);

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

  // -- generate memory conflict

   void transactionalRegion() {

   try {
       synchronized (monitor) {
           barrier.wait();
           Thread.sleep(1000);  
        }
   } catch (Exception e) {
       System.out.println("fail #10");
   }


/*
   for (int i = 0; i < conflictLoop; i++) {
       synchronized (monitor) {
       sharedVariable--;
       }
   } 
*/

/*
  for (int j = 0; j < 10;j++) {

    synchronized (monitor) {
   for( int i=0; i < 1024*1024*100; i++) {
    arrayx[i]++;
    }
   }
} 
*/

/*
   synchronized (monitor) {
    synchronized (monitor) {
    sharedVariable++;
    UNSAFE.pageSize();
    }
   }
*/
   }



   void causeConflict() throws Exception {
/*
   work1 = () -> {
       try {
          synchronized (monitor) {   
              barrier.await();
              Thread.sleep(1000);
    //          sharedVariable++;
          }
       } catch (Exception e) {
           System.out.println("fail #10");
       }
   }; 

   thread1 = new Thread(work1); // run work1
// thread1.setDaemon(true);
   thread1.start();
 


   try {
     barrier.await();
   synchronized (monitor) {
      sharedVariable++;
   }
   } catch (Exception e) {
     System.out.println("fail #11");
   }


   thread1.join(); // wait thread1 finish
*/
  work1 = () -> {
      try {
          System.out.println("Entering thread to sleep...");
          synchronized (monitor) {
              barrier.await();
              Thread.sleep(1000); // 1s
          }
      } catch (Exception e) {
          System.out.println("fail #100");  
      }
  };

  thread1 = new Thread(work1);
  thread1.start();
  syncAndTest();
  thread1.join();
  }

  public void run() {
      try {
          System.out.println("Entering thread to sleep...");
          synchronized (monitor) {
              barrier.await();
              Thread.sleep(1000); // 1s
          }
      } catch (Exception e) {
          System.out.println("fail #100");  
      }
  }
 
  public void syncAndTest() {
      try {
          barrier.await();
      } catch (Exception e) {
          System.out.println("fail #101");    
      }
      test();
  }

  public void test() {
      synchronized (monitor) {
          sharedVariable++;
      }
  } 


 

}
class retry  {
  protected Object monitor;
  static WhiteBox wb;
  static Runnable work0;
  static CyclicBarrier barrier = new CyclicBarrier(2);
  static Thread thread0; 
  private static int sharedVar = 0;

  public retry() {
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
   a.causeConflict();
   
  }

}
