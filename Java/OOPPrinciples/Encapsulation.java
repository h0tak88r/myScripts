// Encapsulation: Bundling data (fields) and methods in a class, restricting access.
// Example: 'Area' class with private fields (length, breadth), controlled access through getter and setter methods.

class Area {
  private int length;   // Private field to store length
  private int breadth;  // Private field to store breadth

  // Constructor to initialize values
  Area(int length, int breadth) {
    this.length = length;
    this.breadth = breadth;
  }

  // Getter method for length
  public int getLength() {
    return length;
  }

  // Setter method for length
  public void setLength(int length) {
    this.length = length;
  }

  // Getter method for breadth
  public int getBreadth() {
    return breadth;
  }

  // Setter method for breadth
  public void setBreadth(int breadth) {
    this.breadth = breadth;
  }

  // Method to calculate and print area
  public void getArea() {
    int area = length * breadth;
    System.out.println("Area: " + area);
  }
}

// Main class for execution
class Encapsulation {
  public static void main(String[] args) {
    // Create object of Area
    Area rectangle = new Area(5, 6);
    
    // Set values using setter methods
    rectangle.setLength(8);
    rectangle.setBreadth(10);
    
    // Get values using getter methods
    System.out.println("Length: " + rectangle.getLength());  // Output: Length: 8
    System.out.println("Breadth: " + rectangle.getBreadth());  // Output: Breadth: 10
    
    rectangle.getArea();  // Output: Area: 80
  }
}
