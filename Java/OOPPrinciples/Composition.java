// Composition is a concept in object-oriented programming (OOP) that allows you to design and structure classes by combining simpler classes or objects as components. In simpler terms, composition is the act of constructing a complex object by assembling smaller objects
// Composition Example

// Engine class representing a component
class Engine {
    void start() {
        System.out.println("Engine started");
    }

    void stop() {
        System.out.println("Engine stopped");
    }
}

// Car class using composition to include Engine
class Car {
    // Composition: Car has an Engine
    private Engine engine;

    // Constructor to initialize the Engine
    Car(Engine engine) {
        this.engine = engine;
    }

    // Method to start the car
    void startCar() {
        System.out.println("Car is starting...");
        engine.start(); // Delegating the start operation to Engine
    }

    // Method to stop the car
    void stopCar() {
        System.out.println("Car is stopping...");
        engine.stop(); // Delegating the stop operation to Engine
    }
}

// Main class for execution
public class Composition {
    public static void main(String[] args) {
        // Creating an Engine
        Engine carEngine = new Engine();

        // Creating a Car with the Engine
        Car myCar = new Car(carEngine);

        // Using composition to start and stop the car
        myCar.startCar(); // Output: Car is starting... Engine started
        myCar.stopCar();  // Output: Car is stopping... Engine stopped
    }
}
