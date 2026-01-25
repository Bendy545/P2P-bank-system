const FIELDS = {
  my_bank_code: "bank_code",
  listen_port: "listen_port",
  remote_port: "remote_port",
  cmd_timeout_sec: "cmd_timeout",
  client_count: "client_count",
  bank_total: "bank_total",
  server_running: "server_running",
  db_backend: "db_backend"
};

async function fetchStatus() {
  try {
    const r = await fetch("/api/status");
    if (!r.ok) return;

    const status = await r.json();

    Object.entries(FIELDS).forEach(([apiKey, domId]) => {
      if (status[apiKey] !== undefined) {
        const el = document.getElementById(domId);
        if (el) {
          el.textContent = status[apiKey];
        }
      }
    });
  } catch (e) {
    console.error("fetchStatus failed", e);
  }
}

async function fetchLogs() {
  try {
    const r = await fetch("/api/logs");
    if (!r.ok) return;

    const data = await r.json();

    if (!Array.isArray(data)) {
      console.error("logs api error:", data);
      return;
    }

    const tbody = document.querySelector("#log-table tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    data.forEach(l => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${l.created_at ?? ""}</td>
        <td>${l.level ?? ""}</td>
        <td>${l.event_type ?? ""}</td>
        <td>${l.command ?? ""}</td>
        <td>${l.message ?? ""}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("fetchLogs failed", e);
  }
}

async function fetchAccounts() {
  try {
    const r = await fetch("/api/accounts");
    if (!r.ok) return;

    const data = await r.json();

    if (!Array.isArray(data)) {
      console.error("account api error:", data);
      return;
    }

    const tbody = document.querySelector("#account-table tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    data.forEach(a => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${a.account_no ?? ""}</td>
        <td>${a.balance ?? ""}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("fetchAccounts failed", e);
  }
}


window.addEventListener("load", () => {
  fetchStatus();
  fetchLogs();
  fetchAccounts();

  setInterval(fetchStatus, 2000);
  setInterval(fetchLogs, 3000);
  setInterval(fetchAccounts, 4000);
});
