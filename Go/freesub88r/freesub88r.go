package freesub88r

import (
	"fmt"
	"strings"
	"net/http"
	"io"
)

type sub88r struct {
	domain string
}

func New(domain string) *sub88r {
	return &sub88r{domain: domain}
}

func (s *sub88r) fetchSubdomainsFromRapiddns(domain string) []string {
	url := fmt.Sprintf("https://rapiddns.io/subdomain/%s?full=1#result", domain)

	resp, err := http.Get(url)
	if err != nil {
		return nil
	}

	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)

	
	// Parse HTML response
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(body))
	if err != nil {
		fmt.Printf("[X] Error parsing HTML for domain %s from %s: %v\n", domain, url, err)
		return []string{}
	}

	subdomains := []string{}
	websiteTable := doc.Find("table.table-striped").First()

	if websiteTable.Length() > 0 {
		websiteTable.Find("tbody").Each(func(_ int, tbody *goquery.Selection) {
			tbody.Find("tr").Each(func(_ int, tr *goquery.Selection) {
				subdomain := tr.Find("td").First().Text()
				subdomains = append(subdomains, subdomain)
			})
		})
	} else {
		fmt.Println("[X] No table element found on the page.")
	}

	return subdomains
}
