public class Messages {
    private String reciept;
    private String text;
    private int id;

    public Messages(String reciept, String text, int id) {
        this.reciept = reciept;
        this.text = text;
        this.id = id;
    }

    public void getDetails() {
        System.out.println("Message Details: ");
        System.out.println("Reciept: " + reciept);
        System.out.println("Text: " + text);
        System.out.println("ID: " + id);
        System.out.println("********************");
    }
}
