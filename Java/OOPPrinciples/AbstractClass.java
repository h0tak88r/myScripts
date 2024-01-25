// Abstract Class: A class that cannot be instantiated and may contain abstract methods. 
// It serves as a blueprint for other classes.

// Example: Abstract class 'Vehicle' with concrete method 'startEngine' and abstract method 'fuelUp'.

// Abstract class 'Vehicle'
abstract class Vehicle {
  // Concrete method
  public void startEngine() {
    System.out.println("Engine started");
  }

  // Abstract method (to be implemented by subclasses)
  public abstract void fuelUp();
}

// Concrete subclass 'Car' extending abstract class 'Vehicle'
class Car extends Vehicle {
  // Implementation of abstract method 'fuelUp' for Car
  @Override
  public void fuelUp() {
    System.out.println("Car fueled up with gasoline");
  }

  // Additional method specific to Car
  public void drift() {
    System.out.println("Car drifting");
  }
}

// Concrete subclass 'Motorcycle' extending abstract class 'Vehicle'
class Motorcycle extends Vehicle {
  // Implementation of abstract method 'fuelUp' for Motorcycle
  @Override
  public void fuelUp() {
    System.out.println("Motorcycle fueled up with petrol");
  }

  // Additional method specific to Motorcycle
  public void wheelie() {
    System.out.println("Motorcycle doing a wheelie");
  }
}

// Main class for execution
class AbstractClass {
  public static void main(String[] args) {
    // Create objects of Car and Motorcycle
    Car myCar = new Car();
    Motorcycle myMotorcycle = new Motorcycle();

    // Demonstrate abstract class and polymorphism
    myCar.startEngine();     // Output: Engine started
    myCar.fuelUp();          // Output: Car fueled up with gasoline
    myCar.drift();           // Output: Car drifting

    myMotorcycle.startEngine();  // Output: Engine started
    myMotorcycle.fuelUp();       // Output: Motorcycle fueled up with petrol
    myMotorcycle.wheelie();      // Output: Motorcycle doing a wheelie
  }
}
