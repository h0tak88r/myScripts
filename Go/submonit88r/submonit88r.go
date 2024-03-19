package main

import (
	"bufio"
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/h0tak88r/submonit88r/pkg/sub88r"

	"github.com/spf13/cobra"

	_ "github.com/mattn/go-sqlite3"
)

const (
	dbFile          = "subdomains_database.db"
	resultsFileName = "subMonit88rResults.txt"
)

type config struct {
	DomainList string
	Webhook    string
	Monitor    bool
}

var cfg config

func init() {
	rootCmd := &cobra.Command{
		Use:   "goMonit88r",
		Short: "A tool for subdomain enumeration with monitoring and Discord notification support.",
		Run:   run,
	}
	rootCmd.Flags().StringVarP(&cfg.DomainList, "domain-list", "l", "", "Specify a file containing a list of domains")
	rootCmd.Flags().StringVarP(&cfg.Webhook, "webhook", "w", "", "Specify the Discord webhook URL")
	rootCmd.Flags().BoolVarP(&cfg.Monitor, "monitor", "m", false, "Enable subdomain monitoring")

	// Add validation for required flags
	err := rootCmd.MarkFlagRequired("domain-list")
	if err != nil {
		log.Fatal(err)
	}

	// Add custom validation for flags
	cobra.OnInitialize(validateFlags)

	rootCmdInstance = rootCmd
}

func validateFlags() {
	if cfg.DomainList == "" {
		fmt.Println("Error: Missing required flag --domain-list")
		fmt.Println("Use 'goMonit88r --help' for usage information.")
		os.Exit(1)
	}
}

var rootCmdInstance *cobra.Command
var monitorInterval = 10 * time.Hour

func printLogo() {
	fmt.Println(`
		┏┓  ┓ ┳┳┓    • ┏┓┏┓  
		┗┓┓┏┣┓┃┃┃┏┓┏┓┓╋┣┫┣┫┏┓
		┗┛┗┻┗┛┛ ┗┗┛┛┗┗┗┗┛┗┛┛ 
				by sallam(h0tak88r)
	`)

}
func main() {
	printLogo()
	err := rootCmdInstance.Execute()
	if err != nil {
		log.Fatal(err)
	}
}

func run(cmd *cobra.Command, args []string) {
	go printLogo()
	go initDatabase()

	if cfg.Monitor {
		monitorSubdomains()
	} else {
		subdomainEnumeration()
	}
}

func monitorSubdomains() {
	for {
		subdomainEnumeration()
		time.Sleep(monitorInterval)
	}
}

func subdomainEnumeration() {
	startTime := time.Now()
	domains, err := readDomainsFromFile(cfg.DomainList)
	if err != nil {
		log.Fatal(err)
	}

	uniqueSubdomains := make(map[string]struct{})

	for _, domain := range domains {
		subdomains := fetchSubdomainsFromSources(domain)
		for _, subdomain := range subdomains {
			uniqueSubdomains[subdomain] = struct{}{}
		}
	}

	var allSubdomains []string
	for subdomain := range uniqueSubdomains {
		allSubdomains = append(allSubdomains, subdomain)
	}

	oldSubdomains := getSubdomainsFromDB()
	newSubdomains := difference(allSubdomains, oldSubdomains)

	writeSubdomainsToFile(resultsFileName, allSubdomains)

	elapsedTime := time.Since(startTime)
	fmt.Printf("[+] Subdomains Enumeration completed in %s, Results are saved in subMonit88rResults.txt.\n", elapsedTime)

	if len(newSubdomains) > 0 {
		fmt.Printf("[+] %d new subdomains discovered:\n", len(newSubdomains))
		addSubdomainsToDB(newSubdomains)

		for _, subdomain := range newSubdomains {
			fmt.Println(subdomain)
		}
		// Notify user via Discord webhook if provided
		if cfg.Webhook != "" {
			go sendDiscordNotification(newSubdomains)
		}
	}
}

