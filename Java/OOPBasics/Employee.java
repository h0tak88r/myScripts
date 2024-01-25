// Employee.java
public class Employee {
  String name;
  double baseSalary;
  double bonusHours;
  double sales;

  public double calculateNetSalary() {
    // Assume a fixed bonus rate and commission rate
    double bonusRate = 10; // 10% bonus rate
    double commissionRate = 0.05; // 5% commission rate

    // Calculate bonus and commission
    double bonus = (bonusHours / 40) * baseSalary * (bonusRate / 100);
    double commission = sales * commissionRate;

    // Calculate net salary
    double netSalary = baseSalary + bonus + commission;

    return netSalary;
  }

  public void displaySalaryDetails() {
    System.out.println("Name: " + name);
    System.out.println("Base Salary: $" + baseSalary);
    System.out.println("Bonus: $" + ((bonusHours / 40) * baseSalary * 0.1));
    System.out.println("Commission: $" + (sales * 0.05));
    System.out.println("Net Salary: $" + calculateNetSalary());
  }
}
