from flask import Flask, render_template, request
import socket

app = Flask(__name__)

# Ethical hacking recon ports
PORTS = {
    21: ("FTP", "HIGH", "Cleartext credentials"),
    22: ("SSH", "LOW", "Secure if configured"),
    23: ("Telnet", "HIGH", "Insecure protocol"),
    80: ("HTTP", "MEDIUM", "Service exposure"),
    443: ("HTTPS", "LOW", "Encrypted service"),
    445: ("SMB", "HIGH", "Lateral movement risk"),
    3389: ("RDP", "HIGH", "Brute-force target"),
}

def grab_banner(target, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((target, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "No banner"
    except:
        return "No banner"

def scan_target(target):
    findings = []
    risk_summary = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for port, (service, risk, reason) in PORTS.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)

            if sock.connect_ex((target, port)) == 0:
                banner = grab_banner(target, port)

                findings.append({
                    "port": port,
                    "service": service,
                    "risk": risk,
                    "reason": reason,
                    "banner": banner
                })

                risk_summary[risk] += 1

            sock.close()
        except:
            pass

    return findings, risk_summary

@app.route("/", methods=["GET", "POST"])
def dashboard():
    results = []
    target = ""
    risk_summary = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    if request.method == "POST":
        target = request.form["target"]
        results, risk_summary = scan_target(target)

    return render_template(
        "dashboard.html",
        target=target,
        results=results,
        risk_summary=risk_summary
    )

if __name__ == "__main__":
    app.run(debug=True)
