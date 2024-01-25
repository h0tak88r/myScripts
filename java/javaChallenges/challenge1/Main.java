import java.util.Objects;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Random;


public class Main {
    private static final Scanner scanner = new Scanner(System.in);
    private static final ArrayList<Contacts> contactsList = new ArrayList<>();
    private static final ArrayList<Messages> messagesList = new ArrayList<>();
    private static final Random random =new Random();

    public static void main(String[] args) {
        System.out.println("Please enter your name: ");
        String name = scanner.next();
        System.out.println("Hello " + name + " Shall We Start ?");
        showOptions();
    }
    private static void showOptions() {
        System.out.println("""
                \t1. Manage Contact.
                \t2. Messages"
                \t3. Quite
                """);
        int choice = scanner.nextInt();
        switch (choice) {
            case 1:
                manageContacts();
                break;
            case 2:
                manageMessaging();
                break;
            default:
                break;
        }
    }

    private static void manageMessaging() {
        System.out.println("What To Do ?");
        System.out.println("""
                \t1. See the list of all messages
                \t2. Send a new message
                \t3. Go back to the previous menu
                """);
        int choice = scanner.nextInt();
        switch (choice){
            case 1:
                showMessages();
                manageMessaging();
                break;
            case 2:
                sendMessage();
                manageMessaging();
                break;
            default:
                showOptions();
        }
    }

    private static void showMessages() {
        for(Messages m: messagesList){
            m.getDetails();
        }
    }

    private static void sendMessage() {
        System.out.println("For Who ?");
        String name = scanner.next();
        System.out.println("What you wanna Say ?");
        String text = scanner.next();
        int messageId = random.nextInt();
        Messages message = new Messages(name,text,messageId);
        for(Contacts c: contactsList){
            if(c.getName().equals(name)){
                messagesList.add(message);
                System.out.println("Done, Your Message Sent to" + name );
            }else{
                System.out.println("Sorry" + name + " Is not actually in our contacts list.");
            }
        }
    }

    private static void manageContacts() {
        System.out.println("Ok Lets See what to do with Contacts....");
        System.out.println("""
                \t1. Show All Contacts.
                \t2. Add a new contact
                \t3. Search for a contact
                \t4. Delete a contact
                \t5. Go back to the previous menu""");
        int choice = scanner.nextInt();
        switch (choice) {
            case 1:
                showAllContacts();
                manageContacts();
                break;
            case 2:
                addNewContacts();
                manageContacts();
                break;
            case 3:
                searchContact();
                manageContacts();
                break;
            case 4:
                deleteContact();
                manageContacts();
                break;
            default:
                showOptions();
        }
    }

    private static void deleteContact() {
        System.out.println("Who you wanna delete ?");
        String name = scanner.next();
        contactsList.removeIf(c -> c.getName().equals(name));
        System.out.println("If it were really in our contacts list it should be removed now so cheer !!");
    }

    private static void searchContact() {
        System.out.println("Enter contact name :");
        String name = scanner.next();
        for (Contacts c : contactsList) {
            if (Objects.equals(c.getName(), name)) {
                System.out.println("Yeah we have found it ");
                c.getDetails();
            } else {
                System.out.println("Sorry we do not have such contact in our contact list");
            }
        }

    }

    private static void addNewContacts() {
        System.out.println("OK lets add new contact to our Contact List !");
        System.out.println("Contact Name?");
        String name = scanner.next();
        System.out.println("Contact Email?");
        String email = scanner.next();
        System.out.println("Contact Number?");
        int number = scanner.nextInt();
        Contacts contact = new Contacts(name, number, email);
        contactsList.add(contact);
        System.out.println("Done, Your Contact Saved to our contact List !");
    }

    private static void showAllContacts() {
        for (Contacts c : contactsList) {
            c.getDetails();
            System.out.println("*****************************");
        }
    }

}