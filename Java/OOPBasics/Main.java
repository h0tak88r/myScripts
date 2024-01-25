public class Main {
  public static void main(String[] args) {

    Player player1 = new Player();
    player1.name = "mszt";
    player1.age = 88;
    player1.rank = 1;

    player1.pass();
    player1.shoot();
    player1.playerDetails();

    Car car1 = new Car();
    car1.name = "BMW";
    car1.model = "M3";
    car1.color = "Black";
    car1.turnLeft();

    Employee employee1 = new Employee();
    employee1.name = "John";
    employee1.baseSalary = 50000;
    employee1.bonusHours = 40;
    employee1.sales = 100000;
    employee1.displaySalaryDetails();
    employee1.calculateNetSalary();


  }
}