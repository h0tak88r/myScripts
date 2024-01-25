// Inheritance: A mechanism in OOP where a new class inherits properties and behaviors from an existing class.
// Example: 'Animal' superclass with 'Dog' and 'Cat' subclasses demonstrating inheritance.


// Animal superclass
class Animal {
  protected String name;  // Protected field for animal name

  // Constructor to initialize name
  Animal(String name) {
    this.name = name;
  }

  // Method to display general sound of an animal
  public void makeSound() {
    System.out.println("Generic Animal Sound");
  }
}

// Dog subclass inheriting from Animal
class Dog extends Animal {
  private String breed;  // Private field for dog breed

  // Constructor to initialize name and breed
  Dog(String name, String breed) {
    super(name);  // Call superclass constructor
    this.breed = breed;
  }

  // Method to display specific sound of a dog
  @Override
  public void makeSound() {
    System.out.println("Woof! Woof!");
  }

  // Method to display additional information about the dog
  public void displayInfo() {
    System.out.println("Dog Name: " + name);
    System.out.println("Breed: " + breed);
  }
}

// Cat subclass inheriting from Animal
class Cat extends Animal {
  private boolean hasTail;  // Private field indicating whether the cat has a tail

  // Constructor to initialize name and tail information
  Cat(String name, boolean hasTail) {
    super(name);  // Call superclass constructor
    this.hasTail = hasTail;
  }

  // Method to display specific sound of a cat
  @Override
  public void makeSound() {
    System.out.println("Meow! Meow!");
  }

  // Method to display additional information about the cat
  public void displayInfo() {
    System.out.println("Cat Name: " + name);
    System.out.println("Has Tail: " + hasTail);
  }
}

// Main class for execution
class Inheritance {
  public static void main(String[] args) {
    // Create objects of Dog and Cat
    Dog myDog = new Dog("Buddy", "Golden Retriever");
    Cat myCat = new Cat("Whiskers", true);

    // Demonstrate inheritance and polymorphism
    myDog.makeSound();        // Output: Woof! Woof!
    myDog.displayInfo();      // Output: Dog Name: Buddy, Breed: Golden Retriever

    myCat.makeSound();        // Output: Meow! Meow!
    myCat.displayInfo();      // Output: Cat Name: Whiskers, Has Tail: true
  }
}