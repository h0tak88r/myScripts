// Interface: A collection of abstract methods. Classes implement interfaces to provide specific behavior.
// Example: 'Shape' interface implemented by 'Circle' and 'Rectangle' classes.

// Shape interface
interface Shape {
  double calculateArea();  // Abstract method to calculate area
  void display();          // Abstract method to display shape
}

// Circle class implementing Shape interface
class Circle implements Shape {
  private double radius;  // Private field for circle radius

  // Constructor to initialize radius
  Circle(double radius) {
    this.radius = radius;
  }

  // Implementing abstract method to calculate area for a circle
  @Override
  public double calculateArea() {
    return Math.PI * radius * radius;
  }

  // Implementing abstract method to display information about the circle
  @Override
  public void display() {
    System.out.println("Circle - Radius: " + radius);
  }
}

// Rectangle class implementing Shape interface
class Rectangle implements Shape {
  private double length;  // Private field for rectangle length
  private double width;   // Private field for rectangle width

  // Constructor to initialize length and width
  Rectangle(double length, double width) {
    this.length = length;
    this.width = width;
  }

  // Implementing abstract method to calculate area for a rectangle
  @Override
  public double calculateArea() {
    return length * width;
  }

  // Implementing abstract method to display information about the rectangle
  @Override
  public void display() {
    System.out.println("Rectangle - Length: " + length + ", Width: " + width);
  }
}

// Main class for execution
class Interface {
  public static void main(String[] args) {
    // Create objects of Circle and Rectangle
    Circle myCircle = new Circle(5.0);
    Rectangle myRectangle = new Rectangle(4.0, 6.0);

    // Demonstrate interface implementation
    displayShapeInfo(myCircle);    // Output: Circle - Radius: 5.0
    displayShapeInfo(myRectangle); // Output: Rectangle - Length: 4.0, Width: 6.0
  }

  // Method to display information using the Shape interface
  public static void displayShapeInfo(Shape shape) {
    System.out.println("Area: " + shape.calculateArea());
    shape.display();
  }
}