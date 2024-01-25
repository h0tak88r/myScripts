public class Player {
  String name;
  short age;
  short rank;

  void pass(){
    System.out.println("player " + name + " passing!");
  }

  void shoot(){
    System.out.println("player " + name + " shooting!");
  }

  void playerDetails(){
    System.out.println(
      "\nplayer name : " + name +
      "\nplayer age  : " + age  +
      "\nplayer rank : " + rank
    );
  }
}