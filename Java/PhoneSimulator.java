import java.util.ArrayList;
import java.util.Scanner;

class Contact {
    private String name;
    private String phoneNumber;

    public Contact(String name, String phoneNumber) {
        this.name = name;
        this.phoneNumber = phoneNumber;
    }

    public String getName() {
        return name;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }
}

class Message {
    private String sender;
    private String content;

    public Message(String sender, String content) {
        this.sender = sender;
        this.content = content;
    }

    public String getSender() {
        return sender;
    }

    public String getContent() {
        return content;
    }
}

public class PhoneSimulator {
    private static ArrayList<Contact> contacts = new ArrayList<>();
    private static ArrayList<Message> messages = new ArrayList<>();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        greetUser();

        int choice;
        do {
            displayMainMenu();
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume the newline character

            switch (choice) {
                case 1:
                    manageContacts();
                    break;
                case 2:
                    manageMessages();
                    break;
                case 3:
                    System.out.println("Quitting the application. Goodbye!");
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        } while (choice != 3);

        scanner.close();
    }

    private static void greetUser() {
        System.out.println("Welcome to Phone Simulator!");
    }

    private static void displayMainMenu() {
        System.out.println("\nMain Menu:");
        System.out.println("1. Manage contacts");
        System.out.println("2. Messages");
        System.out.println("3. Quit");
        System.out.print("Enter your choice: ");
    }

    private static void manageContacts() {
        int choice;
        do {
            displayContactsMenu();
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume the newline character

            switch (choice) {
                case 1:
                    showAllContacts();
                    break;
                case 2:
                    addContact();
                    break;
                case 3:
                    searchContact();
                    break;
                case 4:
                    deleteContact();
                    break;
                case 5:
                    System.out.println("Going back to the main menu.");
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        } while (choice != 5);
    }

    private static void displayContactsMenu() {
        System.out.println("\nContacts Menu:");
        System.out.println("1. Show all contacts");
        System.out.println("2. Add a new contact");
        System.out.println("3. Search for a contact");
        System.out.println("4. Delete a contact");
        System.out.println("5. Go back to the previous menu");
        System.out.print("Enter your choice: ");
    }

    private static void showAllContacts() {
        if (contacts.isEmpty()) {
            System.out.println("No contacts available.");
        } else {
            System.out.println("\nList of Contacts:");
            for (Contact contact : contacts) {
                System.out.println("Name: " + contact.getName() + ", Phone Number: " + contact.getPhoneNumber());
            }
        }
    }

    private static void addContact() {
        System.out.print("Enter the name of the new contact: ");
        String name = scanner.nextLine();
        System.out.print("Enter the phone number of the new contact: ");
        String phoneNumber = scanner.nextLine();

        Contact newContact = new Contact(name, phoneNumber);
        contacts.add(newContact);

        System.out.println("Contact added successfully!");
    }

    private static void searchContact() {
        System.out.print("Enter the name to search for: ");
        String searchName = scanner.nextLine();

        for (Contact contact : contacts) {
            if (contact.getName().equalsIgnoreCase(searchName)) {
                System.out.println("Contact found:");
                System.out.println("Name: " + contact.getName() + ", Phone Number: " + contact.getPhoneNumber());
                return;
            }
        }

        System.out.println("Contact not found.");
    }

    private static void deleteContact() {
        System.out.print("Enter the name to delete: ");
        String deleteName = scanner.nextLine();

        for (Contact contact : contacts) {
            if (contact.getName().equalsIgnoreCase(deleteName)) {
                contacts.remove(contact);
                System.out.println("Contact deleted successfully!");
                return;
            }
        }

        System.out.println("Contact not found.");
    }

    private static void manageMessages() {
        int choice;
        do {
            displayMessagesMenu();
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume the newline character

            switch (choice) {
                case 1:
                    seeAllMessages();
                    break;
                case 2:
                    sendNewMessage();
                    break;
                case 3:
                    System.out.println("Going back to the main menu.");
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        } while (choice != 3);
    }

    private static void displayMessagesMenu() {
        System.out.println("\nMessages Menu:");
        System.out.println("1. See the list of all messages");
        System.out.println("2. Send a new message");
        System.out.println("3. Go back to the previous menu");
        System.out.print("Enter your choice: ");
    }

    private static void seeAllMessages() {
        if (messages.isEmpty()) {
            System.out.println("No messages available.");
        } else {
            System.out.println("\nList of Messages:");
            for (Message message : messages) {
                System.out.println("Sender: " + message.getSender() + ", Content: " + message.getContent());
            }
        }
    }

    private static void sendNewMessage() {
        System.out.print("Enter the sender's name: ");
        String senderName = scanner.nextLine();
        System.out.print("Enter the message content: ");
        String messageContent = scanner.nextLine();

        Message newMessage = new Message(senderName, messageContent);
        messages.add(newMessage);

        System.out.println("Message sent successfully!");
    }
}
