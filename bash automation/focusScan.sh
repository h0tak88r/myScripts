#!/bin/bash

check_required_tools() {
    echo "[+] Checking if the tools is installed in your machine"
    local required_tools=("subfinder" "naabu" "httpx" "gau" "kxss" "nuclei" "ffuf")
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            echo "Error: $tool is not installed. Please install it before running the script."
            exit 1
        fi
    done
}

banner() {
cat << "EOF"
    ____                _____                  ____  ____      
   / __/______  _______/ ___/_________ _____  ( __ )( __ )_____
  / /_/ ___/ / / / ___/\__ \/ ___/ __ `/ __ \/ __  / __  / ___/
 / __/ /__/ /_/ (__  )___/ / /__/ /_/ / / / / /_/ / /_/ / /    
/_/  \___/\__,_/____//____/\___/\__,_/_/ /_/\____/\____/_/     
                                                                                                                               
EOF
}

cleanup_subs_directory() {
    echo "[+] Cleaning up the subs directory"
    rm -rf focusResults/
    mkdir focusResults/
}

get_target_domain() {
    read -p "Enter the target domain: " target_domain
    echo "$target_domain"
}

get_discord_webhooks() {
    read -p "Enter the Discord webhook URL: " DISCORD_WEBHOOK
}

send_file_to_discord() {
    local webhook_url="$1"
    local file_path="$2"

    if [ -f "$file_path" ]; then
        curl -X POST -F "file=@$file_path" "$webhook_url"
        echo "File '$file_path' successfully sent to Discord."
    else
        echo "Error: File '$file_path' not found."
    fi
}

perform_port_scanning() {
    echo "[+] Performing port scanning"
    naabu -host "$TARGET_DOMAIN" -top-ports 1000 | notify -bulk
}

perform_exposed_panels_scan() {
    echo "[+] Performing exposed panels scan"
    echo "$TARGET_DOMAIN" | nuclei -t nuclei_templates/panels | notify -bulk
}

perform_js_exposure_scan() {
    echo "[+] Performing JS exposure scan"
    gau "$TARGET_DOMAIN"  | grep "\\.js$" | sort -u | tee JS.txt
    nuclei -l JS.txt -t nuclei_templates/js/information-disclosure-in-js-files.yaml | notify -bulk
}

scan_with_new_nuclei_templates() {
    echo "[+] Scan with newly added templates to the nuclei templates repo"
    echo "$TARGET_DOMAIN" | nuclei -t nuclei-templates/ -nt -es info | notify -bulk
}

perform_full_nuclei_scan() {
    echo "[+] Performing a full nuclei scan"
    echo "$TARGET_DOMAIN" | nuclei -t nuclei_templates/Others -es info | notify -bulk
}

xss_scan() {
    echo "[+] Scanning for XSS"
    gau "$TARGET_DOMAIN" | kxss | notify --bulk
}

fuuzing() {
  echo "[+] Fuzzing using h0tak88r_fuzz.txt wordlist"
  ffuf https://$TARGET_DOMAIN/FUZZ -w Wordlists/h0tak88r_fuzz.txt -mc 200,403 -o focusResults/ffufGET.txt
  ffuf https://$TARGET_DOMAIN/FUZZ -w Wordlists/h0tak88r_fuzz.txt -mc 200,403 -X POST -o focusResults/ffufPOST.txt
}

focusScan() {
    check_required_tools

    banner
    cleanup_subs_directory

    TARGET_DOMAIN=$(get_target_domain)
    get_discord_webhooks

    xss_scan
    perform_port_scanning
    perform_exposed_panels_scan
    perform_js_exposure_scan
    scan_with_new_nuclei_templates
    perform_full_nuclei_scan
    fuuzing

    send_file_to_discord "$DISCORD_WEBHOOK" "focusResults/ffufGET.txt"
    send_file_to_discord "$DISCORD_WEBHOOK" "focusResults/ffufPOST.txt"
}

# Main execution
focusScan