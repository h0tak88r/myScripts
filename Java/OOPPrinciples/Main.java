class Animal {
    protected String name;

    protected void display() {
        System.out.println("I am an animal.");
    }
}

class Dog extends Animal {
    public void getInfo() {
        System.out.println("My name is " + name);  // Accessing the protected field from the superclass
    }
}

public class Inheritance {
    public static void main(String[] args) {
        Dog labrador = new Dog();
        labrador.name = "Rocky";  // Modifying the protected field from the subclass
        labrador.display();  // Accessing the protected method from the subclass
        labrador.getInfo();
    }
}
// Output:
// I am an animal.
// My name is Rocky