public class Contacts {
    private String name;
    private int number;
    private String email;

    public Contacts(String name, int number, String email) {
        this.name = name;
        this.number = number;
        this.email = email;
    }

    public void getDetails(){
        System.out.println("Contact Details: ");
        System.out.println("Contact Name: "+ name);
        System.out.println("Contact Number: " + number);
        System.out.println("Contact Email: " + email);
    }

    public String getName() {
        return name;
    }
}
