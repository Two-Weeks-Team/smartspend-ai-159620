async function throwApiError(res: Response, fallback: string): Promise<never> {
  const raw = await res.text();
  const parsed = raw ? safeParseJson(raw) : null;
  const message = parsed?.error?.message ?? parsed?.detail ?? parsed?.message ?? raw ?? fallback;
  throw new Error(message || fallback);
}

function safeParseJson(raw: string): any {
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export type Transaction = {
  transaction_id: string;
  amount: number;
  description: string;
};

export type CategorizedTransaction = {
  transaction_id: string;
  category: string;
};

export async function fetchItems(): Promise<{ items: any[] }> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL ?? ''}/api/items`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    credentials: "include"
  });
  if (!res.ok) {
    throw new Error("Failed to fetch items");
  }
  return res.json();
}

export async function categorizeTransactions(transactions: Transaction[]): Promise<{ categorized_transactions: CategorizedTransaction[] }> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL ?? ''}/api/transactions/categorize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ transactions })
  });
  if (!res.ok) {
    await throwApiError(res, "Categorization failed");
  }
  return res.json();
}