func initDatabase() {
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	_, err = db.Exec("CREATE TABLE IF NOT EXISTS subdomains (id INTEGER PRIMARY KEY, subdomain TEXT)")
	if err != nil {
		log.Fatal(err)
	} else {
		fmt.Println("[+] Database initialized successfully.")
	}
}

func sendDiscordNotification(subdomains []string) {
	message := fmt.Sprintf("[Subdomain Monitor] %d new subdomains discovered:\n", len(subdomains))
	for _, subdomain := range subdomains {
		message += subdomain + "\n"
	}

	if err := sendWebhookMessage(cfg.Webhook, message); err != nil {
		fmt.Printf("[!] Error sending Discord notification: %v\n", err)
	}
}

func sendWebhookMessage(webhook, message string) error {
	payload := map[string]string{"content": message}
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	client := &http.Client{}
	req, err := http.NewRequest("POST", webhook, bytes.NewBuffer(payloadBytes))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("non-OK status code: %d", resp.StatusCode)
	}

	return nil
}

func addSubdomainsToDB(subdomains []string) {
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		log.Fatalf("Error opening database: %v", err)
	}
	defer db.Close()

	tx, err := db.Begin()
	if err != nil {
		log.Fatal(err)
	}

	stmt, err := tx.Prepare("INSERT INTO subdomains (subdomain) VALUES (?)")
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()

	for _, subdomain := range subdomains {
		_, err = stmt.Exec(subdomain)
		if err != nil {
			log.Fatal(err)
		}
	}

	err = tx.Commit()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("[+] Added %d new subdomains to the database.\n", len(subdomains))
}

func getSubdomainsFromDB() []string {
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	rows, err := db.Query("SELECT subdomain FROM subdomains")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	var subdomains []string

	for rows.Next() {
		var subdomain string
		err := rows.Scan(&subdomain)
		if err != nil {
			log.Fatal(err)
		}
		subdomains = append(subdomains, subdomain)
	}

	fmt.Println("[+] Retrieved subdomains from the database.")

	return subdomains
}

// Fetch subdomains from different sources using subber package
func fetchSubdomainsFromSources(domain string) []string {
	var wg sync.WaitGroup

	// Create a Subber instance
	subber := &sub88r.Subber{
		Domain:  domain,
		Results: &sub88r.Results{},
	}

	// Define a function to fetch subdomains from a source
	fetch := func(fetchFunc func() error, sourceName string) {
		wg.Add(1)
		defer wg.Done()
		fmt.Printf("[+] Getting Subdomains from %s...\n", sourceName)
		if err := fetchFunc(); err != nil {
			log.Fatalf("Error while getting subdomains from %s: %v\n", sourceName, err)
		}
	}

	// Fetch subdomains from each source concurrently
	go fetch(subber.Anubis, "Anubis jdlc.me")
	go fetch(subber.UrlScan, "UrlScan")
	go fetch(subber.CrtSh, "CrtSh")
	go fetch(subber.HackerTarget, "HackerTarget")
	go fetch(subber.Otx, "Otx")

	wg.Wait()

	return subber.GetAllSubdomains()
}

func difference(set1, set2 []string) []string {
	var diff []string
	set := make(map[string]struct{})

	for _, s := range set2 {
		set[s] = struct{}{}
	}

	for _, s := range set1 {
		if _, ok := set[s]; !ok {
			diff = append(diff, s)
		}
	}

	return diff
}

func writeSubdomainsToFile(filename string, subdomains []string) {
	file, err := os.Create(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	uniqueSubdomains := make(map[string]struct{})

	for _, subdomain := range subdomains {
		if _, ok := uniqueSubdomains[subdomain]; !ok {
			file.WriteString(subdomain + "\n")
			uniqueSubdomains[subdomain] = struct{}{}
		}
	}
}

func readDomainsFromFile(filename string) ([]string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var domains []string
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		domains = append(domains, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return domains, nil
}
