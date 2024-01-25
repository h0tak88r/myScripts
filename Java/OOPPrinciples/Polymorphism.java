// Polymorphism Example: Method Overloading, Method Overriding, and Runtime Polymorphism

// Animal class representing the base class
class Animal {
    // Method to make a sound
    void makeSound() {
        System.out.println("Animal makes a generic sound");
    }
}

// Dog class inheriting from Animal
class Dog extends Animal {
    // Method overriding to provide specific sound for Dog
    @Override
    void makeSound() {
        System.out.println("Dog barks");
    }

    // Additional method specific to Dog
    void fetch() {
        System.out.println("Dog fetches a ball");
    }
}

// Cat class inheriting from Animal
class Cat extends Animal {
    // Method overriding to provide specific sound for Cat
    @Override
    void makeSound() {
        System.out.println("Cat meows");
    }

    // Additional method specific to Cat
    void climb() {
        System.out.println("Cat climbs a tree");
    }
}

// Main class for execution
public class Polymorphism {
    public static void main(String[] args) {
        // Example 1: Method Overloading
        System.out.println("Example 1: Method Overloading");
        System.out.println("Sum of integers: " + add(5, 10));
        System.out.println("Concatenation of strings: " + add("Hello", "World"));
        System.out.println();

        // Example 2: Runtime Polymorphism using Method Overriding
        System.out.println("Example 2: Runtime Polymorphism");
        Animal genericAnimal = new Animal();
        Dog myDog = new Dog();
        Cat myCat = new Cat();

        genericAnimal.makeSound();  // Output: Animal makes a generic sound
        myDog.makeSound();          // Output: Dog barks
        myCat.makeSound();          // Output: Cat meows
        System.out.println();

        // Example 3: Method Overriding with Additional Methods
        System.out.println("Example 3: Method Overriding with Additional Methods");
        myDog.fetch();  // Output: Dog fetches a ball
        myCat.climb();  // Output: Cat climbs a tree
    }

    // Method Overloading example
    private static int add(int a, int b) {
        return a + b;
    }

    private static String add(String a, String b) {
        return a + " " + b;
    }
}
