const API_BASE_URL = "http://localhost:8000/api/v1";

export async function sendChatMessage(message: string) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!response.ok) {
    throw new Error("Failed to send chat message");
  }
  return response.json();
}

export async function fetchPnLReport() {
  const response = await fetch(`${API_BASE_URL}/reports/pl`);
  if (!response.ok) {
    throw new Error("Failed to fetch P&L report");
  }
  return response.json();
}

export async function fetchBalanceSheet() {
  const response = await fetch(`${API_BASE_URL}/reports/balance-sheet`);
  if (!response.ok) {
    throw new Error("Failed to fetch Balance Sheet report");
  }
  return response.json();
}
